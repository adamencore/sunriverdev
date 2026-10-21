"""SunRiver Firelight interactive lot map.

The art is Adam's Illustrator export (sitegen/lotmap_template.svg). Each lot shape carries data-lot="N";
the baked-in numbers, number circles and SOLD labels were stripped so they can be drawn from data.
Status and plan colors live in data/lots.json: marking a lot sold is a one-word edit there.
"""
import json
import re
from pathlib import Path

from .lib import S

ROOT = Path(__file__).resolve().parent.parent
GEO = json.loads((ROOT / "sitegen" / "lotmap_geo.json").read_text())
TEMPLATE = (ROOT / "sitegen" / "lotmap_template.svg").read_text()

RED = "#D91E37"
WHITE = "#FFFFFF"
NUM_LIGHT = "#F3F0E8"
BADGE = {"slate": "#33637A", "sage": "#819F85", "orange": "#E07E35", "gray": "#8A8F99"}
STATUS_LABEL = {"available": "Available", "sold": "Sold", "model": "Model home", "future": "Future model",
                "sales": "Sales Center", "upcoming": "Future release"}


def load():
    return json.loads((ROOT / "data" / "lots.json").read_text())


def svg(plans=()):
    data = load()
    by_name = {q["name"].lower(): q for q in plans}
    colors = data["colors"]
    lots = {e["lot"]: e for e in data["lots"]}
    out = TEMPLATE
    marks = []
    for n, e in lots.items():
        g = GEO.get(str(n))
        if not g:
            continue
        st = e.get("status", "available")
        plan_key = e.get("color") if st == "available" and e.get("color") in colors else None
        plan = e.get("plan") or (colors[plan_key]["plan"] if plan_key else None)
        tip = "Lot %d: %s" % (n, STATUS_LABEL.get(st, st.title()))
        if plan and st not in ("sold", "model"):
            tip += " (%s plan)" % plan
        elif st == "model":
            tip = "Lot %d: %s model home" % (n, plan)
        fill = None
        if st == "sold":
            fill = RED
        elif plan_key:
            fill = colors[plan_key]["hex"]
        elif st in ("available", "upcoming"):
            fill = WHITE
        q = by_name.get((plan or "").lower())
        attrs = ' data-tip="%s" data-status="%s" tabindex="0" role="link" aria-label="%s"' % (tip, st, tip)
        if q:
            attrs += ' data-plan="%s"' % q["slug"]
        if fill:
            attrs += ' style="fill:%s"' % fill

        def tag(m, attrs=attrs, st=st, n=n):
            head = re.sub(r'\sclass="([^"]*)"', lambda c: ' class="%s lm-lot is-%s"' % (c.group(1), st), m.group(2))
            if "lm-lot" not in head:
                head += ' class="lm-lot is-%s"' % st
            return m.group(1) + head + ' data-lot="%d"%s' % (n, attrs)
        # tag the lot's shape in the Illustrator art
        out, k = re.subn(r'(<(?:path|polygon|rect|polyline)\b)([^>]*?)\sdata-lot="%d"' % n, tag, out, count=1)
        if not k or g.get("strip") and st != "sold":
            continue
        if "c" not in g:
            continue
        cx, cy = g["c"]
        if st == "sold":
            marks.append('<circle cx="%.2f" cy="%.2f" r="8.47" fill="%s"/>' % (cx, cy, WHITE))
            marks.append('<text x="%.2f" y="%.2f" fill="%s">%d</text>' % (cx, cy + 3.45, RED, n))
            dx, dy = g.get("s", [1.0, 13.5])  # SOLD sits where the Illustrator art put it
            marks.append('<text class="lm-sold" x="%.2f" y="%.2f" fill="%s">SOLD</text>' % (cx + dx, cy + dy + 3.45, WHITE))
        elif plan_key:
            marks.append('<text x="%.2f" y="%.2f" fill="%s">%d</text>' % (cx, cy + 3.45, WHITE, n))
        else:
            badge = "gray" if st == "upcoming" else e.get("badge", "slate")
            marks.append('<circle cx="%.2f" cy="%.2f" r="8.47" fill="%s"/>' % (cx, cy, BADGE.get(badge, BADGE["slate"])))
            marks.append('<text x="%.2f" y="%.2f" fill="%s">%d</text>' % (cx, cy + 3.45, NUM_LIGHT, n))
    out = out.replace("</svg>", '<g class="lm-marks" aria-hidden="true">%s</g></svg>' % "".join(marks))
    cards = {}
    for q in plans:
        ref = q.get("gallery") and q["gallery"][0]["asset"]
        cards[q["slug"]] = {"name": q["name"], "sqft": "{:,}".format(q["squareFootage"]), "price": q.get("priceRange", ""),
                            "spec": q.get("specLine", ""), "img": S(ref, 640) if ref else "", "url": "/floor-plans/%s" % q["slug"]}
    plan_json = json.dumps(cards, separators=(",", ":")).replace("</", "<\\/")
    avail = sum(1 for e in lots.values() if e.get("status") == "available")
    sold = sum(1 for e in lots.values() if e.get("status") == "sold")
    out = re.sub(r"<svg\b", '<svg class="lotmap-svg" role="group" aria-label="SunRiver Firelight lot map: %d homesites available, %d sold"' % (avail, sold), out, count=1)
    out = re.sub(r"<\?xml[^>]*>", "", out)
    return '''<div class="lotmap-preview" role="group" aria-label="Lot card preview">
  <span>Preview the lot card:</span>
  <button type="button" data-card="light" aria-pressed="true">Option 1: Light</button>
  <button type="button" data-card="detail" aria-pressed="false">Option 2: More info</button>
</div>
<div class="lotmap card-light">
  <div class="lotmap-scroll lotmap-window">
    <div class="lotmap-stage">%s</div>
    <div class="lotmap-zoom" role="group" aria-label="Map zoom">
      <button type="button" data-zoom="in" aria-label="Zoom in"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 4v12M4 10h12"/></svg></button>
      <button type="button" data-zoom="out" aria-label="Zoom out"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h12"/></svg></button>
      <button type="button" data-zoom="reset" aria-label="Show the whole map"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5V3h4.5M12.5 3H17v4.5M17 12.5V17h-4.5M7.5 17H3v-4.5"/></svg></button>
    </div>
    <p class="lotmap-hint">Drag to explore. Pinch or use + to zoom.</p>
    <div class="lotmap-card" hidden></div>
    <script type="application/json" class="lotmap-plans">%s</script>
  </div>
  <ul class="lotmap-key">
    <li><span class="sw sw-open"></span>Available</li>
    <li><span class="sw sw-sold"></span>Sold</li>
    <li><span class="sw sw-model"></span>Model home</li>
    <li><span class="sw sw-future"></span>Future model</li>
    <li><span class="sw sw-plan"></span>Plan selected</li>
  </ul>
</div>''' % (out.strip(), plan_json)
