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


def listing_price_text(l):
    p = l.get("price")
    if l.get("askForPricing") or not p:
        return "Ask for pricing"
    return "$" + "{:,}".format(int(p)) if isinstance(p, (int, float)) else str(p)


def load():
    return json.loads((ROOT / "data" / "lots.json").read_text())


FOR_SALE = ("For Sale", "Move in Ready", "Coming Soon")
# only these lots react to the pointer: a homesite you can still buy. Sold lots, model homes, future models, the Sales
# Center and future-release lots are part of the picture only (no hover, no card, not focusable).
INTERACTIVE = ("available",)


def lot_listings(listings):
    """{lot number: listing} for SunRiver Firelight homes currently for sale, read from the listing address
    ("Home 26, 992 W Frank Ave"), so a new listing in Sanity links its lot on the next deploy."""
    out = {}
    for l in listings or ():
        if "firelight" not in (l.get("community") or "").lower() or l.get("status") not in FOR_SALE:
            continue
        m = re.match(r"\s*Home\s+(\d+)", l.get("address") or "")
        if m:
            out[int(m.group(1))] = l
    return out


def svg(plans=(), listings=()):
    data = load()
    homes = lot_listings(listings)
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
        home = homes.get(n) if st == "available" else None
        if home:
            tip = "Lot %d: %s for sale" % (n, home.get("title") or plan or "Home")
        if st in INTERACTIVE:
            attrs = ' data-tip="%s" data-status="%s" tabindex="0" role="link" aria-label="%s"' % (tip, st, tip)
        else:
            attrs = ' data-status="%s"' % st
        if q:
            attrs += ' data-plan="%s"' % q["slug"]
        if home:
            attrs += ' data-home="%s"' % home["slug"]
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
            # no "SOLD" label: the red fill and the key already say it
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
    for n, l in homes.items():
        cards["home:" + l["slug"]] = {"name": l.get("title") or "Home", "sqft": "{:,}".format(l.get("squareFootage") or 0),
                                      "price": listing_price_text(l), "spec": "%s bed | %s bath" % (l.get("beds") or "", l.get("baths") or ""),
                                      "img": S(l["photo"], 640) if l.get("photo") else "", "url": "/homes-for-sale/%s" % l["slug"]}
    plan_json = json.dumps(cards, separators=(",", ":")).replace("</", "<\\/")
    avail = sum(1 for e in lots.values() if e.get("status") == "available")
    sold = sum(1 for e in lots.values() if e.get("status") == "sold")
    out = re.sub(r"<svg\b", '<svg class="lotmap-svg" role="group" aria-label="SunRiver Firelight lot map: %d homesites available, %d sold"' % (avail, sold), out, count=1)
    out = re.sub(r"<\?xml[^>]*>", "", out)
    # lot card: Option 1 "Light" (chosen 2026-10-29); the "More info" style stays in site.js under .card-detail
    return '''<div class="lotmap card-light">
  <div class="lotmap-scroll lotmap-window">
    <div class="lotmap-stage">%s</div>
    <div class="lotmap-zoom" role="group" aria-label="Map zoom">
      <button type="button" data-zoom="in" aria-label="Zoom in"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 4v12M4 10h12"/></svg></button>
      <button type="button" data-zoom="out" aria-label="Zoom out"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h12"/></svg></button>
      <button type="button" data-zoom="reset" aria-label="Show the whole map"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5V3h4.5M12.5 3H17v4.5M17 12.5V17h-4.5M7.5 17H3v-4.5"/></svg></button>
    </div>
    <p class="lotmap-hint">Drag to explore. Pinch or use + to zoom.</p>
    <ul class="lotmap-key" aria-label="Map key">
      <li><span class="sw sw-open"></span>Available</li>
      <li><span class="sw sw-sold"></span>Sold</li>
      <li><span class="sw sw-model"></span>Model home</li>
      <li><span class="sw sw-future"></span>Future model</li>
      <li><span class="sw sw-plan"></span>Plan selected</li>
    </ul>
    <div class="lotmap-card" hidden></div>
    <script type="application/json" class="lotmap-plans">%s</script>
  </div>
</div>''' % (out.strip(), plan_json)
