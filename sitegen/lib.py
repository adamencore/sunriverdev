"""Shared building blocks for the SunRiver static site.

Pages are rendered into the PAGES dict ({url path: html}) and written by build.py.
Image helpers:
  V(name)   a file from the dev site's /_next/static/media folder (mirrored into /media/v at build time)
  VP(path)  any other public file on the dev site, e.g. /images/icons/bed.png (also mirrored)
  S(ref)    a Sanity CMS image, hotlinked from cdn.sanity.io
  SQ(path)  an image on the current sunriver.com Squarespace CDN
"""
import hashlib
import html
import re
from pathlib import Path
from datetime import datetime, timedelta

VERCEL = "https://sunriver-website.vercel.app"
SANITY_CDN = "https://cdn.sanity.io/images/ib6s13lu/production/"
SQUARESPACE = "https://images.squarespace-cdn.com/content/v1/65e0b11913912d2c2162c71b/"
SITE_NAME = "SunRiver Firelight"
PHONE = "(435) 688-1000"
PHONE_TEL = "tel:+14356881000"

MIRROR = {}   # local path -> remote url
_ASSETS = Path(__file__).resolve().parent.parent / "assets"


def asset_v(name):
    """Content hash for cache busting, so browsers pick up new CSS and JS right after a deploy."""
    return hashlib.md5((_ASSETS / name).read_bytes()).hexdigest()[:10]

PAGES = {}    # url path ("/", "/about", ...) -> html


def esc(s):
    return html.escape("" if s is None else str(s), quote=True)


def clean(s):
    """Brand rule: no em dashes anywhere in published copy (CMS text included)."""
    if s is None:
        return ""
    s = str(s)
    s = re.sub(r"\s*—\s*", " - ", s)
    return s


def mirror(remote_path):
    local = "/media/v/" + remote_path.lstrip("/").replace("_next/static/media/", "")
    MIRROR[local] = VERCEL + remote_path
    return local


def V(name):
    return mirror("/_next/static/media/" + name)


def VP(path):
    return mirror(path)


def SQ(path):
    return SQUARESPACE + path


def sanity_id(ref):
    """'image-<hash>-WxH-ext' or '<hash>-WxH.ext' -> ('<hash>-WxH.ext', W, H)."""
    r = ref[6:] if ref.startswith("image-") else ref
    if "." not in r:
        base, ext = r.rsplit("-", 1)
        r = base + "." + ext
    m = re.search(r"-(\d+)x(\d+)\.", r)
    w, h = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    return r, w, h


def S(ref, w=None):
    fid, ow, _ = sanity_id(ref)
    url = SANITY_CDN + fid
    if fid.endswith(".svg"):
        return url
    q = ["auto=format", "fit=max", "q=80"]
    if w:
        q.append("w=%d" % min(w, ow or w))
    return url + "?" + "&".join(q)


def img(src, alt="", cls="", loading="lazy", attrs=""):
    c = ' class="%s"' % cls if cls else ""
    a = (" " + attrs) if attrs else ""
    return '<img src="%s" alt="%s"%s loading="%s" decoding="async"%s>' % (src, esc(alt), c, loading, a)


def simg(ref, alt="", w=1200, cls="", loading="lazy", sizes="100vw"):
    """Responsive Sanity image with a small srcset."""
    _, ow, oh = sanity_id(ref)
    widths = sorted(set(x for x in (w // 2, w, w * 2) if not ow or x <= ow) or {ow})
    srcset = ", ".join("%s %dw" % (S(ref, x), x) for x in widths)
    dims = ' width="%d" height="%d"' % (ow, oh) if ow and oh else ""
    return img(S(ref, w), alt, cls, loading, 'srcset="%s" sizes="%s"%s' % (srcset, sizes, dims))


def photo(src, alt="", ratio="ratio-43", extra=""):
    return '<div class="photo %s %s">%s</div>' % (ratio, extra, img(src, alt))


def btn(label, href, kind=""):
    return '<a class="btn %s" href="%s">%s</a>' % (kind, href, label)


def money(v):
    if v is None:
        return ""
    return "${:,.0f}".format(round(float(v)))


def nice_date(iso):
    if not iso:
        return ""
    d = datetime.strptime(iso[:19], "%Y-%m-%dT%H:%M:%S") if "T" in iso else datetime.strptime(iso[:10], "%Y-%m-%d")
    if "T" in iso:
        d = d - timedelta(hours=6)   # Mountain time
    return "%s %d, %d" % (d.strftime("%B"), d.day, d.year)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower().replace("&", "")).strip("-")


# ------------------------------------------------------------------ chrome
LOGO = VP("/images/sr-communities-logo.svg")
FOOTER_BG = V("footer-rocks.16z_pgs-5dzer.jpg")

LIFE = [
    ("Live In", "/live-in", "Floor Plans. The Design Center. How We Build.", V("live-in.0-iialxva3p9u.jpg"), "Couple relaxing in a SunRiver Firelight home"),
    ("Live Out", "/live-out", "Southern Utah. Trails and Nearby Adventure.", V("live-out.2z9c8sf8gogme.jpg"), "SunRiver members hiking in red rock country"),
    ("Live On", "/live-on", "Clubs and Activities. Events Calendar. Bucketlist.", V("live-on.2kwzvtocledst.jpg"), "SunRiver members enjoying a club activity"),
]
NAV = [("homes", "Homes", "/homes-for-sale"), ("about", "About", "/about"), ("visit", "Visit", "/contact-us")]


def overlay_header():
    """Homepage header from Figma "Home Clark Life NAV 4": logo over the hero, translucent pill nav,
    and a light blue Life at SunRiver dropdown with a photo."""
    from .figma_assets import FG
    items = "".join('<li><a href="%s">%s</a></li>' % (h, t) for t, h, _, _, _ in LIFE)
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="site-header overlay" data-menu="closed">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="SunRiver Communities home">%s</a>
    <button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="main-nav pill-nav" aria-label="Main">
      <div class="nav-item" data-open="false"><button class="nav-link" type="button" aria-expanded="false" aria-controls="life-menu">Life at SunRiver<span class="chev" aria-hidden="true"></span></button>
        <div class="pill-drop" id="life-menu"><ul>%s</ul><a class="pill-drop-photo" href="/live-in" tabindex="-1" aria-hidden="true">%s</a></div></div>
      <div class="nav-item"><a class="nav-link" href="/homes-for-sale">Homes</a></div>
      <div class="nav-item"><a class="nav-link" href="/about">About</a></div>
      <div class="nav-item"><a class="nav-link" href="/contact-us">Contact</a></div>
      <a class="pill-cta" href="/sunriver-firelight">Visit</a>
    </nav>
  </div>
</header>''' % (img(LOGO, "SunRiver Communities", loading="eager"), items, img(FG("nav-photo"), "SunRiver members at a SunRiver Villas home"))


def header(active):
    if active == "home-overlay":
        return overlay_header()
    cards = "".join(
        '<a class="mega-card" href="%s"><span class="mega-photo">%s</span><span class="mega-tag">%s</span><span class="mega-sub">%s</span></a>'
        % (href, img(src, alt), t, sub) for t, href, sub, src, alt in LIFE)
    cur = ' aria-current="page"' if active == "life" else ""
    life = ('<div class="nav-item" data-open="false"><button class="nav-link" type="button" aria-expanded="false" aria-controls="life-menu"%s>'
            'Life at SunRiver<span class="chev" aria-hidden="true"></span></button>'
            '<div class="mega" id="life-menu"><div class="wrap mega-cards">%s</div></div></div>') % (cur, cards)
    links = "".join('<div class="nav-item"><a class="nav-link" href="%s"%s>%s</a></div>'
                    % (h, ' aria-current="page"' if k == active else "", t) for k, t, h in NAV)
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="site-header" data-menu="closed">
  <a class="founders-tab" href="/founders-club">Join The Founders Club</a>
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="SunRiver Communities home">%s</a>
    <button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="main-nav" aria-label="Main">%s%s<a class="btn nav-cta" href="/contact-us">Contact Us</a></nav>
  </div>
</header>''' % (img(LOGO, "SunRiver Communities", loading="eager"), life, links)


SOCIAL = '''<div class="social">
  <a href="https://facebook.com/sunriver" aria-label="SunRiver on Facebook"><svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.3V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6H14z"/></svg></a>
  <a href="https://instagram.com/sunriver_communities/" aria-label="SunRiver on Instagram"><svg viewBox="0 0 24 24"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM12 2.5c-2.6 0-2.9 0-3.9.1C4.6 2.7 2.7 4.6 2.6 8.1 2.5 9.1 2.5 9.4 2.5 12s0 2.9.1 3.9c.1 3.5 2 5.4 5.5 5.5 1 .1 1.3.1 3.9.1s2.9 0 3.9-.1c3.5-.1 5.4-2 5.5-5.5.1-1 .1-1.3.1-3.9s0-2.9-.1-3.9c-.1-3.5-2-5.4-5.5-5.5-1-.1-1.3-.1-3.9-.1zm0 1.7c2.5 0 2.8 0 3.8.1 2.6.1 3.8 1.3 3.9 3.9.1 1 .1 1.3.1 3.8s0 2.8-.1 3.8c-.1 2.6-1.3 3.8-3.9 3.9-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-2.6-.1-3.8-1.3-3.9-3.9-.1-1-.1-1.3-.1-3.8s0-2.8.1-3.8C4.3 5.5 5.5 4.3 8.2 4.3c1-.1 1.3-.1 3.8-.1z"/></svg></a>
  <a href="https://www.youtube.com/@sunriver_communities" aria-label="SunRiver on YouTube"><svg viewBox="0 0 24 24"><path d="M23 7.2s-.2-1.6-.9-2.3c-.9-.9-1.9-.9-2.3-1C16.6 3.6 12 3.6 12 3.6s-4.6 0-7.8.3c-.4.1-1.4.1-2.3 1C1.2 5.6 1 7.2 1 7.2S.8 9.1.8 11v1.8c0 1.9.2 3.8.2 3.8s.2 1.6.9 2.3c.9.9 2 .9 2.6 1 1.8.2 7.5.2 7.5.2s4.6 0 7.8-.3c.4-.1 1.4-.1 2.3-1 .7-.7.9-2.3.9-2.3s.2-1.9.2-3.8V11c0-1.9-.2-3.8-.2-3.8zM9.7 15.1V8.5l6 3.3-6 3.3z"/></svg></a>
</div>'''

FOOTER_COLS = [
    ("Company", [("Why SunRiver?", "/why-sunriver"), ("About", "/about"), ("Southern Utah", "/southern-utah"), ("FAQ", "/faq"), ("History", "/history")]),
    ("Find a Home", [("Homes for Sale", "/homes-for-sale"), ("Mortgage Options", "/no-mortgage-payments-for-life"), ("Energy Efficient Homes", "/energy"), ("Floor Plans", "/floor-plans")]),
    ("Communities", [("SunRiver St. George", "/st-george"), ("SunRiver Firelight", "/sunriver-firelight"), ("SunRiver Villas", "/villas")]),
    ("Get in Touch", [("Contact Us", "/contact-us"), ("Bucketlistliving Blog", "/bucketlistliving"), ("SunRiverToday.com", "https://www.sunrivertoday.com/"),
                      ("SRvillasToday.com", "https://www.srvillastoday.com/"), ("Privacy Policy", "/privacy-policy")]),
]


def footer():
    cols = "".join('<div class="footer-col"><h2>%s</h2><ul>%s</ul></div>' % (
        t, "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="italic"' if l == "Privacy Policy" else "", l) for l, h in links))
        for t, links in FOOTER_COLS)
    return '''<footer class="site-footer">
  %s
  <div class="wrap">
    %s
    <div class="footer-grid">
      <div class="footer-brand">%s<p>182 Cottonwood Dr<br>Toquerville, UT 84737</p><p><a href="%s">Sales Office: %s</a></p></div>
      %s
    </div>
    <p class="copyright">SunRiver Firelight &copy; 2026 All Rights Reserved</p>
  </div>
</footer>''' % (img(FOOTER_BG, "", "footer-bg"), SOCIAL, img(LOGO, "SunRiver Communities"), PHONE_TEL, PHONE, cols)


FONTS = '''<style>
@font-face{font-family:"ABC Ginto";src:url("%s") format("opentype");font-weight:500;font-style:normal;font-display:swap}
@font-face{font-family:"ABC Ginto";src:url("%s") format("opentype");font-weight:900;font-style:normal;font-display:swap}
@font-face{font-family:"Tiempos Text";src:url("%s") format("opentype");font-weight:500;font-style:normal;font-display:swap}
</style>''' % (V("ABCGintoMedium-s.p.1gnfcs1mxia21.otf"), V("ABCGintoBlack-s.p.06eqbvszkm88h.otf"), V("TiemposTextMedium-s.p.1nnfz5h4rihgs.otf"))


def add(path, title, description, active, body, body_class=""):
    full_title = title if SITE_NAME in title else "%s | %s" % (title, SITE_NAME)
    doc = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.sanity.io">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@500;700;900&family=Source+Serif+4:opsz,wght@8..60,500&display=swap">
%s
<link rel="stylesheet" href="/assets/styles.css?v=%s">
</head>
<body%s>
%s
<main id="main">
%s
</main>
%s
<script src="/assets/site.js?v=%s" defer></script>
</body>
</html>
''' % (esc(full_title), esc(description), esc(full_title), esc(description), FONTS, asset_v("styles.css"),
       ' class="%s"' % body_class if body_class else "", header(active), body, footer(), asset_v("site.js"))
    assert "—" not in doc, "em dash found on %s" % path
    PAGES[path] = doc


# ------------------------------------------------------------------ components
def chat_section(title="Ready to Chat?", intro="Ready to take the next step and speak with an agent about your next home? Fill out the form below and we'll reach out as soon as possible.", fid="chat"):
    return '''<section class="section yellow-bg chat" id="%(fid)s" aria-labelledby="%(fid)s-title">
  <div class="wrap">
    <h2 id="%(fid)s-title">%(title)s</h2>
    <hr class="rule">
    <p>%(intro)s</p>
    <form class="chat-form" data-demo novalidate>
      <div class="row">
        <div><label for="%(fid)s-first">First Name</label><input id="%(fid)s-first" name="firstname" type="text" autocomplete="given-name" required></div>
        <div><label for="%(fid)s-last">Last Name</label><input id="%(fid)s-last" name="lastname" type="text" autocomplete="family-name" required></div>
      </div>
      <div class="row">
        <div><label for="%(fid)s-email">Email Address</label><input id="%(fid)s-email" name="email" type="email" autocomplete="email" required></div>
        <div><label for="%(fid)s-phone">Phone</label><input id="%(fid)s-phone" name="phone" type="tel" autocomplete="tel"></div>
      </div>
      <fieldset><legend>What are you interested in?</legend>
        <div class="checks">
          <label><input type="checkbox" name="interest" value="agent">Speak With A SunRiver Agent</label>
          <label><input type="checkbox" name="interest" value="availability">Availability Info</label>
          <label><input type="checkbox" name="interest" value="firelight">Learn More About SunRiver Firelight</label>
          <label><input type="checkbox" name="interest" value="financing">Financing Options</label>
          <label><input type="checkbox" name="interest" value="other">Something Else</label>
        </div>
      </fieldset>
      <p class="consent">By clicking "Submit", I authorize SunRiver to contact me about this request via the contact information I provide. I understand calls or texts may use automated technology. I can opt out at any time on the SunRiver website or by unsubscribing. This consent is not required to complete my request.</p>
      <button class="btn sand-btn" type="submit">Submit</button>
      <p class="form-note" hidden></p>
    </form>
  </div>
</section>''' % dict(fid=fid, title=title, intro=intro)


def sand_hero(eyebrow, title, sub="", tag="h1"):
    e = '<p class="eyebrow">%s</p>' % eyebrow if eyebrow else ""
    s = '<p class="sand-hero-sub">%s</p>' % sub if sub else ""
    return '<section class="sand-hero"><div class="wrap">%s<%s>%s</%s>%s</div></section>' % (e, tag, title, tag, s)


ABOUT_TABS = [("About Us", "/about"), ("History", "/history"), ("FAQ", "/faq"), ("Southern Utah", "/southern-utah")]


def yellow_hero(title_html, current):
    tabs = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == current else "", t) for t, h in ABOUT_TABS)
    return ('<section class="yellow-hero"><div class="wrap"><h1>%s</h1></div></section>'
            '<nav class="tabbar" aria-label="About SunRiver"><ul>%s</ul></nav>') % (title_html, tabs)


def photo_hero(eyebrow, title, sub, src, alt, cta=None):
    b = '<div class="btn-row">%s</div>' % cta if cta else ""
    e = '<p class="eyebrow">%s</p>' % eyebrow if eyebrow else ""
    return '''<section class="photo-hero">%s
  <div class="wrap">%s<h1>%s</h1><hr class="rule">%s%s</div></section>''' % (img(src, alt, loading="eager"), e, title, "<p>%s</p>" % sub if sub else "", b)


def banner(text_html, src, cta=None, tall=False, tag="h2"):
    return '<section class="banner%s">%s<div class="wrap"><%s>%s</%s>%s</div></section>' % (
        " tall" if tall else "", img(src, ""), tag, text_html, tag, cta or "")


def band(src, alt="", height="clamp(220px, 32vw, 460px)"):
    return '<div class="band" style="height:%s">%s</div>' % (height, img(src, alt))


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"


def star_list(items, cls=""):
    return '<ul class="star-list %s">%s</ul>' % (cls, "".join("<li>%s</li>" % i for i in items))


def faq(q, a):
    return '<details class="faq"><summary>%s</summary><div class="answer">%s</div></details>' % (q, a)


FOUNDERS_BADGE = V("founders-badge.164umvg6w-3uo.png")
