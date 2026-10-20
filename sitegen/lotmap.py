"""SunRiver Firelight interactive lot map.

The art is Adam's Illustrator export (sitegen/lotmap_template.svg). Each lot shape carries data-lot="N";
the baked-in numbers, number circles and SOLD labels were stripped so they can be drawn from data.
Status and plan colors live in data/lots.json: marking a lot sold is a one-word edit there.
"""
import json
import re
from pathlib import Path

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


def svg():
    data = load()
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
        attrs = ' data-tip="%s" tabindex="0" role="img" aria-label="%s"' % (tip, tip)
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
    avail = sum(1 for e in lots.values() if e.get("status") == "available")
    sold = sum(1 for e in lots.values() if e.get("status") == "sold")
    out = re.sub(r"<svg\b", '<svg class="lotmap-svg" role="group" aria-label="SunRiver Firelight lot map: %d homesites available, %d sold"' % (avail, sold), out, count=1)
    out = re.sub(r"<\?xml[^>]*>", "", out)
    return '''<div class="lotmap">
  <div class="lotmap-scroll">
    %s
    <div class="lotmap-tip" hidden></div>
  </div>
  <ul class="lotmap-key">
    <li><span class="sw sw-open"></span>Available</li>
    <li><span class="sw sw-sold"></span>Sold</li>
    <li><span class="sw sw-model"></span>Model home</li>
    <li><span class="sw sw-future"></span>Future model</li>
    <li><span class="sw sw-plan"></span>Plan selected</li>
  </ul>
</div>''' % out.strip()
