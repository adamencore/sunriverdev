"""SunRiver Firelight interactive lot map.

Shapes come from sitegen/lotmap_geo.json (traced from the Illustrator map).
Status and colors come from data/lots.json, so marking a lot sold is a one-word edit there.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO = json.loads((ROOT / "sitegen" / "lotmap_geo.json").read_text())
STATUS_LABEL = {"available": "Available", "sold": "Sold", "model": "Model home", "future": "Future model", "sales": "Sales Center"}
# Strip lots along Honey Mesquite Dr carry their numbers outside the lot, already drawn on the base art.
OUTSIDE_NUMBER = {4, 5, 6, 7, 8, 9, 67, 68, 69, 70, 71}


def load():
    return json.loads((ROOT / "data" / "lots.json").read_text())


def _label(n, cx, cy, lines, cls):
    if len(lines) == 1:
        return '<text class="%s" x="%d" y="%d">%s</text>' % (cls, cx, cy, lines[0])
    return '<text class="%s" x="%d" y="%d"><tspan x="%d" dy="-0.55em">%s</tspan><tspan x="%d" dy="1.1em">%s</tspan></text>' % (
        cls, cx, cy, cx, lines[0], cx, lines[1])


def svg():
    data = load()
    colors = data["colors"]
    out = []
    for e in data["lots"]:
        n = e["lot"]
        g = GEO.get(str(n))
        if not g:
            continue
        st = e.get("status", "available")
        cx, cy = g["label"]
        cls = ["lm-lot", "is-" + st]
        style = ""
        if st == "available" and e.get("color") in colors:
            cls.append("has-plan")
            style = ' style="--lot:%s"' % colors[e["color"]]["hex"]
            if e["color"] == "yellow":
                cls.append("light")
        plan = e.get("plan") or (colors.get(e.get("color"), {}).get("plan") if e.get("color") else None)
        tip = "Lot %d: %s" % (n, STATUS_LABEL.get(st, st.title()))
        if plan and st != "sold":
            tip += " (%s)" % plan
        inner = '<polygon points="%s"/>' % g["pts"]
        if st == "model":
            inner += _label(n, cx, cy, [e.get("plan", "")], "lot-name")
        elif st == "future":
            inner += _label(n, cx, cy, ["Future", "Model"], "lot-name")
        elif st == "sales":
            inner += _label(n, cx, cy, ["Sales", "Center"], "lot-name")
        elif n not in OUTSIDE_NUMBER:
            if "has-plan" in cls:
                inner += '<text class="lot-num" x="%d" y="%d">%d</text>' % (cx, cy, n)
            else:
                inner += '<circle class="lot-badge %s" cx="%d" cy="%d" r="23"/><text class="lot-num" x="%d" y="%d">%d</text>' % (
                    "b-" + e.get("badge", "slate"), cx, cy, cx, cy, n)
        out.append('<g class="%s" data-lot="%d" data-tip="%s" tabindex="0" role="img" aria-label="%s"%s>%s</g>' % (
            " ".join(cls), n, tip, tip, style, inner))
    avail = sum(1 for e in data["lots"] if e.get("status") == "available")
    sold = sum(1 for e in data["lots"] if e.get("status") == "sold")
    return '''<div class="lotmap">
  <div class="lotmap-scroll">
    <svg class="lotmap-svg" viewBox="0 0 1500 1726" aria-labelledby="lotmap-title">
      <title id="lotmap-title">SunRiver Firelight lot map: %d homesites available, %d sold</title>
      <image href="/assets/lotmap/base.webp" width="1500" height="1726"/>
      %s
    </svg>
    <div class="lotmap-tip" hidden></div>
  </div>
  <ul class="lotmap-key">
    <li><span class="sw sw-open"></span>Available</li>
    <li><span class="sw sw-sold"></span>Sold</li>
    <li><span class="sw sw-model"></span>Model home</li>
    <li><span class="sw sw-future"></span>Future model</li>
    <li><span class="sw sw-plan"></span>Plan selected</li>
  </ul>
</div>''' % (avail, sold, "\n      ".join(out))
