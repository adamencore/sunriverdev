"""Pages driven by the Sanity CMS: floor plans, homes for sale, Bucketlist Living blog."""
from . import lotmap
import math
import re

from .figma_assets import FG
from .lib import (full_hero, PAGES, PHONE, PHONE_TEL, S, V, VP, FOUNDERS_BADGE, add, btn, chat_section, clean, esc, img, money,
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


def mh_card(p):
    """Plan card from the OFFICIAL Figma "Homes for Sale / Model Homes NEW" frame: photo with a yellow tag,
    number, name in yellow, size and spec line, serif price on sand."""
    ref = plan_image(p)
    pic = simg(ref, "%s exterior rendering at SunRiver Firelight" % p["name"], 782, sizes="(max-width: 700px) 100vw, 391px") if ref else ""
    tag = '<span class="mh-tag">%s</span>' % esc(p["badge"]) if p.get("badge") else ""
    spec = " &nbsp;|&nbsp; ".join(["%s ft" % p["squareFootage"]] + [esc(x.strip()) for x in (p.get("specLine") or "").split("|") if x.strip()])
    return '''<a class="mh-card" href="/floor-plans/%s">
  <span class="mh-img">%s%s</span>
  <span class="mh-body"><span class="mh-num">%s</span><span class="mh-name">%s</span><span class="mh-spec">%s</span><span class="mh-price">%s</span><span class="mh-go" aria-hidden="true"></span></span>
</a>''' % (p["slug"], pic, tag, p["squareFootage"], esc(p["name"]), spec, esc(p.get("priceRange", "")))


def build_floor_plans(plans):
    """Floor Plans main page: OFFICIAL Figma "Homes for Sale / Model Homes NEW" (6:206).
    Photo hero with the Founders tab, then every plan in a three-column grid."""
    grid = "".join(mh_card(p) for p in plans)
    add("/floor-plans", "Floor Plans", "%d SunRiver Firelight floor plans in Toquerville, Utah, starting at %s." % (len(plans), min_price(plans)), "life-overlay", '''
<section class="fah-hero fp-banner">
  %s
  <div class="wrap fah-hero-inner">
    <h1>Floor Plans</h1>
    <p>Find your home at SunRiver Firelight</p>
  </div>
</section>
<section class="mh-section">
  <div class="wrap">
    <h2 class="visually-hidden">SunRiver Firelight floor plans</h2>
    <div class="mh-grid">%s</div>
  </div>
</section>
<section class="fl-founders">
  %s
  <div class="wrap fl-founders-inner">
    <div class="fl-founders-text">
      <h2>Be part of <span>history</span> at SunRiver Firelight</h2>
      <p>Become a member of the SunRiver Firelight Founders Club and be among the first 74 homeowners to help shape this exciting new community!</p>
      <a class="flp-btn light" href="/founders-club">Learn more</a>
    </div>
    %s
  </div>
</section>
<section class="fl-trails">
  <h2>Over 22 miles of trails</h2>
  %s
</section>
<section class="fl-smart">
  %s
  <div class="wrap fl-smart-inner">
    <h2>Explore our <span>Smart Home</span> options</h2>
    <p>Working alongside our talented designers, you can create a home that captures your imagination and leaves your home just plain smart.</p>
    <a class="flp-btn" href="/energy">Learn more</a>
  </div>
</section>''' % (img(FG("fah-hero"), "SunRiver Firelight homes with red rock mesas behind them", "fah-hero-img", "eager"), grid,
         img(FG("fl-founders"), "", "fl-bg"), img(V("founders-badge-tilt.3k3jxq99pwu_k.svg"), "SunRiver Firelight Founders Club badge", "fl-badge"),
         img(FG("fl-trails"), "Red rock and mountain trail country near SunRiver Firelight", "fl-trails-img"),
         img(FG("fl-smart"), "", "fl-bg")))

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


def thumbs_html(refs, alt, contain=()):
    if len(refs) < 2:
        return ""
    return '<div class="hd-thumbs%s">%s%s</div>' % (
        " has-more" if len(refs) > 4 else "",
        "".join('<button type="button" class="thumb%s" data-src="%s"%s aria-label="Show image %d">%s</button>' % (
            " is-active" if k == 0 else "", S(r, 1600), ' data-fit="contain"' if r in contain else "", k + 1, img(S(r, 320), "%s %d" % (alt, k + 1))) for k, r in enumerate(refs)),
        '<button type="button" class="see-more" aria-expanded="false">See more</button>' if len(refs) > 4 else "")


ICON_HOBBY = '<svg class="chip-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l5-12 4 7 2-3 5 8z" fill="none" stroke="#335A97" stroke-width="1.8" stroke-linejoin="round"/><circle cx="17" cy="6" r="2" fill="none" stroke="#335A97" stroke-width="1.8"/></svg>'


def plan_chips(p):
    """Bed, Bath, Hobby, Garage chips, in the order of the Figma floor plan frame."""
    spec = p.get("specLine") or ""
    garage = re.search(r"(Ext\.\s*)?(\d+(?:\.\d+)?)\s*Car Garage", spec)
    chips = []
    if p.get("bedrooms"):
        chips.append('<span class="chip">%s%s Bed</span>' % (img(ICON_BED, "", "chip-icon"), num(p["bedrooms"])))
    if p.get("bathrooms"):
        chips.append('<span class="chip">%s%s Bath</span>' % (img(ICON_BATH, "", "chip-icon"), num(p["bathrooms"])))
    if "hobby" in spec.lower():
        chips.append('<span class="chip">%sHobby</span>' % ICON_HOBBY)
    if garage:
        chips.append('<span class="chip">%s%s%s Car Garage</span>' % (img(ICON_GARAGE, "", "chip-icon"), "Ext. " if garage.group(1) else "", garage.group(2)))
    return '<div class="chips pd-chips">%s</div>' % "".join(chips)


def plan_link_card(q):
    ref = plan_image(q)
    pic = simg(ref, "%s exterior rendering" % q["name"], 760, sizes="(max-width: 860px) 100vw, 380px") if ref else ""
    return '<a class="po-card" href="/floor-plans/%s"><span class="po-img">%s</span><span class="po-bar"><span class="po-sqft">%s</span><span class="po-name">%s</span><span class="po-go" aria-hidden="true"></span></span></a>' % (
        q["slug"], pic, q["squareFootage"], esc(q["name"]))


def build_plan(p, i, plans):
    """Floor plan page, built on the OFFICIAL Figma floor plan detail frame (the "Hamlet" version of
    "Homes for Sale Home Detail"): number and big name, gallery, price card with features, floor plan
    drawing card, virtual tour, other floor plans, Founders Club and sales team cards."""
    name = esc(p["name"])
    gallery = p.get("gallery") or []
    refs = [g["asset"] for g in gallery]
    alt = gallery[0].get("alt") if gallery and gallery[0].get("alt") else "%s at SunRiver Firelight" % p["name"]
    main = simg(refs[0], alt, 1400, loading="eager", sizes="(max-width: 860px) 100vw, 667px") if refs else ""
    sqft = "{:,}".format(p["squareFootage"])
    beds, baths = num(p.get("bedrooms")), num(p.get("bathrooms"))
    spec = (p.get("specLine") or "").lower()
    extras = " and a hobby room" if "hobby" in spec else ""
    story = ("The %s offers %s sq ft on one level with %s beds, %s baths%s around a bright great room, "
             "in SunRiver Firelight, SunRiver's newest 55+ Active Adult community." % (p["name"], sqft, beds, baths, extras))
    feats = "".join("<li>%s</li>" % esc(f) for f in (p.get("features") or []))
    features = '<h2 class="pd-feat-title">Standard Luxury Features</h2><ul class="pd-feats">%s</ul>' % feats if feats else ""
    diagram = p.get("planDiagram") or {}
    drawing = ""
    if diagram.get("asset"):
        drawing = '''<div class="pd-plan">
      <h2>The %s Floor Plan</h2>
      <a class="pd-plan-img" href="%s" data-lightbox>%s</a>
    </div>''' % (name, S(diagram["asset"], 2400), simg(diagram["asset"], diagram.get("alt") or "%s floor plan drawing" % p["name"], 940, sizes="(max-width: 860px) 100vw, 470px"))
    tour = ""
    if p.get("matterportId"):
        tour = '''<div class="pd-tour" id="tour">
      <h2>Take a virtual tour</h2>
      <div class="pd-tour-frame"><iframe src="https://my.matterport.com/show/?m=%s" title="%s 3D virtual tour" allow="xr-spatial-tracking; fullscreen" allowfullscreen loading="lazy"></iframe></div>
    </div>''' % (p["matterportId"], name)
    others = [plans[(i + k) % len(plans)] for k in (1, 2, 3) if len(plans) > k]
    add("/floor-plans/%s" % p["slug"], "%s Floor Plan" % p["name"],
        "The %s at SunRiver Firelight: %s sq ft, %s, %s." % (p["name"], sqft, p.get("specLine", ""), p.get("priceRange", "")), "life", '''
<section class="hd pd">
  <div class="wrap">
    <a class="hd-back" href="/floor-plans">See all floor plans</a>
    <p class="pd-num">%s</p>
    <h1 class="pd-title">%s</h1>
    <div class="pd-top">
      <div class="hd-media viewer"><div class="viewer-main">%s</div>%s</div>
      <div class="pd-card">
        <p class="pd-price">%s</p>
        <p class="pd-line"><span>%s ft<sup>2</sup></span><strong>Smart Single-Level Living</strong></p>
        <p class="pd-story">%s</p>
        %s
        %s
        <div class="hd-actions"><a class="hd-btn solid" href="/contact-us">Schedule a Tour</a><a class="hd-btn" href="/contact-us#team">Request Info</a></div>
      </div>
    </div>
    %s
    %s
    <div class="pd-others">
      <h2>Check out other floor plans</h2>
      <div class="pd-others-grid">%s</div>
    </div>
    %s
  </div>
</section>''' % (p["squareFootage"], name, main, thumbs_html(refs, alt), esc(p.get("priceRange", "")), sqft, esc(story),
                 plan_chips(p), features, drawing, tour, "".join(plan_link_card(q) for q in others), contact_row()), body_class="sand-page")


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


BADGE_LABEL = {"Move in Ready": "Move-In-Ready"}


def listing_card(l):
    """Homes for sale card, styled like the developers' Vercel build (sunriver-website.vercel.app/homes-for-sale):
    status pill with a dot, plan name and square feet with a yellow underline, address and home number, price, spec chips."""
    photo = simg(l["photo"], l.get("photoAlt") or l.get("title"), 568, sizes="(max-width: 700px) 100vw, 284px") if l.get("photo") else ""
    data = 'data-community="%s" data-status="%s" data-sqft="%s" data-beds="%s" data-baths="%s" data-garage="%s" data-hobby="%s"' % (
        esc(l.get("community", "")), esc(l.get("status", "")), l.get("squareFootage") or 0, l.get("beds") or 0,
        l.get("baths") or 0, l.get("garageSpaces") or 0, l.get("hobbyRooms") or 0)
    st = l.get("status") or ""
    badge = '<span class="home-badge is-%s"><i aria-hidden="true"></i>%s</span>' % (slugify(st), esc(BADGE_LABEL.get(st, st))) if st else ""
    m = re.match(r"\s*Home\s+(\d+)", l.get("address") or "")
    home_no = '<span class="home-no"> | Home %s</span>' % m.group(1) if m else ""
    # a price, or "Ask for pricing"; a home under contract with no price shows none
    price = "" if (st == "Under Contract" and not l.get("price")) else listing_price(l)
    return '''<a class="home-card" href="/homes-for-sale/%s" %s><span class="home-card-in">
  <span class="home-img">%s%s</span>
  <span class="home-body">
    <span class="home-title"><strong>%s</strong><span class="home-sf">%s sf</span></span>
    <span class="home-address">%s%s</span>
    %s
    %s
  </span>
</span></a>''' % (l["slug"], data, photo, badge, esc(clean(l.get("title"))), l.get("squareFootage") or "",
             esc(short_address(l)), home_no, '<span class="home-price">%s</span>' % price if price else "", spec_chips(l))


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
    add("/homes-for-sale", "Homes for Sale", "Move-in ready and available homes at SunRiver Firelight, SunRiver Villas and SunRiver St. George.", "homes-overlay", '''
<section class="fah-hero hfs-hero">%s<div class="wrap fah-hero-inner"><h1>Homes for sale</h1></div></section>
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
</section>''' % (img(FG("hfs-hero"), "Aerial view of SunRiver Firelight with Pine Valley Mountain behind it", "fah-hero-img", "eager"), comm, stat, sqft,
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
    mls = ""
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
    banner = full_hero(img(V("bucketlist-wordmark.3qnr5_89a42b3.png"), "Bucketlist Living", "wordmark", "eager"),
                       "Stories, events and guides from SunRiver Firelight and Southern Utah.", src=V("bucketlist-banner.02if0nz4sgehw.webp"), cls="fh-blog")
    blog_listing(posts, "/bucketlistliving", banner, "", "#bucketlistliving", "Bucketlist Living: stories, events and guides from SunRiver Firelight and Southern Utah.", cats)
    for c in cats:
        cp = [p for p in posts if c in (p.get("categories") or [])]
        blog_listing(cp, "/bucketlistliving/category/%s" % slugify(c), full_hero(esc(c), eyebrow="Category", src=V("bucketlist-banner.02if0nz4sgehw.webp"), cls="fh-blog"), "", "%s | #bucketlistliving" % c,
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


# ================================================================== LIVE IN (OFFICIAL Figma "Live In", work in progress)
# The three flip cards under 04 / The Design Center (1 Choose your plan and lot, 2 See full-size samples,
# 3 Know what it costs) are parked, not deleted: set this to True to bring them back.
SHOW_DC_FLIPS = False


def build_live_in(plans, listings):
    """Live In page from the OFFICIAL Figma "Live In" frame: photo hero, intro, the floor plans,
    a yellow visit band, homes ready now, and the available lots section (lot map to come)."""
    cards = []
    for p in plans[:4]:  # the design shows four plans, then a See all floor plans button
        cards.append(plan_link_card(p))
    rows = "".join('<div class="li-plan-row%s">%s</div>' % (" shift" if r % 2 else "", "".join(cards[r * 2:r * 2 + 2]))
                   for r in range((len(cards) + 1) // 2))
    ready = sorted([l for l in listings if l.get("status") in ("Move in Ready", "For Sale")], key=listing_sort_key)[:6]
    sizes = sorted(p["squareFootage"] for p in plans)
    # 04 / The Design Center: three cards that flip on hover (or tap) to a photo
    steps = [("1", "Choose your plan and lot", "Start with the footprint and place you want to call home.",
              FG("hfs-hero"), "Aerial view of homesites at SunRiver Firelight"),
             ("2", "See full-size samples", "Cabinetry, countertops, flooring, tile, fixtures, lighting, and paint, with a designer beside you.",
              "/assets/img/design-center-samples.webp", "A SunRiver designer showing full-size countertop samples at the Design Center"),
             ("3", "Know what it costs", "Leave knowing what your home will look like and what each selection costs.",
              S("image-4002cc30c79b533f3eab3b908037c2757c646f0e-2000x1333-jpg", 900), "The finished kitchen in the Astoria model home")]
    flips = "".join('''<div class="li-flip" tabindex="0"><div class="li-flip-in">
      <div class="li-flip-front"><span class="li-flip-num">%s</span><h3>%s</h3><p>%s</p></div>
      <div class="li-flip-back" aria-hidden="true">%s<span>%s</span></div></div></div>''' % (n, t, d, img(src, alt), t) for n, t, d, src, alt in steps)
    add_with_firelight("/live-in", "Live In", "Live In at SunRiver Firelight: seven floor plans, homes ready now and homesites to choose from.", "life-overlay", '''
<section class="fah-hero li-hero">
  %s
  <div class="wrap fah-hero-inner"><h1>Live In</h1></div>
</section>
<section class="li-intro li-lead">
  <div class="wrap li-in">
    <h2>A new home for exactly this stage.</h2>
    <p class="li-serif"><strong><mark>Live In</mark> is the home itself.</strong> Not a smaller version of the house you are leaving. A better fit for the chapter you are starting. Open kitchens, hobby rooms, extended garages, customization throughout. Quality that refuses compromise. Twenty-five years and 2,600 homes taught us what holds up, and everything below is the result.</p>
    <div class="li-btns"><a class="li-btn solid" href="/floor-plans">See floor plans</a><a class="li-btn" href="/contact-us">Schedule a visit</a></div>
  </div>
</section>
<section class="li-plans">
  <div class="wrap li-in">
    <p class="li-eyebrow">01 / Floor plans</p>
    <h2 class="li-title">Seven floor plans. Every one built<br> for how you actually live.</h2>
    <p class="li-copy">Sizes run from {:,} to {:,} square feet, two to three bedrooms, and garages up to an extended three-car. Every plan includes custom-crafted cabinetry, solid-surface countertops, Moen fixtures, GE appliances, structured wiring, hybrid gas and electric heating and cooling, low-E windows, and concrete roof tile. Standard, not upgrades.</p>
    <div class="li-plan-grid">%s</div>
    <div class="li-btns li-plans-more"><a class="li-btn solid" href="/floor-plans">See all floor plans</a></div>
  </div>
</section>
<section class="li-visit">
  <svg class="li-wave" viewBox="0 0 1440 360" preserveAspectRatio="none" aria-hidden="true"><path d="M0 250 C 260 120, 520 120, 760 210 S 1220 300, 1440 160 L1440 360 L0 360 Z" fill="#fff" fill-opacity=".07"/><path d="M0 110 C 300 30, 560 60, 820 140 S 1260 200, 1440 60 L1440 0 L0 0 Z" fill="#fff" fill-opacity=".05"/></svg>
  <div class="wrap li-visit-inner">
    <h2>Come see how it feels.</h2>
    <div class="li-btns center"><a class="li-btn light" href="/contact-us">Schedule a visit</a><a class="li-btn white" href="/homes-for-sale">See homes for sale</a></div>
  </div>
</section>
<section class="li-ready">
  <div class="wrap li-in">
    <p class="li-eyebrow">02 / Homes for sale</p>
    <h2 class="li-title">Homes ready now.</h2>
    <p class="li-copy">Some people want to choose every finish. Some people are ready to move. See the actual house instead of a rendering, and begin living here in weeks rather than months.</p>
    <div class="li-home-grid">%s</div>
    <div class="li-step">
      <h2>Step inside a real home.</h2>
      <p>Ask about availability and the estimated completion date.</p>
      <a class="li-btn solid" href="/contact-us">Schedule a visit</a>
    </div>
  </div>
</section>
<section class="li-lots" id="lots">
  <div class="wrap li-in">
    <p class="li-eyebrow">03 / Available lots</p>
    <h2 class="li-title">Pick your spot.</h2>
    <p class="li-copy">Some homesites back to open desert, some sit higher for the view, and others put you closer to the community center and trailheads. What you can build on each one varies.</p>
  </div>
  <div class="wrap li-in">%s
    <div class="li-walk"><div><h3>Walk the ground.</h3><p>The right location makes more sense in person.</p></div><a class="li-btn solid" href="/contact-us">Meet with an agent</a></div>
  </div>
</section>
<section class="li-dc" id="design-center">
  <div class="wrap li-in">
    <p class="li-eyebrow">04 / The Design Center</p>
    <h2 class="li-title">You are not buying the home.<br> You are building it.</h2>
    <p class="li-copy">Most builders hand you three packages and call it a choice. We hand you a room.</p>
    <div class="li-dc-feature">
      <div class="li-dc-img">%s</div>
      <div class="li-dc-text"><h3>Choices with real life in mind.</h3>
        <p>Where the light lands in the morning. Which counter you will stand at when there are twelve people over. Whether the hobby room is for pottery or a workbench, because those need different outlets.</p>
        <p>The point of the appointment is not to upsell you. It is to make the house match the way you live.</p></div>
    </div>
    %s
    <div class="li-btns"><a class="li-btn solid" href="/design">Explore the Design Center</a></div>
  </div>
</section>'''.format(sizes[0], sizes[-1]).replace("{{", "{").replace("}}", "}") % (
        img(FG("li-hero"), "SunRiver members visiting in a SunRiver Firelight living room", "fah-hero-img", "eager"),
        rows, "".join(listing_card(l) for l in ready), lotmap.svg(plans),
        img(FG("li-bedroom"), "A finished bedroom in a SunRiver Firelight home"),
        '<div class="li-flips" data-anim="fade">%s</div>' % flips if SHOW_DC_FLIPS else ""))


def build_live_out():
    """Live Out page, patterned on the Figma "Live In" page (no Live Out frame yet). Copy from Adam's Live Out doc.
    Drive times marked as estimates in that doc still need verifying."""
    close = [("Quail Creek Reservoir", "8 min"), ("Red Cliffs National Conservation Area", "10 min"),
             ("Sky Mountain Golf Course, Hurricane", "12 min"), ("Sand Hollow State Park", "22 min"),
             ("St. George", "about 30 min"), ("Zion National Park", "31 min"), ("St. George Regional Airport", "36 min")]
    far = [("Zion National Park", "31 min", "/assets/img/lo-zion.webp"),
           ("Utah Shakespeare Festival", "Cedar City, about 50 min", "/assets/img/lo-shakespeare.webp"),
           ("Bryce Canyon", "about 2 hrs", "/assets/img/lo-bryce.webp"),
           ("Grand Canyon North Rim", "about 2.5 hrs", "/assets/img/lo-grand-canyon.webp")]
    also = "Brian Head for snow, about an hour away, so you can see it without living in it. Las Vegas, about 2 hours."
    rows = "".join('<li><span>%s</span><strong>%s</strong></li>' % (esc(a), b) for a, b in close)
    cards = "".join('<div class="lo-card">%s<div class="lo-card-text"><strong>%s</strong><span>%s</span></div></div>' % (
        img(p, t), esc(t), d) for t, d, p in far)
    trails = [("Inside the community", "Trailheads within walking distance of most homesites, so a morning hike starts at your front door."),
              ("Ten minutes out", "Toquerville Falls. Confluence Park. The Virgin River. Quail Creek, where the water is warm by April. Red Cliffs, where the slot canyons and petroglyphs are."),
              ("Twenty to thirty minutes out", "Sand Hollow for boating and side-by-sides. Zion National Park, 31 minutes from your front door.")]
    trail_cols = "".join('<div class="lo-col"><h3>%s</h3><p>%s</p></div>' % (a, b) for a, b in trails)
    nearby = [("Groceries", [("Lin's Marketplace, Hurricane", "15 min"), ("Walmart Supercenter, Hurricane", "15 min"), ("Costco, Washington", "28 min")]),
              ("Healthcare", [("Intermountain Hurricane Valley Clinic and InstaCare", "15 min"), ("St. George Regional Hospital, the region's Level II trauma center", "32 min")]),
              ("Dining", [("River Rock Roasting Company, La Verkin", "4 min"), ("Pigs Ear American Bistro", "10 min"), ("The Hurricane restaurant strip", "15 min")])]
    near_html = "".join('<div class="lo-near"><h3>%s</h3><ul>%s</ul></div>' % (
        c, "".join('<li><span>%s</span><strong>%s</strong></li>' % (esc(a), b) for a, b in items)) for c, items in nearby)
    add_with_firelight("/live-out", "Live Out", "Live Out at SunRiver Firelight: Zion 31 minutes away, 22 miles of trails, and everything you need close by.", "life-overlay", '''
<section class="fah-hero li-hero lo-hero">
  %s
  <div class="wrap fah-hero-inner"><h1>Live Out</h1></div>
</section>
<section class="li-intro li-lead">
  <div class="wrap li-in">
    <h2>Zion is 31 minutes away. That is the point.</h2>
    <p class="li-serif"><strong><mark>Live Out</mark> is everything past the front door.</strong> We built on the Zion side of Southern Utah so the parks, the trails, and the reservoirs are the daily backdrop, not the weekend plan. Three hundred days of sun, a few degrees cooler than St. George, and the trailheads start where the driveway ends. Everything below is within a half hour.</p>
    <div class="li-btns"><a class="li-btn solid" href="#nearby">See what is nearby</a><a class="li-btn" href="/contact-us">Schedule a visit</a></div>
  </div>
</section>
<section class="li-plans lo-region">
  <div class="wrap li-in">
    <p class="li-eyebrow">01 / Southern Utah</p>
    <h2 class="li-title">The landscape is the daily backdrop,<br> not the weekend plan.</h2>
    <p class="li-copy">That is the reason to be on this side of Southern Utah. SunRiver Firelight sits on the Zion side, north of Hurricane, where red rock and open desert are part of every day instead of an occasional outing.</p>
    <div class="lo-region-grid">
      <div class="lo-times"><h3>What is close</h3><ul>%s</ul></div>
      <div class="lo-far"><h3>And farther out</h3><div class="lo-cards">%s</div><p class="lo-also">%s</p></div>
    </div>
    <div class="lo-weather">
      <h3>The weather is the quiet reason people move here.</h3>
      <div class="lo-stats">
        <div><strong>300</strong><span>Days of sunshine, give or take</span></div>
        <div><strong>50s</strong><span>Winter afternoons</span></div>
        <div><strong>500 ft</strong><span>Higher than St. George, so summer runs a few degrees cooler, and it never turns into a place that snows</span></div>
      </div>
    </div>
  </div>
</section>
<section class="li-visit">
  <svg class="li-wave" viewBox="0 0 1440 360" preserveAspectRatio="none" aria-hidden="true"><path d="M0 250 C 260 120, 520 120, 760 210 S 1220 300, 1440 160 L1440 360 L0 360 Z" fill="#fff" fill-opacity=".07"/><path d="M0 110 C 300 30, 560 60, 820 140 S 1260 200, 1440 60 L1440 0 L0 0 Z" fill="#fff" fill-opacity=".05"/></svg>
  <div class="wrap li-visit-inner">
    <h2>Come see it for yourself.</h2>
    <div class="li-btns center"><a class="li-btn light" href="/contact-us">Schedule a visit</a><a class="li-btn white" href="/discovery-villas">Stay a few nights</a></div>
  </div>
</section>
<section class="li-ready lo-trails" id="trails">
  <div class="wrap li-in">
    <p class="li-eyebrow">02 / Trails and adventure</p>
    <h2 class="li-title">The trails start where<br> the driveway ends.</h2>
    <p class="li-copy">Twenty-two miles of trail run through and around SunRiver Firelight. Not a paved loop around a retention pond. Real desert trail, with the kind of grade and view that makes you want to go again tomorrow.</p>
    <div class="lo-cols">%s</div>
  </div>
  <div class="lo-trail-img">%s</div>
</section>
<section class="li-lots lo-nearby" id="nearby">
  <div class="wrap li-in">
    <p class="li-eyebrow">03 / What is nearby</p>
    <h2 class="li-title">Live a little closer.</h2>
    <p class="li-copy">Groceries, healthcare and a good cup of coffee are a short drive from your front door.</p>
    <div class="lo-near-grid">%s</div>
    <div class="li-btns"><a class="li-btn solid" href="/contact-us">Schedule a visit</a></div>
  </div>
</section>''' % (img(V("live-out.2z9c8sf8gogme.jpg"), "SunRiver members hiking in red rock country", "fah-hero-img", "eager"),
                 rows, cards, also, trail_cols, img(FG("fl-trails"), "Trails and red rock mountains around SunRiver Firelight"), near_html))


# ================================================================== LIVE ON (patterned on the Figma "Live In" page, like Live Out)
def build_live_on(posts):
    """Live On page. Copy from Adam's Live On doc, in the brand language from the sales playbook: Members, the Clubhouse,
    future tense for anything not built. Clubs and the calendar schedule live in data/live_on.json (placeholders for now)."""
    import json
    from pathlib import Path
    d = json.loads((Path(__file__).resolve().parent.parent / "data" / "live_on.json").read_text())
    now = "".join('<li><span>%s</span><strong>%s</strong></li>' % (esc(c["name"]), esc(c["when"])) for c in d["running_now"])
    later = "".join('<li><span>%s</span></li>' % esc(c) for c in d["clubhouse_opens"])
    shots = [("Sunrise Stroll", "Monthly, 7:30 AM", V("week-hike.13z6azl5t3od2.jpg")),
             ("Pilates Workshop", "Select Thursdays, 11 AM", V("club-yoga.0jzome1ix55zy.jpg")),
             ("Drop-in Games", "Wednesdays, 2 PM", V("cc-billiards.1qmjemn1vq503.jpg"))]
    shot_html = "".join('<div class="lo-card">%s<div class="lo-card-text"><strong>%s</strong><span>%s</span></div></div>' % (
        img(p, "SunRiver members, %s" % t.lower()), t, w) for t, w, p in shots)
    cal = {"recurring": d["recurring"], "events": [e for e in d["events"] if e.get("date")]}
    cal_json = json.dumps(cal, separators=(",", ":")).replace("</", "<\\/")
    phases = [("Built and open today", ["Five model homes", "Occupied homes in phases one and two", "22 miles of trails",
                                      "The first pickleball courts", "The sales office at 182 Cottonwood Drive"]),
              ("Under construction now", ["The Clubhouse", "The 4,000 square foot pool", "The full pickleball complex",
                                          "Toquerville Parkway, the new bypass with direct I-15 and Zion access"]),
              ("Coming after that", ["Additional phases toward 1,200 homes total", "Additional amenity areas"])]
    phase_html = "".join('<div class="lon-phase"><span class="lon-dot"></span><h3>%s</h3><ul>%s</ul></div>' % (
        h, "".join("<li>%s</li>" % esc(x) for x in items)) for h, items in phases)
    recent = sorted(posts, key=lambda p: p.get("publishDate") or "", reverse=True)[:3]
    posts_html = '<div class="post-grid cols-3 lon-posts">%s</div>' % "".join(post_card(p) for p in recent) if recent else ""
    add_with_firelight("/live-on", "Live On", "Live On at SunRiver Firelight: clubs and activities, the events calendar, what is coming and when, and Bucketlist Living.", "life-overlay", '''
<section class="fah-hero li-hero lon-hero">
  %s
  <div class="wrap fah-hero-inner"><h1>Live On</h1></div>
</section>
<section class="li-intro li-lead">
  <div class="wrap li-in">
    <h2>Nobody acts their age here.</h2>
    <p class="li-serif"><strong><mark>Live On</mark> is everyone you have not met yet.</strong> People move here for the hiking and end up running a club they never meant to join. That is not an accident. We build the calendar, the Clubhouse, and the trails so you keep running into the same people on purpose, until they are your people. Move, connect, grow. The home gets you here. This is why you stay.</p>
    <div class="li-btns"><a class="li-btn solid" href="#calendar">See the calendar</a><a class="li-btn" href="/contact-us">Schedule a visit</a></div>
  </div>
</section>
<section class="li-plans lon-clubs" id="clubs">
  <div class="wrap li-in">
    <p class="li-eyebrow">01 / Clubs and activities</p>
    <h2 class="li-title">Real friendships do not<br> happen by accident.</h2>
    <p class="li-copy">They happen when people keep bumping into each other on purpose, which is what a good calendar is actually for.</p>
    <div class="lo-cards lon-shots">%s</div>
    <div class="lon-lists">
      <div class="lo-times"><h3>What is running now</h3><ul>%s</ul></div>
      <div class="lo-times"><h3>What starts when the Clubhouse opens</h3><ul class="lon-plain">%s</ul></div>
      <div class="lon-own"><h3>And what you start yourself</h3><p>Every club here began because a Member wanted it to exist and asked. There is no committee to petition. Tell a Steward what you want to run and they will help you find your people.</p></div>
    </div>
  </div>
</section>
<section class="li-ready lon-cal" id="calendar">
  <div class="wrap li-in">
    <p class="li-eyebrow">02 / Events calendar</p>
    <h2 class="li-title">What is happening this month.</h2>
    <div class="lon-calendar" data-cal>
      <div class="lon-cal-bar">
        <div class="lon-cal-nav"><button type="button" data-cal-prev aria-label="Previous month"><svg viewBox="0 0 10 16" aria-hidden="true"><path d="M8 2L2 8l6 6"/></svg></button><h3 data-cal-title aria-live="polite"></h3><button type="button" data-cal-next aria-label="Next month"><svg viewBox="0 0 10 16" aria-hidden="true"><path d="M2 2l6 6-6 6"/></svg></button></div>
        <div class="lon-cal-tools">
          <div class="lon-cal-filter" role="group" aria-label="Show"><button type="button" data-f="all" aria-pressed="true">All</button><button type="button" data-f="Clubs" aria-pressed="false">Clubs</button><button type="button" data-f="Events" aria-pressed="false">Events</button><button type="button" data-f="Around town" aria-pressed="false">Around town</button></div>
          <button type="button" class="lon-cal-print" data-cal-print>Print this month</button>
        </div>
      </div>
      <div class="lon-cal-grid" data-cal-grid></div>
      <script type="application/json" class="lon-cal-data">%s</script>
    </div>
    <div class="li-walk lon-guest">
      <div><h3>Not a Member yet?</h3><p>Prospective buyers are welcome at most events. Come see what a Tuesday actually looks like.</p></div>
      <a class="li-btn solid" href="/contact-us">Join us at the next one</a>
    </div>
  </div>
</section>
<section class="li-visit">
  <svg class="li-wave" viewBox="0 0 1440 360" preserveAspectRatio="none" aria-hidden="true"><path d="M0 250 C 260 120, 520 120, 760 210 S 1220 300, 1440 160 L1440 360 L0 360 Z" fill="#fff" fill-opacity=".07"/><path d="M0 110 C 300 30, 560 60, 820 140 S 1260 200, 1440 60 L1440 0 L0 0 Z" fill="#fff" fill-opacity=".05"/></svg>
  <div class="wrap li-visit-inner">
    <h2>Come see what a Tuesday looks like.</h2>
    <div class="li-btns center"><a class="li-btn light" href="/contact-us">Schedule a visit</a><a class="li-btn white" href="/discovery-villas">Stay a few nights</a></div>
  </div>
</section>
<section class="li-lots lon-coming" id="coming">
  <div class="wrap li-in">
    <p class="li-eyebrow">03 / What is coming and when</p>
    <h2 class="li-title">What is built, what is under construction,<br> and when the rest arrives.</h2>
    <p class="li-copy">We build in phases. That means parts of this community are a construction site right now, and we would rather show you the schedule than talk around it.</p>
    <div class="lon-phases">%s</div>
    <p class="lon-updated">Updated the first week of every month, with photographs taken on site and dates that move only when we tell you they moved.</p>
    <div class="lon-honest">
      <div class="lon-honest-img">%s</div>
      <div class="lon-honest-text">
        <h3>Here is the part nobody else will say out loud.</h3>
        <p>If you buy now, you will live through some of the building. You will hear equipment. Some streets will be closed. That is the honest tradeoff.</p>
        <p>Here is the other half of it, learned across twenty-five years and 2,500 homes: the people who buy early become the connectors. They are the ones who know everybody, because they were here when there were only forty of them and there was nothing to do but figure each other out. By the time the amenities open, they already have their people. The Members who arrive later spend a year catching up.</p>
        <p class="lon-kicker">Early is harder. It is also better.</p>
        <a class="li-btn solid" href="/contact-us">Walk the site with the developer</a>
      </div>
    </div>
  </div>
</section>
<section class="li-ready lon-blog" id="bucketlist">
  <div class="wrap li-in">
    <p class="li-eyebrow">04 / Bucketlist Living</p>
    <h2 class="li-title">Stories from the people<br> who live here.</h2>
    <p class="li-copy">The Member who learned to throw pottery at 71. The couple who did all five Utah national parks in a year. Bucketlist Living is where SunRiver Members tell their stories, along with guides to the trails, parks and towns around us.</p>
    %s
    <div class="li-btns"><a class="li-btn solid" href="/bucketlistliving">Read Bucketlist Living</a></div>
  </div>
</section>''' % (img(V("live-on.2kwzvtocledst.jpg"), "SunRiver members playing pool together", "fah-hero-img", "eager"),
                 shot_html, now, later, cal_json, phase_html,
                 simg("00a771c4786df837151167618e14dcacac89a759-2048x1506.webp", "Rendering of the SunRiver Firelight Clubhouse", 1200, sizes="(max-width: 860px) 100vw, 45vw"),
                 posts_html))


# ================================================================== SUNRIVER FIRELIGHT (the live sunriver.com page, rebuilt in the Live In style)
def build_firelight(plans):
    """SunRiver Firelight overview, from the live sunriver.com/sunriver-firelight page with the copy brought in line:
    Members, the Clubhouse, future tense for what is not built, drive times matching Live Out, no golf, and the
    dated items (reservations, summer/fall updates, the invented week of activities) dropped."""
    mix = [("Brand new homes", "Choose your homesite, then design the home that goes on it."),
           ("Outdoor living", "Red rock, open desert and 22 miles of trail run through and around the community."),
           ("Prime location", "On the Zion side of Southern Utah, north of Hurricane, with St. George about 30 minutes away."),
           ("Designed for you", "Hobby rooms, open kitchens and garages up to an extended three-car, with room for the gear you love."),
           ("Mild seasons", "About 500 feet higher than St. George, so summers run a few degrees cooler, without the snow."),
           ("Community", "SunRiver is more than a place to live. It is a community of people who refuse to slow down.")]
    mix_html = "".join('<div class="lo-col"><h3>%s</h3><p>%s</p></div>' % x for x in mix)
    amen = [("The Clubhouse", "The hub for social, recreational and wellness life at SunRiver Firelight, with fitness rooms, event spaces and dedicated rooms for hobbies and clubs.", V("amenity-clubhouse.1s09xtqihpiiw.jpg")),
            ("The pool", "A 4,000 square foot pool for laps, sunning on the deck or a poolside evening with neighbors.", V("amenity-pool.3xoam7a_jzu33.jpg")),
            ("Pickleball", "Courts for players of every level, for daily play, friendly competition and the conversation after the game.", V("amenity-pickleball.2602yc92h05vt.jpg"))]
    amen_html = "".join('<div class="fl-amen-card"><div class="fl-amen-img">%s</div><h3>%s</h3><p>%s</p></div>' % (img(p, "%s at SunRiver Firelight" % t), t, d) for t, d, p in amen)
    clubs = [("Hiking", "Trails from the front door", V("club-hiking.3s1-w8hg6a1nh.jpg")),
             ("Pilates and yoga", "Workshops and classes", V("club-yoga.0jzome1ix55zy.jpg")),
             ("Pickleball", "Play, then stay and talk", V("club-pickleball.3iqae91xix18y.jpg"))]
    club_html = "".join('<div class="lo-card">%s<div class="lo-card-text"><strong>%s</strong><span>%s</span></div></div>' % (
        img(p, "SunRiver members, %s" % t.lower()), t, w) for t, w, p in clubs)
    cards = [plan_link_card(p) for p in plans[:4]]
    rows = "".join('<div class="li-plan-row%s">%s</div>' % (" shift" if r % 2 else "", "".join(cards[r * 2:r * 2 + 2])) for r in range((len(cards) + 1) // 2))
    add("/sunriver-firelight", "SunRiver Firelight", "SunRiver Firelight in Toquerville, Utah: SunRiver's newest 55+ community puts Zion National Park in your backyard.", "life-overlay", '''
<section class="fah-hero li-hero fl-hero">
  %s
  <div class="wrap fah-hero-inner"><h1>SunRiver Firelight</h1></div>
</section>
<section class="li-intro">
  <div class="wrap li-in">
    <h2>Zion in your<br> backyard.</h2>
    <p class="li-serif">SunRiver Firelight is the newest community from SunRiver: single-family homes in Toquerville, with Springdale and Zion National Park close enough for a morning trip. Live a little closer.</p>
    <div class="li-btns"><a class="li-btn solid" href="/contact-us">Talk with an agent</a><a class="li-btn" href="/floor-plans">Explore floor plans</a></div>
  </div>
</section>
<section class="li-plans fl-mix">
  <div class="wrap li-in">
    <p class="li-eyebrow">01 / Just the right mix</p>
    <h2 class="li-title">Everything you came to<br> Southern Utah for.</h2>
    <div class="lo-cols">%s</div>
    <div class="lo-weather">
      <h3>Live a little closer.</h3>
      <div class="lo-stats">
        <div><strong>31 min</strong><span>To Zion National Park</span></div>
        <div><strong>30 min</strong><span>To St. George, give or take</span></div>
        <div><strong>50 min</strong><span>To Cedar City and the Utah Shakespeare Festival</span></div>
      </div>
      <p class="li-copy">Toquerville Parkway, the new bypass now under construction, will run right past SunRiver Firelight with direct access to I-15 and Zion National Park.</p>
    </div>
  </div>
</section>
<section class="li-visit">
  <svg class="li-wave" viewBox="0 0 1440 360" preserveAspectRatio="none" aria-hidden="true"><path d="M0 250 C 260 120, 520 120, 760 210 S 1220 300, 1440 160 L1440 360 L0 360 Z" fill="#fff" fill-opacity=".07"/><path d="M0 110 C 300 30, 560 60, 820 140 S 1260 200, 1440 60 L1440 0 L0 0 Z" fill="#fff" fill-opacity=".05"/></svg>
  <div class="wrap li-visit-inner">
    <h2>Come see it for yourself.</h2>
    <div class="li-btns center"><a class="li-btn light" href="/contact-us">Schedule a visit</a><a class="li-btn white" href="/discovery-villas">Stay a few nights</a></div>
  </div>
</section>
<section class="li-ready fl-amen" id="clubhouse">
  <div class="wrap li-in">
    <p class="li-eyebrow">02 / The Clubhouse</p>
    <h2 class="li-title">The future heart of<br> SunRiver Firelight.</h2>
    <p class="li-copy">Phase 1 of the Clubhouse is under construction now. When it opens, this is where SunRiver members will work out, gather, take a class and start the next club.</p>
    <div class="fl-amen-grid">%s</div>
    <div class="li-btns"><a class="li-btn solid" href="/live-on#coming">See what is coming and when</a><a class="li-btn" href="/amenities-video">Watch the flythrough</a></div>
  </div>
</section>
<section class="li-plans fl-clubs">
  <div class="wrap li-in">
    <p class="li-eyebrow">03 / Clubs and activities</p>
    <h2 class="li-title">So much time.<br> So much to do.</h2>
    <p class="li-copy">Clubs are already meeting at SunRiver Firelight, from the Breakfast Social to Pilates workshops and drop-in games, and every new club starts because a Member asks for it.</p>
    <div class="lo-cards lon-shots">%s</div>
    <div class="li-btns"><a class="li-btn solid" href="/live-on#calendar">See this month&rsquo;s calendar</a><a class="li-btn" href="/live-on">Explore Live On</a></div>
  </div>
</section>
<section class="li-ready fl-homes">
  <div class="wrap li-in">
    <p class="li-eyebrow">04 / Homes</p>
    <h2 class="li-title">Seven floor plans.<br> Your choice of homesite.</h2>
    <p class="li-copy">Pick the plan, pick the lot, then finish it your way at the Design Center. Looking for something sooner? Move-in ready homes are available now.</p>
    <div class="li-plan-grid">%s</div>
    <div class="li-btns li-plans-more"><a class="li-btn solid" href="/floor-plans">See all floor plans</a><a class="li-btn" href="/live-in#lots">Pick your homesite</a><a class="li-btn" href="/homes-for-sale">Homes for sale</a></div>
  </div>
</section>''' % (img(V("hero.2h_vl62bxoy8t.jpg"), "SunRiver members riding e-bikes on a red rock trail near SunRiver Firelight", "fah-hero-img", "eager"),
                   mix_html, amen_html, club_html, rows))


# A card on each Live In / Out / On page pointing to the SunRiver Firelight overview
FL_PROMO = {
    "/live-in": ("Every home here is part of something bigger.",
                 "The plans, the lots and the Design Center all belong to SunRiver Firelight, SunRiver's newest 55+ community in Toquerville, with the Clubhouse on the way and Zion 31 minutes from your front door.",
                 V("homesites-aerial.0o-k9ic3-z5oy.jpg"), "Aerial view of homesites at SunRiver Firelight"),
    "/live-out": ("Home base for all of it.",
                  "SunRiver Firelight sits on the Zion side of Southern Utah, in Toquerville. See the whole community: the homes, the Clubhouse, and why we built here.",
                  V("hero.2h_vl62bxoy8t.jpg"), "SunRiver members riding e-bikes on a red rock trail near SunRiver Firelight"),
    "/live-on": ("Where all of this happens.",
                 "The clubs, the calendar and the future Clubhouse are all part of SunRiver Firelight, SunRiver's newest 55+ community in Toquerville. See the whole picture.",
                 V("clubhouse-rendering.1ka003naw87xl.jpg"), "Rendering of the SunRiver Firelight Clubhouse"),
}


def add_with_firelight(path, title, description, active, body, body_class=""):
    h, t, src, alt = FL_PROMO[path]
    promo = """
<section class="fl-promo-wrap">
  <div class="wrap li-in">
    <a class="fl-promo" href="/sunriver-firelight">
      <span class="fl-promo-img">%s</span>
      <span class="fl-promo-text">
        <span class="li-eyebrow">SunRiver Firelight</span>
        <span class="fl-promo-h">%s</span>
        <span class="fl-promo-p">%s</span>
        <span class="li-btn solid">Explore SunRiver Firelight</span>
      </span>
    </a>
  </div>
</section>""" % (img(src, alt), h, t)
    add(path, title, description, active, body + promo, body_class)


# ================================================================== DESIGN CENTER (patterned on tripointehomes.com/design-studio, in SunRiver style)
def build_design():
    """The Design Center page, linked from Live In 04. Layout follows Tri Pointe's Design Studio page: photo hero,
    a centered intro, a step-by-step timeline that fills in as you scroll, a dark band, finish categories with tabs,
    what comes standard, questions, and a closing photo band. Copy stays with facts already on the site."""
    K = lambda ref, w=1600: S(ref, w)
    kitchen = "image-4002cc30c79b533f3eab3b908037c2757c646f0e-2000x1333-jpg"
    living = "image-312860ee44f51f22356dcb88f7516b1e9c385b8b-2000x1335-jpg"
    dining = "image-6a1e318870d5ce3c3d850bca703c8a60ca608e64-1334x2000-jpg"
    bedroom = "image-50a51a4be0e76165502af30a2ded5523cc7bee18-2000x1334-jpg"
    exterior = "image-e4478eff78151d8dd145c3ac5fe16468329ce8ff-2000x1334-jpg"
    samples = "/assets/img/design-center-samples.webp"
    steps = [("Choose your plan and homesite", "Start with the footprint and the place you want to call home. Once your plan and lot are set, your Design Center journey begins.", None),
             ("Come prepared", "Bring photos of rooms you love, measurements of the furniture you are keeping, and a sense of how you actually live. Where the light lands in the morning. Whether the hobby room is for pottery or a workbench, because those need different outlets.", None),
             ("Sit down with a designer", "At the Design Center, a SunRiver designer sits beside you with full-size samples of cabinetry, countertops, flooring, tile, fixtures, lighting and paint.", None),
             ("Narrow it down", "See real combinations side by side, compare, and make confident choices about the rooms you will use every day.", None),
             ("Know what it costs", "Leave knowing what your home will look like and what each selection costs. No guesswork, no surprises at closing.", samples)]
    tl = []
    for i, (t, d, pic) in enumerate(steps, 1):
        if pic:
            tl.append('<li class="dz-step dz-step-card"><div class="dz-card">%s<div class="dz-card-text"><span class="dz-num">%d</span><h3>%s</h3><p>%s</p></div></div></li>' % (
                img(pic, "A SunRiver designer showing full-size countertop samples at the Design Center"), i, t, d))
        else:
            tl.append('<li class="dz-step%s"><span class="dz-num">%d</span><div class="dz-step-text"><h3>%s</h3><p>%s</p></div></li>' % (" is-left" if i % 2 == 0 else "", i, t, d))
    cats = [("Cabinetry", "Door styles, finishes and hardware for the kitchen, baths and the hobby room.", K(kitchen), "The kitchen in the Astoria model home"),
            ("Countertops", "Full-size slabs and samples, so you see the real pattern and not a two-inch chip.", FG("nav-kitchen"), "A couple cooking together in a SunRiver Firelight kitchen"),
            ("Flooring", "Wood-look, carpet and tile, chosen room by room for how each space gets used.", K(living), "The living room in the Astoria model home"),
            ("Tile and fixtures", "Backsplashes, shower tile and the fixtures that go with them.", samples, "Full-size samples at the SunRiver Design Center"),
            ("Lighting", "Pendants, chandeliers and the fixtures that set the mood of a room.", K(dining, 1200), "The dining room in the Astoria model home"),
            ("Paint", "Wall colors and trim that tie every room together.", K(bedroom), "A bedroom in the Astoria model home")]
    tabs = "".join('<button type="button" role="tab" aria-selected="%s" data-i="%d">%s</button>' % ("true" if i == 0 else "false", i, t) for i, (t, _, _, _) in enumerate(cats))
    panes = "".join('<figure class="dz-pane%s" data-i="%d">%s<figcaption><strong>%s</strong>%s</figcaption></figure>' % (
        " is-on" if i == 0 else "", i, img(src, alt), t, d) for i, (t, d, src, alt) in enumerate(cats))
    standard = ["Custom-crafted cabinetry", "Solid-surface countertops", "Moen fixtures", "GE appliances", "Structured wiring",
                "Hybrid gas and electric heating and cooling", "Low-E windows", "Concrete roof tile"]
    std = "".join("<li>%s</li>" % x for x in standard)
    qa = [("What comes standard in my home?", "Every plan includes custom-crafted cabinetry, solid-surface countertops, Moen fixtures, GE appliances, structured wiring, hybrid gas and electric heating and cooling, low-E windows and concrete roof tile. Standard, not upgrades."),
          ("When does the design process start?", "Once you have chosen your floor plan and homesite. Your agent will help you set up time at the Design Center."),
          ("Can I prepare ahead of time?", "Yes, and it helps. Bring photos of rooms you love, measurements of furniture you are keeping, and notes on how you use each space."),
          ("Will someone try to upsell me?", "No. The point of the appointment is not to upsell you. It is to make the house match the way you live."),
          ("How much do options cost?", "It depends on the plan and the selections you make. You leave knowing what each selection costs, before anything is final."),
          ("Can I see finished homes first?", "Yes. Five of the seven floor plans are open as model homes, and move-in ready homes are available to walk through.")]
    faq_html = "".join('<details class="faq dz-faq"><summary>%s</summary><div class="answer"><p>%s</p></div></details>' % x for x in qa)
    add("/design", "The Design Center", "The SunRiver Design Center: choose finishes with a designer beside you, see full-size samples, and leave knowing what each selection costs.", "life-overlay", """
<section class="fah-hero li-hero dz-hero">
  %s
  <div class="wrap fah-hero-inner"><h1>The Design Center</h1></div>
</section>
<section class="dz-intro">
  <div class="wrap">
    <h2>Where your home<br> becomes yours.</h2>
    <p>You are not buying the home. You are building it. Most builders hand you three packages and call it a choice. We hand you a room, full-size samples, and a designer who wants to know how you actually live. This is where the floor plan you picked turns into the home you will come back to every day.</p>
  </div>
</section>
<section class="dz-process" id="process">
  <div class="wrap">
    <p class="li-eyebrow center">01 / How it works</p>
    <h2 class="dz-h2">Five steps from floor plan<br> to finished home.</h2>
    <ol class="dz-timeline" data-timeline><li class="dz-line" aria-hidden="true"><span class="dz-line-fill"></span></li>%s</ol>
  </div>
</section>
<section class="dz-band">
  <div class="wrap">
    <h2>Clarity, not a sales pitch.</h2>
    <p>Feeling clear and confident matters more than any single finish. Your designer will show you what comes standard, what each option adds, and how every choice fits your life and your budget. The point of the appointment is not to upsell you. It is to make the house match the way you live.</p>
  </div>
</section>
<div class="dz-wide">%s</div>
<section class="dz-style">
  <div class="wrap">
    <p class="li-eyebrow center">02 / Your style, your choice</p>
    <h2 class="dz-h2 light">Every finish, full size.</h2>
    <p class="dz-sub">Browse the categories you will choose from at the Design Center, then come in and see them in person.</p>
    <div class="dz-tabs" role="tablist" aria-label="Finish categories">%s</div>
    <div class="dz-panes" data-dz-panes>%s</div>
  </div>
</section>
<section class="dz-standard">
  <div class="wrap dz-split">
    <div class="dz-split-text">
      <p class="li-eyebrow">03 / Standard, not upgrades</p>
      <h2 class="dz-h2 left">The good stuff<br> comes included.</h2>
      <p>Every SunRiver Firelight plan starts with a list most builders call upgrades. Your Design Center appointment builds from there.</p>
      <ul class="dz-std">%s</ul>
      <div class="li-btns"><a class="li-btn solid" href="/floor-plans">See the floor plans</a></div>
    </div>
    <div class="dz-split-img">%s</div>
  </div>
</section>
<section class="dz-faqs">
  <div class="wrap">
    <h2 class="dz-h2">Your questions, answered.</h2>
    <div class="dz-faq-list">%s</div>
  </div>
</section>
<section class="dz-cta">
  %s
  <div class="wrap dz-cta-inner">
    <h2>Your home is waiting.</h2>
    <div class="li-btns center"><a class="li-btn white" href="/contact-us">Schedule a visit</a><a class="li-btn light" href="/homes-for-sale">See homes for sale</a></div>
  </div>
</section>
<section class="dz-note"><div class="wrap"><p>Availability and selections vary by floor plan and construction stage. Your designer will guide you to the options that fit.</p></div></section>""" % (
        img(K(kitchen, 2400), "The kitchen in the Astoria model home at SunRiver Firelight", "fah-hero-img", "eager"),
        "".join(tl), img(K(living, 2400), "The living room in the Astoria model home"), tabs, panes, std,
        img(K(bedroom), "A bedroom in the Astoria model home"), faq_html,
        img(K(exterior, 2400), "The Astoria model home at SunRiver Firelight", "dz-cta-img")))
