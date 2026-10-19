"""Pages driven by the Sanity CMS: floor plans, homes for sale, Bucketlist Living blog."""
import math
import re

from .figma_assets import FG
from .lib import (PAGES, PHONE, PHONE_TEL, S, V, VP, FOUNDERS_BADGE, add, btn, chat_section, clean, esc, img, money,
                  nice_date, sand_hero, simg, slugify, star_list)

STATUS_ORDER = {"Move in Ready": 0, "For Sale": 1, "Under Contract": 2, "Sold": 3}
COMMUNITIES = ["SunRiver Firelight", "SunRiver Villas", "SunRiver St George"]
COMMUNITY_LABEL = {"SunRiver St George": "SunRiver St. George"}
SQFT_RANGES = [(1250, 1400), (1450, 1700), (1750, 1900)]
DISCLAIMER = ("Prices are subject to change without notice and reflect standard homesites. Dimensions and square footage are approximate. "
              "Renderings are artist's conceptions and are not meant to show specific detailing. Marketed by SunRiver St. George Realty, L.C.")
ICON_BED, ICON_BATH, ICON_GARAGE = VP("/images/icons/bed.png"), VP("/images/icons/bath.png"), VP("/images/icons/garage.png")


def num(v):
    if v is None:
        return ""
    return ("%g" % float(v))


# ================================================================== FLOOR PLANS
def plan_image(p):
    g = p.get("gallery") or []
    return g[0]["asset"] if g else (p.get("planDiagram") or {}).get("asset")


def plan_card(p, sizes="(max-width: 860px) 100vw, 33vw"):
    badge = '<span class="badge">%s</span>' % esc(p["badge"]) if p.get("badge") else ""
    ref = plan_image(p)
    pic = simg(ref, "%s exterior rendering at SunRiver Firelight" % p["name"], 800, sizes=sizes) if ref else ""
    return '''<a class="plan-card" href="/floor-plans/%s">
  <div class="plan-img">%s%s</div>
  <div class="plan-body"><span class="sqft">%s</span><span class="arrow" aria-hidden="true"></span>
    <span class="name">%s</span><span class="meta">%s ft&sup2; | %s</span><span class="price">%s</span><span class="explore">Explore</span></div></a>''' % (
        p["slug"], pic, badge, p["squareFootage"], esc(p["name"]), "{:,}".format(p["squareFootage"]), esc(p.get("specLine", "")), esc(p.get("priceRange", "")))


def fp_card(p):
    """Floor plan card from the OFFICIAL Figma "Homes for Sale / Model Homes" frame (6:206): photo, number and
    name with a yellow underline, sand band with size, spec and price, then the Explore pill."""
    ref = plan_image(p)
    pic = simg(ref, "%s exterior rendering at SunRiver Firelight" % p["name"], 540, sizes="270px") if ref else ""
    badge = '<em>%s</em>' % esc(p["badge"]) if p.get("badge") else ""
    # keep each part together and let the line break after a bar, like the design ("2 BED | 2 BATH | +")
    spec = " ".join("%s&nbsp;|" % part.strip().replace(" ", "&nbsp;") for part in esc(p.get("specLine", "")).split("|"))[:-len("&nbsp;|")].replace("&nbsp;(", " (")
    return '''<a class="fp-card" href="/floor-plans/%s">
  <span class="fp-img">%s</span>
  <span class="fp-head"><span class="fp-num">%s%s</span><span class="fp-name">%s</span></span>
  <span class="fp-band"><span class="fp-sqft">%s ft<sup>2</sup></span><span class="fp-spec">%s</span><span class="fp-price">%s</span></span>
  <span class="fp-foot"><span class="fp-btn">Explore</span></span>
</a>''' % (p["slug"], pic, p["squareFootage"], badge, esc(p["name"]), p["squareFootage"], spec, esc(p.get("priceRange", "")))


def min_price(plans):
    vals = []
    for p in plans:
        m = re.search(r"\$([\d,]+)", p.get("priceRange") or "")
        if m:
            vals.append(int(m.group(1).replace(",", "")))
    return "${:,}".format(min(vals)) if vals else ""


def build_floor_plans(plans):
    grid = "".join(fp_card(p) for p in plans)
    add("/floor-plans", "Floor Plans", "%d SunRiver Firelight floor plans in Toquerville, Utah, starting at %s." % (len(plans), min_price(plans)), "life", '''
%s
<section class="section">
  <div class="wrap stack-lg">
    <div class="fp-grid">%s</div>
    <p class="note center">%s</p>
  </div>
</section>
%s''' % (sand_hero("", "SunRiver Firelight", "Floor Plans"), grid, DISCLAIMER, chat_section()))

    for i, p in enumerate(plans):
        build_plan(p, i, plans)


def contact_row(founders=True):
    """Founders Club card and Contact Our Sales Team card (OFFICIAL "Homes for Sale Home Detail", 6:503)."""
    fc = ""
    if founders:
        fc = '''<a class="hd-founders" href="/founders-club"><h2>Join the <span>SunRiver Firelight Founders Club</span></h2><p>Reserve your homesite now and lock in Founders Club pricing.</p>%s</a>''' % (
            img(V("founders-badge-tilt.3k3jxq99pwu_k.svg"), "", "hd-badge"))
    return '''<div class="hd-bottom%s">
      %s
      <div class="hd-sales">
        <div class="hd-sales-text"><h2>Contact Our Sales Team</h2><p class="hd-q">Questions? Inquiries?</p>
          <p class="hd-contact"><a href="mailto:info@sunriver.com">info@sunriver.com</a><span aria-hidden="true">|</span><a href="%s">%s</a></p>
          <a class="hd-btn yellow" href="/contact-us">Contact Us Today</a></div>
        <div class="hd-team">%s</div>
      </div>
    </div>''' % ("" if fc else " solo", fc, PHONE_TEL, PHONE, img(FG("sales-team"), "The SunRiver sales team"))


def thumbs_html(refs, alt):
    if len(refs) < 2:
        return ""
    return '<div class="hd-thumbs%s">%s%s</div>' % (
        " has-more" if len(refs) > 4 else "",
        "".join('<button type="button" class="thumb%s" data-src="%s" aria-label="Show image %d">%s</button>' % (
            " is-active" if k == 0 else "", S(r, 1600), k + 1, img(S(r, 320), "%s %d" % (alt, k + 1))) for k, r in enumerate(refs)),
        '<button type="button" class="see-more" aria-expanded="false">See more</button>' if len(refs) > 4 else "")


def plan_chips(p):
    spec = p.get("specLine") or ""
    garage = re.search(r"(Ext\.\s*)?(\d+(?:\.\d+)?)\s*Car Garage", spec)
    chips = []
    if p.get("bedrooms"):
        chips.append('<span class="chip">%s%s Bed</span>' % (img(ICON_BED, "", "chip-icon"), num(p["bedrooms"])))
    if p.get("bathrooms"):
        chips.append('<span class="chip">%s%s Bath</span>' % (img(ICON_BATH, "", "chip-icon"), num(p["bathrooms"])))
    if garage:
        chips.append('<span class="chip">%s%s%s Car Garage</span>' % (img(ICON_GARAGE, "", "chip-icon"), "Ext. " if garage.group(1) else "", garage.group(2)))
    if "hobby" in spec.lower():
        chips.append('<span class="chip">Hobby Room</span>')
    return '<span class="chips hd-chips">%s</span>' % "".join(chips)


def build_plan(p, i, plans):
    """Floor plan page on the OFFICIAL "Homes for Sale Home Detail" template (6:503)."""
    name = esc(p["name"])
    gallery = p.get("gallery") or []
    refs = [g["asset"] for g in gallery]
    alt = gallery[0].get("alt") if gallery and gallery[0].get("alt") else "%s at SunRiver Firelight" % p["name"]
    main = simg(refs[0], alt, 1400, loading="eager", sizes="(max-width: 860px) 100vw, 667px") if refs else ""
    sqft = "{:,}".format(p["squareFootage"])
    spec = p.get("specLine", "")
    status = esc(p["badge"]) if p.get("badge") else "Available to build"
    lot = " &middot; Lot width %s'" % num(p["width"]) if p.get("width") else ""
    story = ("The %s is a %s sq ft single-story home at SunRiver Firelight: %s. Every SunRiver Firelight home comes with our standard luxury features, "
             "and you can make it yours at the Design Center. SunRiver Firelight is SunRiver's newest 55+ community, just west of Toquerville, "
             "with mountain views in every direction and Zion 31 minutes away." % (p["name"], sqft, spec.lower().replace(" | ", ", ")))
    if p.get("matterportId"):
        side = '<div class="hd-map hd-tour"><iframe src="https://my.matterport.com/show/?m=%s" title="%s 3D virtual tour" allow="xr-spatial-tracking; fullscreen" allowfullscreen loading="lazy"></iframe></div>' % (p["matterportId"], name)
    else:
        side = '<div class="hd-map"><iframe src="https://www.google.com/maps?q=SunRiver+Firelight,+Toquerville,+UT&amp;output=embed" title="Map of SunRiver Firelight" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>'
    diagram = p.get("planDiagram") or {}
    drawing = ""
    if diagram.get("asset"):
        drawing = '''<div class="hd-plan">
      <div class="hd-plan-text"><h2>The %s Floor Plan</h2><p>Click the plan to enlarge it.</p><p class="hd-note">%s</p></div>
      <a class="hd-plan-img" href="%s" data-lightbox>%s</a>
    </div>''' % (name, DISCLAIMER, S(diagram["asset"], 2400), simg(diagram["asset"], diagram.get("alt") or "%s floor plan drawing" % p["name"], 900, sizes="(max-width: 860px) 100vw, 420px"))
    features = ""
    if p.get("features"):
        features = '<div class="hd-features"><h2>Standard Luxury Features</h2>%s</div>' % star_list([esc(f) for f in p["features"]], "cols-2")
    others = [plans[(i + k) % len(plans)] for k in (1, 2, 3) if len(plans) > k]
    like = '<section class="hd-like"><div class="wrap"><h2>You may like these</h2><div class="fp-grid">%s</div></div></section>' % "".join(fp_card(q) for q in others)
    tour_link = '<p class="hd-mls"><a href="#tour-card">Take the 3D virtual tour</a></p>' if p.get("matterportId") else ""
    add("/floor-plans/%s" % p["slug"], "%s Floor Plan" % p["name"],
        "The %s at SunRiver Firelight: %s sq ft, %s, %s." % (p["name"], sqft, spec, p.get("priceRange", "")), "life", '''
<section class="hd">
  <div class="wrap">
    <a class="hd-back" href="/floor-plans">See all floor plans</a>
    <div class="hd-top">
      <div class="hd-media viewer"><div class="viewer-main">%s</div>%s</div>
      <div class="hd-card">
        <p class="hd-price">%s</p>
        <p class="hd-name"><strong>%s</strong><span aria-hidden="true">|</span>%s sqft</p>
        <h1 class="hd-address">The %s Floor Plan</h1>
        <p class="hd-comm">SunRiver Firelight%s</p>
        %s
        <p class="hd-status">%s</p>
        <div class="hd-actions"><a class="hd-btn solid" href="/contact-us">Schedule a Tour</a><a class="hd-btn" href="/contact-us#team">Request Info</a></div>
        %s
      </div>
    </div>
    <div class="hd-desc" id="tour-card">
      <div class="hd-desc-text"><h2>Single Family Home in Toquerville</h2><p>%s</p></div>
      %s
    </div>
    %s
    %s
    %s
  </div>
</section>
%s''' % (main, thumbs_html(refs, alt), esc(p.get("priceRange", "")), name, sqft, name, lot, plan_chips(p), status, tour_link,
         esc(story), side, features, drawing, contact_row(), like), body_class="sand-page")


# ================================================================== HOMES FOR SALE
def listing_sort_key(l):
    return (STATUS_ORDER.get(l.get("status"), 9), -int((l.get("statusDate") or "0000-00-00").replace("-", "")), l.get("title") or "")


def listing_price(l):
    if l.get("askForPricing") or not l.get("price"):
        return "Ask for pricing"
    return money(l["price"])


def status_chip(status):
    return '<span class="status status-%s">%s</span>' % (slugify(status or ""), esc(status or ""))


def spec_chips(l, cls="chips"):
    chips = []
    if l.get("beds"):
        chips.append('<span class="chip">%s%s Bed</span>' % (img(ICON_BED, "", "chip-icon"), num(l["beds"])))
    if l.get("baths"):
        chips.append('<span class="chip">%s%s Bath</span>' % (img(ICON_BATH, "", "chip-icon"), num(l["baths"])))
    if l.get("garageSpaces"):
        chips.append('<span class="chip">%s%s Car Garage</span>' % (img(ICON_GARAGE, "", "chip-icon"), num(l["garageSpaces"])))
    return '<span class="%s">%s</span>' % (cls, "".join(chips))


def short_address(l):
    """'Home 26, 992 W Frank Ave, Toquerville, UT' -> '992 W Frank Ave, Toquerville, UT'"""
    return re.sub(r"^\s*Home\s+\d+,\s*", "", l.get("address") or "")


def listing_card(l):
    """Homes for sale card, OFFICIAL Figma "Homes for Sale Filter Simple" (6:267)."""
    photo = simg(l["photo"], l.get("photoAlt") or l.get("title"), 568, sizes="(max-width: 700px) 100vw, 284px") if l.get("photo") else ""
    data = 'data-community="%s" data-status="%s" data-sqft="%s" data-beds="%s" data-baths="%s" data-garage="%s" data-hobby="%s"' % (
        esc(l.get("community", "")), esc(l.get("status", "")), l.get("squareFootage") or 0, l.get("beds") or 0,
        l.get("baths") or 0, l.get("garageSpaces") or 0, l.get("hobbyRooms") or 0)
    return '''<a class="home-card" href="/homes-for-sale/%s" %s>
  <span class="home-img">%s<span class="home-badge">%s</span></span>
  <span class="home-title"><strong>%s</strong><span>{:,} sqft</span></span>
  <span class="home-address">%s</span>
  <span class="home-price">%s</span>
  %s
</a>'''.format(l.get("squareFootage") or 0) % (
        l["slug"], data, photo, esc(l.get("status") or ""), esc(clean(l.get("title"))), esc(short_address(l)), listing_price(l), spec_chips(l))


def box(name, value, label, checked=False):
    return '<label><input type="checkbox" name="%s" value="%s"%s><span>%s</span></label>' % (name, value, " checked" if checked else "", label)


def plus_group(name, label, options):
    """Minimum-count group (2+, 3+, 4+): square boxes like the design, only one on at a time."""
    return '<fieldset><legend>%s</legend><div class="opts two" data-single>%s</div></fieldset>' % (
        label, "".join(box(name, v, "%s+" % v) for v in options))


def build_homes(listings):
    ls = sorted(listings, key=listing_sort_key)
    cards = "".join(listing_card(l) for l in ls)
    comm = "".join(box("community", c, c, c == "SunRiver Firelight") for c in COMMUNITIES)
    stat = "".join(box("status", st, st) for st in STATUS_ORDER)
    sqft = "".join(box("sqft", "%d-%d" % (a, b), "%d-%d <small>ft2</small>" % (a, b)) for a, b in SQFT_RANGES)
    add("/homes-for-sale", "Homes for Sale", "Move-in ready and available homes at SunRiver Firelight, SunRiver Villas and SunRiver St. George.", "homes", '''
<section class="hfs-band">%s<div class="wrap"><h1>Homes for sale</h1></div></section>
<section class="hfs">
  <div class="wrap hfs-grid">
    <aside class="filters" aria-label="Filter homes">
      <form id="home-filters">
        <p class="filters-title">Filter</p>
        <fieldset><legend>Community</legend><div class="opts">%s</div></fieldset>
        <fieldset><legend>Status</legend><div class="opts">%s</div></fieldset>
        <fieldset><legend>SQFT</legend><div class="opts">%s</div></fieldset>
        %s%s%s%s
        <button type="submit" class="filter-btn">Filter</button>
      </form>
    </aside>
    <div class="hfs-results">
      <p class="results-count" aria-live="polite"><span id="home-count">%d</span> homes</p>
      <div class="home-grid" id="home-grid">%s</div>
      <div class="empty-state" id="home-empty" hidden><h2 class="h3">No homes match those filters.</h2><p>Try widening your search, or talk with our sales team about homes coming soon.</p>%s</div>
    </div>
  </div>
</section>''' % (img(FG("hfs-band"), "", loading="eager"), comm, stat, sqft,
                  plus_group("beds", "Beds", [2, 3, 4]), plus_group("baths", "Bath", [2, 3, 4]), plus_group("garage", "Garage", [2, 3, 4]),
                  plus_group("hobby", "Hobby", [1, 2]), len(ls), cards, btn("Contact Sales", "/contact-us")), body_class="sand-page")

    for l in ls:
        build_listing(l)


def listing_story(l):
    """Heading and paragraph for the description card. Uses the CMS description when one is published."""
    sa = short_address(l)
    city = sa.split(",")[1].strip() if sa.count(",") >= 2 else "Southern Utah"
    head = "Single Family Home in %s" % city
    d = l.get("description")
    if isinstance(d, list):
        d = " ".join("".join(c.get("text", "") for c in b.get("children", [])) for b in d if isinstance(b, dict) and b.get("_type") == "block")
    if isinstance(d, str) and d.strip():
        return head, clean(d.strip())
    title = clean(l.get("title") or "")
    comm = COMMUNITY_LABEL.get(l.get("community"), l.get("community") or "SunRiver")
    parts = []
    if l.get("beds"):
        parts.append("%s bedrooms" % num(l["beds"]))
    if l.get("baths"):
        parts.append("%s bathrooms" % num(l["baths"]))
    if l.get("hobbyRooms"):
        parts.append("a hobby room")
    if l.get("garageSpaces"):
        parts.append("a %s car garage" % num(l["garageSpaces"]))
    spec = (", ".join(parts[:-1]) + " and " + parts[-1]) if len(parts) > 1 else "".join(parts)
    plan = "This %s floor plan home" % title if title and title.lower() != "single family" else "This single family home"
    status = {"Move in Ready": " It is move in ready, so you can settle in and start living here right away.",
              "For Sale": " It is available now.",
              "Under Contract": " It is under contract. Our sales team can show you similar homes.",
              "Sold": " It has sold. Our sales team can show you similar homes."}.get(l.get("status"), "")
    extra = ""
    if l.get("community") == "SunRiver Firelight":
        extra = (" SunRiver Firelight is SunRiver's newest 55+ community, just west of Toquerville with mountain views in every direction "
                 "and Zion 31 minutes away. Founders Club homeowners get two years of HOA dues paid by SunRiver.")
    return head, "%s at %s has %s of living space%s.%s%s" % (
        plan, comm, "{:,} sq ft".format(l.get("squareFootage") or 0), (" with " + spec) if spec else "", status, extra)


def build_listing(l):
    """Listing page, OFFICIAL Figma "Homes for Sale Home Detail" (6:503)."""
    pics = ([l["photo"]] if l.get("photo") else []) + [g for g in (l.get("gallery") or []) if g != l.get("photo")]
    alt = l.get("photoAlt") or l.get("title")
    main = simg(pics[0], alt, 1400, loading="eager", sizes="(max-width: 860px) 100vw, 667px") if pics else ""
    thumbs = ""
    if len(pics) > 1:
        thumbs = '<div class="hd-thumbs%s">%s%s</div>' % (
            " has-more" if len(pics) > 4 else "",
            "".join('<button type="button" class="thumb%s" data-src="%s" aria-label="Show photo %d">%s</button>' % (
                " is-active" if k == 0 else "", S(r, 1600), k + 1, img(S(r, 320), "%s photo %d" % (alt, k + 1))) for k, r in enumerate(pics)),
            '<button type="button" class="see-more" aria-expanded="false">See more</button>' if len(pics) > 4 else "")
    m = re.match(r"\s*Home\s+(\d+)", l.get("address") or "")
    home_no = m.group(1) if m else ""
    videos = ""
    if l.get("youtubeShortIds"):
        vids = "".join('<div class="short"><iframe src="https://www.youtube.com/embed/%s" title="Video tour of %s" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen loading="lazy"></iframe></div>' % (v, esc(l.get("title"))) for v in l["youtubeShortIds"])
        videos = '<section class="hd-videos"><div class="wrap stack-lg"><div class="center stack"><h2 class="h2">Take a look inside%s</h2><hr class="rule center"></div><div class="shorts">%s</div></div></section>' % (
            " Home %s" % home_no if home_no else "", vids)
    addr = short_address(l) or l.get("address") or ""
    title = clean(l.get("title"))
    head, story = listing_story(l)
    comm = COMMUNITY_LABEL.get(l.get("community"), l.get("community", ""))
    mls = '<p class="hd-mls">MLS# %s</p>' % esc(l["mlsNumber"]) if l.get("mlsNumber") else ""
    add("/homes-for-sale/%s" % l["slug"], "%s, %s" % (title, addr),
        "%s at %s: %s sq ft, %s bed, %s bath. %s." % (title, l.get("address") or "", "{:,}".format(l.get("squareFootage") or 0), num(l.get("beds")), num(l.get("baths")), l.get("status", "")), "homes", '''
<section class="hd">
  <div class="wrap">
    <a class="hd-back" href="/homes-for-sale">See all homes for sale</a>
    <div class="hd-top">
      <div class="hd-media viewer"><div class="viewer-main">%s</div>%s</div>
      <div class="hd-card">
        <p class="hd-price">%s</p>
        <p class="hd-name"><strong>%s</strong><span aria-hidden="true">|</span>%s sqft</p>
        <h1 class="hd-address">%s</h1>
        <p class="hd-comm">%s</p>
        %s
        <p class="hd-status">%s</p>
        <div class="hd-actions"><a class="hd-btn solid" href="/contact-us">Schedule a Tour</a><a class="hd-btn" href="/contact-us#team">Request Info</a></div>
        %s
      </div>
    </div>
    <div class="hd-desc">
      <div class="hd-desc-text"><h2>%s</h2><p>%s</p></div>
      <div class="hd-map"><iframe src="https://www.google.com/maps?q=%s&amp;output=embed" title="Map of %s" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
    %s
  </div>
</section>
%s''' % (main, thumbs, listing_price(l), esc(title), "{:,}".format(l.get("squareFootage") or 0), esc(addr),
         esc(comm), spec_chips(l, "chips hd-chips"), esc(l.get("status") or ""), mls,
         esc(head), esc(story), esc(addr).replace(" ", "+"), esc(addr),
         contact_row(l.get("community") == "SunRiver Firelight"), videos), body_class="sand-page")


# ================================================================== BLOG
PER_PAGE = 24


def render_spans(children, mark_defs):
    defs = {d.get("_key"): d for d in mark_defs or []}
    out = []
    for c in children or []:
        t = esc(clean(c.get("text", ""))).replace("\n", "<br>")
        for m in reversed(c.get("marks") or []):
            if m == "strong":
                t = "<strong>%s</strong>" % t
            elif m == "em":
                t = "<em>%s</em>" % t
            elif m == "underline":
                t = "<u>%s</u>" % t
            elif m == "strike-through":
                t = "<s>%s</s>" % t
            elif m == "code":
                t = "<code>%s</code>" % t
            elif m in defs and defs[m].get("_type") == "link" and defs[m].get("href"):
                href = defs[m]["href"]
                ext = href.startswith("http") and "sunriver.com" not in href
                t = '<a href="%s"%s>%s</a>' % (esc(href), ' target="_blank" rel="noopener"' if ext else "", t)
        out.append(t)
    return "".join(out)


def portable_text(body):
    out, list_type, items = [], None, []

    def flush():
        nonlocal list_type, items
        if list_type:
            tag = "ol" if list_type == "number" else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % i for i in items), tag))
        list_type, items = None, []

    for b in body or []:
        t = b.get("_type")
        if t == "block" and b.get("listItem"):
            if list_type != b["listItem"]:
                flush()
                list_type = b["listItem"]
            items.append(render_spans(b.get("children"), b.get("markDefs")))
            continue
        flush()
        if t == "block":
            inner = render_spans(b.get("children"), b.get("markDefs"))
            if not inner.strip():
                continue
            style = b.get("style") or "normal"
            tag = {"h1": "h2", "h2": "h2", "h3": "h3", "h4": "h4", "h5": "h4", "h6": "h4", "blockquote": "blockquote"}.get(style, "p")
            out.append("<%s>%s</%s>" % (tag, inner, tag))
        elif t == "image" and (b.get("asset") or {}).get("_ref"):
            ref = b["asset"]["_ref"]
            out.append('<figure>%s</figure>' % simg(ref, b.get("alt") or "", 1000, sizes="(max-width: 820px) 100vw, 760px"))
    flush()
    return "\n".join(out)


def post_card(p):
    cat = (p.get("categories") or [None])[0]
    cover = simg(p["cover"], p["title"], 640, sizes="(max-width: 700px) 100vw, 30vw") if p.get("cover") else ""
    return '''<a class="post-card" href="/bucketlistliving/%s"><div class="photo">%s</div>%s<h3>%s</h3><time datetime="%s">%s</time></a>''' % (
        p["slug"], cover, '<span class="post-cat">%s</span>' % esc(cat) if cat else "", esc(clean(p["title"])),
        esc((p.get("publishDate") or "")[:10]), nice_date(p.get("publishDate")))


def blog_listing(posts, base, title_html, intro_html, page_title, description, cats, current_cat=None):
    pages = max(1, math.ceil(len(posts) / float(PER_PAGE)))
    chips = '<nav class="cat-chips" aria-label="Categories"><a href="/bucketlistliving"%s>All</a>%s</nav>' % (
        ' aria-current="page"' if not current_cat else "",
        "".join('<a href="/bucketlistliving/category/%s"%s>%s</a>' % (slugify(c), ' aria-current="page"' if c == current_cat else "", esc(c)) for c in cats))
    for n in range(1, pages + 1):
        chunk = posts[(n - 1) * PER_PAGE: n * PER_PAGE]
        path = base if n == 1 else "%s/page/%d" % (base, n)
        prev = '<a class="btn blue-btn" href="%s">Newer</a>' % (base if n == 2 else "%s/page/%d" % (base, n - 1)) if n > 1 else ""
        nxt = '<a class="btn" href="%s/page/%d">Older</a>' % (base, n + 1) if n < pages else ""
        pager = '<nav class="pager" aria-label="Pages">%s<span>Page %d of %d</span>%s</nav>' % (prev, n, pages, nxt) if pages > 1 else ""
        add(path, page_title if n == 1 else "%s, page %d" % (page_title, n), description, "life", '''
%s
<section class="section blog">
  <div class="wrap stack-lg">
    %s
    <div class="post-grid">%s</div>
    %s
  </div>
</section>''' % (title_html + intro_html, chips, "".join(post_card(p) for p in chunk), pager))


def build_blog(posts):
    posts = sorted(posts, key=lambda p: p.get("publishDate") or "", reverse=True)
    cats = sorted(set(c for p in posts for c in (p.get("categories") or []) if c))
    banner = '''<section class="blog-banner">%s<div class="wrap">%s<p>Stories, events and guides from SunRiver Firelight and Southern Utah.</p></div></section>''' % (
        img(V("bucketlist-banner.02if0nz4sgehw.webp"), "", loading="eager"), img(V("bucketlist-wordmark.3qnr5_89a42b3.png"), "Bucketlist Living", "wordmark", "eager"))
    blog_listing(posts, "/bucketlistliving", banner, "", "#bucketlistliving", "Bucketlist Living: stories, events and guides from SunRiver Firelight and Southern Utah.", cats)
    for c in cats:
        cp = [p for p in posts if c in (p.get("categories") or [])]
        blog_listing(cp, "/bucketlistliving/category/%s" % slugify(c), sand_hero("Category", esc(c)), "", "%s | #bucketlistliving" % c,
                     "%s stories from Bucketlist Living at SunRiver." % c, cats, c)

    for i, p in enumerate(posts):
        more = [q for q in posts[max(0, i - 2): i + 6] if q is not p][:4]
        chips = '<div class="post-chips"><a href="/bucketlistliving">#bucketlistliving</a>%s</div>' % "".join(
            '<a href="/bucketlistliving/category/%s">%s</a>' % (slugify(c), esc(c)) for c in (p.get("categories") or []) if c)
        cover = '<div class="post-cover">%s</div>' % simg(p["cover"], p["title"], 1400, loading="eager", sizes="(max-width: 1100px) 100vw, 1040px") if p.get("cover") else ""
        desc = clean(p.get("excerpt")) or clean(" ".join(
            "".join(c.get("text", "") for c in b.get("children", [])) for b in p["body"] if b.get("_type") == "block"))[:155]
        add("/bucketlistliving/%s" % p["slug"], clean(p["title"]), desc, "life", '''
<article class="section post">
  <div class="wrap post-wrap">
    %s
    %s
    <header class="post-head"><h1>%s</h1><time datetime="%s">%s</time></header>
    <div class="post-body">%s</div>
  </div>
</article>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="h2">More from #bucketlistliving</h2><hr class="rule center"></div>
    <div class="post-grid cols-4">%s</div>
    <div class="center">%s</div>
  </div>
</section>''' % (chips, cover, esc(clean(p["title"])), esc((p.get("publishDate") or "")[:10]), nice_date(p.get("publishDate")),
                 portable_text(p.get("body")), "".join(post_card(q) for q in more), btn("See all stories", "/bucketlistliving")))
