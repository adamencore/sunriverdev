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
# Header logo, inline so its colors can adapt to whatever it sits on (see site.js)
LOGO_SVG = '<svg class="logo-svg" viewBox="0 0 337.36 125.66" aria-hidden="true" focusable="false"><g><g><path class="lg-word" d="M37.62,78.51v-13.13c4.45,3.11,10.94,5.44,16.66,5.44,3.95,0,5.65-1.27,5.65-3.74,0-1.55-.78-2.68-3.25-3.6l-6.42-1.91c-9.11-2.75-12.85-7.27-12.85-14.61,0-10.02,7.27-16.02,19.62-16.02,6.07,0,11.65,1.55,16.8,4.09v12.85c-4.73-2.82-10.02-4.45-14.89-4.45-4.09,0-5.86,1.06-5.86,3.11,0,1.62,1.27,2.61,3.81,3.39l5.22,1.41c9.88,2.61,14.33,7.41,14.33,15.39,0,10.38-7.48,16.66-20.33,16.66-6.28,0-12.56-1.55-18.49-4.87"/><path class="lg-word" d="M116.95,45.97v35.93h-13.83v-5.36c-1.84,3.53-5.79,6.42-10.87,6.42-8.89,0-12.85-6-12.85-14.82v-22.16h14.19v19.27c0,3.81,1.2,6.14,4.45,6.14s4.73-2.47,4.73-6.56v-18.85h14.19Z"/><path class="lg-word" d="M159.02,59.31v22.59h-14.19v-19.34c0-3.6-1.2-5.93-4.45-5.93s-4.8,2.54-4.8,6.14v19.13h-14.19v-35.93h13.9v5.08c1.77-3.39,5.44-6.14,11.08-6.14,7.91,0,12.63,5.36,12.63,14.4"/><path class="lg-word" d="M184,55.78c4.52,0,6.78-2.19,6.78-5.86s-2.12-5.44-6.07-5.44h-5.93v11.29h5.22ZM190.84,81.9l-12.07-19.06v19.06h-14.54v-49.41h23.15c11.58,0,19.06,5.72,19.06,15.88,0,7.06-3.67,12.49-11.51,14.12l12.92,19.41h-17.01Z"/><path class="lg-word" d="M211.1,45.97h14.19v35.93h-14.19v-35.93ZM210.67,36.3c0-4.02,2.96-6.78,7.48-6.78s7.41,2.75,7.41,6.78c0,4.24-3.11,6.92-7.41,6.92s-7.48-2.68-7.48-6.92"/><path class="lg-word" d="M282.94,60.44h11.79c-.21-3.53-2.26-5.36-5.72-5.36s-5.72,1.98-6.07,5.36M306.45,67.64h-23.29c1.48,2.89,5.08,4.8,11.15,4.8,3.95,0,7.55-.99,10.52-2.75v9.39c-2.75,2.05-7.62,3.88-14.4,3.88-13.48,0-21.81-7.41-21.81-19.2s7.84-18.85,19.83-18.85,18,6.35,18,18.14v4.59Z"/><path class="lg-word" d="M337.36,46.61v12.92c-1.2-.71-3.11-1.34-5.72-1.34-5.22,0-7.98,3.11-7.98,9.18v14.54h-14.19v-35.93h14.19v7.62c1.62-6.21,4.94-8.26,9.17-8.26,2.05,0,3.53.64,4.52,1.27"/><path class="lg-accent" d="M10.33,88.8l-1.32-.32.81,1.09s3.76,4.94,9.66,1.08c1.52-.99,2.62-2.6,3.68-4.15,1.04-1.52,2.03-2.96,3.35-3.83,1.81-1.18,3.46-.81,3.53-.79l1.32.32-.81-1.09s-.55-.72-1.53-1.39c-1.62-1.1-4.46-2.1-8.14.31-1.51.99-2.61,2.59-3.68,4.14-1.05,1.52-2.03,2.96-3.36,3.83-1.81,1.19-3.46.81-3.53.79M2.32,70.96l-1.14-.75.39,1.3c.02.06,1.85,5.94,8.71,4.32,1.77-.41,3.35-1.54,4.88-2.64,1.5-1.07,2.92-2.08,4.46-2.45,2.1-.5,3.53.43,3.59.47l1.13.75-.39-1.3s-.27-.87-.96-1.82c-1.14-1.59-3.47-3.5-7.75-2.49-1.76.41-3.35,1.54-4.87,2.64-1.5,1.07-2.92,2.09-4.46,2.45-2.1.49-3.53-.43-3.59-.47M4.11,53.12c-2.15-.25-3.17-1.61-3.21-1.67l-.81-1.09-.08,1.36c0,.06-.29,6.21,6.71,7.04,1.8.21,3.67-.31,5.49-.81,1.78-.49,3.46-.96,5.03-.77,2.15.26,3.17,1.61,3.21,1.67l.81,1.09.08-1.35s.04-.9-.28-2.04c-.53-1.89-2.06-4.47-6.43-4.99-1.8-.21-3.67.31-5.48.81-1.78.49-3.46.96-5.03.77M19.1,37.4c-1.62-.81-3.55-.97-5.43-1.11-1.84-.14-3.58-.28-4.99-.99-1.93-.97-2.43-2.6-2.45-2.66l-.39-1.31-.54,1.25c-.02.06-2.4,5.73,3.9,8.91,1.62.82,3.56.97,5.43,1.12,1.84.14,3.58.28,4.99.99,1.93.97,2.43,2.6,2.45,2.66l.39,1.3.54-1.25s.35-.84.44-2.02c.14-1.96-.41-4.91-4.34-6.89M28.14,25.65c-1.24-1.32-3.01-2.12-4.72-2.9-1.68-.77-3.27-1.49-4.35-2.64-1.48-1.57-1.39-3.27-1.39-3.34l.08-1.36-.94.99s-4.22,4.57.62,9.7c1.24,1.32,3.01,2.13,4.72,2.9,1.68.77,3.27,1.49,4.35,2.64,1.48,1.58,1.39,3.27,1.39,3.34l-.08,1.36.94-.99s.61-.66,1.1-1.74c.81-1.79,1.3-4.75-1.72-7.96M39.54,25.78c1.37-1.4,2.85-4.03,1.11-8.07-.72-1.66-2.1-3.03-3.44-4.34-1.32-1.29-2.56-2.52-3.19-3.97-.85-1.99-.19-3.55-.16-3.61l.54-1.25-1.22.61c-.06.03-5.52,2.85-2.74,9.33.72,1.67,2.1,3.03,3.44,4.34,1.32,1.29,2.56,2.52,3.18,3.97.85,1.99.19,3.55.16,3.62l-.54,1.25,1.21-.61s.81-.42,1.63-1.26M53.37,9.26c-.8-1.67-1.55-3.24-1.64-4.82-.12-2.16,1.03-3.4,1.08-3.45l.94-.99-1.35.15c-.06,0-6.17.79-5.76,7.83.1,1.81.94,3.56,1.75,5.26.8,1.67,1.55,3.24,1.64,4.82.12,2.16-1.03,3.4-1.08,3.45l-.94.99,1.35-.15s.9-.12,1.96-.63c1.77-.85,4.05-2.81,3.8-7.2-.1-1.81-.94-3.56-1.75-5.26M72.28,2.97l1.22-.61-1.32-.32c-.06-.01-6.06-1.37-8.09,5.39-.52,1.74-.34,3.67-.16,5.54.18,1.84.35,3.57-.11,5.09-.62,2.07-2.13,2.85-2.2,2.88l-1.22.61,1.32.32s.88.2,2.06.08c1.95-.2,4.77-1.25,6.03-5.47.52-1.73.34-3.67.15-5.54-.18-1.84-.34-3.57.11-5.09.62-2.07,2.13-2.84,2.2-2.87M89.89,11.49l1.35-.15-1.14-.75s-5.23-3.36-9.45,2.29c-1.08,1.45-1.57,3.34-2.04,5.16-.46,1.79-.9,3.48-1.84,4.74-1.29,1.73-2.98,1.94-3.05,1.95l-1.35.15,1.13.75s.76.49,1.91.78c1.9.48,4.91.45,7.54-3.08,1.08-1.45,1.57-3.33,2.04-5.15.46-1.79.9-3.48,1.85-4.75,1.29-1.73,2.98-1.94,3.05-1.95M104.84,25.83l-.81-1.09c-.03-.05-3.76-4.94-9.66-1.08-1.52.99-2.62,2.6-3.68,4.15-1.04,1.52-2.03,2.96-3.35,3.83-1.81,1.18-3.46.8-3.53.79l-1.32-.32.81,1.09s.55.72,1.53,1.39c1.62,1.1,4.46,2.1,8.14-.31,1.52-.99,2.61-2.59,3.68-4.14,1.05-1.52,2.03-2.96,3.36-3.83,1.81-1.19,3.46-.81,3.53-.79l1.32.32Z"/><polygon class="lg-word" points="270.03 45.99 255.77 81.92 241.37 81.92 227.19 45.99 242.29 45.99 248.5 65.12 254.93 45.99 270.03 45.99"/><g><path class="lg-accent" d="M98.71,116.43h2.16l-.83,6.95c-2.47,1.38-5.22,2.28-9.35,2.28-8.21,0-13.39-5.7-13.39-13.59,0-9.15,6.13-14.77,13.86-14.77,4.01,0,6.87,1.06,8.76,2.59v6.13h-2.12c-1.06-4.36-3.3-6.44-6.83-6.44-5.81,0-8.21,5.26-8.21,11.35,0,7.11,2.95,12.41,8.72,12.41,3.73,0,5.73-2.32,7.23-6.91Z"/><path class="lg-accent" d="M103.66,115.13c0-6.87,4.56-11.31,10.29-11.31,6.05,0,9.98,4.48,9.98,10.53,0,6.87-4.59,11.31-10.33,11.31-6.05,0-9.94-4.48-9.94-10.53ZM118.98,115.33c0-5.11-2-9.27-5.54-9.27-3.26,0-4.87,3.3-4.87,8.09,0,5.11,2,9.23,5.58,9.23,3.22,0,4.83-3.26,4.83-8.05Z"/><path class="lg-accent" d="M152.04,125.27v-1.77c1.77-.24,2.75-.43,2.75-2.24v-10.6c0-2.51-.86-3.38-3.14-3.38-1.81,0-3.46.71-4.83,1.65v12.33c0,1.81,1.02,2,2.75,2.24v1.77h-10.25v-1.77c1.77-.24,2.75-.43,2.75-2.24v-10.6c0-2.51-.86-3.38-3.1-3.38-1.85,0-3.5.71-4.87,1.65v12.33c0,1.81.94,2,2.71,2.24v1.77h-10.29v-1.77c1.73-.24,2.83-.43,2.83-2.24v-12.8l-2.63-1.69v-.98l6.28-2.04h1.1v4.01c1.81-1.88,4.01-3.93,7.27-3.93,2.67,0,4.56,1.26,5.22,4.08,1.85-1.88,4.28-4.08,7.58-4.08s5.38,1.92,5.38,6.4v11.04c0,1.81,1.06,2,2.83,2.24v1.77h-10.33Z"/><path class="lg-accent" d="M189.9,125.27v-1.77c1.77-.24,2.75-.43,2.75-2.24v-10.6c0-2.51-.86-3.38-3.14-3.38-1.81,0-3.46.71-4.83,1.65v12.33c0,1.81,1.02,2,2.75,2.24v1.77h-10.25v-1.77c1.77-.24,2.75-.43,2.75-2.24v-10.6c0-2.51-.86-3.38-3.1-3.38-1.85,0-3.5.71-4.87,1.65v12.33c0,1.81.94,2,2.71,2.24v1.77h-10.29v-1.77c1.73-.24,2.83-.43,2.83-2.24v-12.8l-2.63-1.69v-.98l6.28-2.04h1.1v4.01c1.81-1.88,4.01-3.93,7.27-3.93,2.67,0,4.56,1.26,5.22,4.08,1.85-1.88,4.28-4.08,7.58-4.08s5.38,1.92,5.38,6.4v11.04c0,1.81,1.06,2,2.83,2.24v1.77h-10.33Z"/><path class="lg-accent" d="M217.27,121.81c-1.77,1.85-4.01,3.85-7.31,3.85s-5.66-1.92-5.66-6.52v-10.29c0-1.3-.39-1.85-2.08-2.12l-.63-.12v-1.57l6.68-1.22h.83v14.73c0,2.59,1.02,3.77,3.26,3.77,1.88,0,3.53-.75,4.91-1.65v-11.82c0-1.3-.39-1.85-2.08-2.12l-.59-.12v-1.57l6.6-1.22h.86v16.77c0,1.33.35,1.73,1.96,1.88l.98.08v1.77l-6.87,1.34h-.86v-3.85Z"/><path class="lg-accent" d="M243.22,110.66c0-2.43-.98-3.38-3.3-3.38-1.85,0-3.81.71-5.14,1.65v12.33c0,1.81.98,2,2.75,2.24v1.77h-10.33v-1.77c1.73-.24,2.83-.43,2.83-2.24v-12.8l-2.63-1.69v-.98l6.28-2.04h1.1v4.01c1.81-1.88,4.24-3.93,7.54-3.93,3.53,0,5.66,1.92,5.66,6.44v11c0,1.81,1.06,2,2.83,2.24v1.77h-10.37v-1.77c1.77-.24,2.79-.43,2.79-2.24v-10.6Z"/><path class="lg-accent" d="M260.42,121.26c0,1.81,1.06,2,2.83,2.24v1.77h-10.41v-1.77c1.73-.24,2.83-.43,2.83-2.24v-12.84l-2.63-1.69v-.94l6.28-1.96h1.1v17.44ZM254.88,98.52c0-1.61,1.26-2.95,3.02-2.95s2.98,1.34,2.98,2.95-1.26,2.95-2.98,2.95-3.02-1.33-3.02-2.95Z"/><path class="lg-accent" d="M272.16,104.21h5.77v2.36h-5.77v13.24c0,2.08.9,2.83,2.91,2.83,1.1,0,2.4-.31,3.38-.83l.51,1.22c-1.49,1.61-3.65,2.63-6.36,2.63-3.14,0-5.18-1.49-5.18-5.11v-13.98h-2.79v-1.49c2.2-1.14,4.32-2.98,6.13-5.5h1.41v4.63Z"/><path class="lg-accent" d="M287.95,121.26c0,1.81,1.06,2,2.83,2.24v1.77h-10.41v-1.77c1.73-.24,2.83-.43,2.83-2.24v-12.84l-2.63-1.69v-.94l6.28-1.96h1.1v17.44ZM282.41,98.52c0-1.61,1.26-2.95,3.02-2.95s2.98,1.34,2.98,2.95-1.26,2.95-2.98,2.95-3.02-1.33-3.02-2.95Z"/><path class="lg-accent" d="M311.08,112.66v1.3h-13.71c0,4.75,2.67,7.93,6.83,7.93,2.79,0,4.63-1.3,6.05-3.18l.86.51c-.98,3.81-3.97,6.44-8.56,6.44-5.77,0-9.43-4.36-9.43-10.25,0-6.95,4.24-11.59,9.82-11.59s8.13,3.77,8.13,8.84ZM297.49,111.95h9.15c-.04-3.61-1.45-5.97-4.32-5.97s-4.52,2.79-4.83,5.97Z"/><path class="lg-accent" d="M314.02,123.62l-.24-5.07h2.04c.75,3.22,2.59,5.11,5.73,5.11,2.32,0,3.81-1.06,3.81-2.95,0-2.24-1.57-3.02-5.11-4.01-3.97-1.1-6.32-2.79-6.32-6.52s2.87-6.36,7.3-6.36c2.71,0,4.95.67,6.68,1.69v4.71h-2c-.59-2.87-2.16-4.36-4.83-4.36-2.04,0-3.22,1.22-3.22,2.83,0,1.92,1.3,2.95,4.52,3.81,4.04,1.1,6.83,2.47,6.83,6.6,0,3.89-2.91,6.56-7.78,6.56-2.83,0-5.5-.63-7.42-2.04Z"/></g></g></g></svg>'
FOOTER_BG = V("footer-rocks.16z_pgs-5dzer.jpg")

LIFE = [
    ("Live In", "/live-in", "Floor Plans. The Design Center. How We Build.", V("live-in.0-iialxva3p9u.jpg"), "Couple relaxing in a SunRiver Firelight home"),
    ("Live Out", "/live-out", "Southern Utah. Trails and Nearby Adventure.", V("live-out.2z9c8sf8gogme.jpg"), "SunRiver members hiking in red rock country"),
    ("Live On", "/live-on", "Clubs and Activities. Events Calendar. Bucketlist.", V("live-on.2kwzvtocledst.jpg"), "SunRiver members enjoying a club activity"),
]
NAV = [("homes", "Homes", "/homes-for-sale"), ("about", "About", "/about"), ("visit", "Visit", "/contact-us")]


def pill_header(active, variant="bar"):
    """Site header from the OFFICIAL SunRiver Website Figma file: logo plus the pill nav with the
    Life at SunRiver dropdown ("Home Clark Life NAV 6").
      variant "home"    : over the homepage hero, no tab ("Home Clark Life NAV 6")
      variant "overlay" : over a photo hero with the yellow Founders Club tab ("Homes for Sale / Model Homes")
      variant "bar"     : white 168px bar with shadow ("Homes for Sale Filter Simple", "Home Detail")"""
    from .figma_assets import FG
    items = "".join('<li><a href="%s" data-i="%d"><strong>%s</strong><span>%s</span></a></li>' % (h, k, t, sub) for k, (t, h, sub, _, _) in enumerate(LIFE))
    # Dropdown photo per item (OFFICIAL "Home NAV Live In/Out/On"): it swaps as you hover each one.
    # Live On uses the Figma photo, which is also what shows when the menu first opens.
    shots = [(LIFE[0][3], LIFE[0][4]), (LIFE[1][3], LIFE[1][4]), (FG("nav-photo"), "SunRiver members playing pickleball")]
    photos = "".join('<span class="pd-shot%s" data-i="%d">%s</span>' % (" is-on" if k == 2 else "", k, img(src, alt, loading="eager"))
                     for k, (src, alt) in enumerate(shots))
    cur = lambda k: ' aria-current="page"' if k == active else ""
    tab = ""  # the Founders Club tab is retired
    # One header everywhere: logo plus the floating pill, no white bar behind it.
    cls = {"home": "site-header overlay", "overlay": "site-header overlay", "bar": "site-header overlay on-light"}[variant]
    return '''<a class="skip" href="#main">Skip to content</a>
<header class="%s" data-menu="closed">
  %s
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="SunRiver Communities home">%s</a>
    <button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="main-nav pill-nav" aria-label="Main">
      <div class="nav-item" data-open="false"><button class="nav-link" type="button" aria-expanded="false" aria-controls="life-menu"%s>Life at SunRiver<span class="chev" aria-hidden="true"></span></button>
        <div class="pill-drop" id="life-menu" data-active="2"><ul>%s</ul><div class="pill-drop-photo" aria-hidden="true">%s</div></div></div>
      <div class="nav-item"><a class="nav-link" href="/homes-for-sale"%s>Homes</a></div>
      <div class="nav-item"><a class="nav-link" href="/discovery-villas"%s>Discovery Villas</a></div>
      <a class="pill-cta" href="/contact-us"%s>Visit</a>
    </nav>
  </div>
</header>
<div class="m-nav" id="m-nav" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="m-nav-bar">
    <a class="m-nav-logo" href="/" aria-label="SunRiver Communities home">%s</a>
    <a class="m-nav-visit" href="/contact-us">Visit</a>
    <button class="m-nav-close" type="button" aria-label="Close menu"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5l10 10M15 5L5 15"/></svg></button>
  </div>
  <nav class="m-nav-body" aria-label="Mobile">
    <p class="m-nav-head">Life at SunRiver</p>
    <div class="m-nav-group"><a class="m-nav-top" href="/live-in">Live In</a>
      <a href="/floor-plans">Floor Plans</a><a href="/live-in#design-center">The Design Center</a><a href="/energy">How We Build</a></div>
    <div class="m-nav-group"><a class="m-nav-top" href="/live-out">Live Out</a>
      <a href="/southern-utah">Southern Utah</a><a href="/live-out#trails">Trails &amp; Nearby Adventures</a></div>
    <div class="m-nav-group"><a class="m-nav-top" href="/live-on">Live On</a>
      <a href="/live-on">Clubs &amp; Activities</a><a href="/bucketlistliving/category/events">Events Calendar</a><a href="/bucketlistliving">Bucketlist</a></div>
    <a class="m-nav-top" href="/homes-for-sale">Homes</a>
    <a class="m-nav-top" href="/discovery-villas">Discovery Villas</a>
    <div class="m-nav-photo">%s</div>
  </nav>
</div>''' % (cls, tab, LOGO_SVG, cur("life"), items, photos,
       cur("homes"), cur("villas"), cur("visit"), LOGO_SVG, img(LIFE[1][3], LIFE[1][4]))


def header(active):
    """Every page uses the pill nav. "home-overlay" is the homepage; an active key ending in "-overlay"
    puts the header over that page's photo hero with the Founders tab; everything else gets the white bar."""
    if active == "home-overlay":
        return pill_header("", "home")
    if active.endswith("-overlay"):
        return pill_header(active[:-8], "overlay")
    return pill_header(active, "bar")


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
    if body.lstrip().startswith('<section class="fah-hero') and not active.endswith("-overlay"):
        active = (active or "page") + "-overlay"  # full photo hero: the header and nav sit on the photo
    if active.endswith("-overlay") and active != "home-overlay":
        body_class = (body_class + " overlay-page").strip()
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


def full_hero(title, sub="", eyebrow="", src=None, alt="", cta=None, pos="50% 40%", extra="", tag="h1", cls=""):
    """The sitewide page hero: a full-bleed photo that runs up under the floating header (like Homes for Sale),
    a white wash at the top for the logo and nav, a blue tint behind a white title with a yellow underline."""
    from .figma_assets import FG
    src = src or FG("hfs-hero")
    e = '<p class="fh-eyebrow">%s</p>' % eyebrow if eyebrow else ""
    sb = '<p class="fh-sub">%s</p>' % sub if sub else ""
    c = '<div class="fh-cta">%s</div>' % cta if cta else ""
    return ('<section class="fah-hero fh-hero%s">%s<div class="wrap fah-hero-inner">%s<%s>%s</%s>%s%s</div>%s</section>' % (
        " " + cls if cls else "", img(src, alt, "fah-hero-img", "eager", 'style="object-position:%s"' % pos), e, tag, title, tag, sb, c, extra))


def sand_hero(eyebrow, title, sub="", tag="h1", src=None, alt="", pos="50% 40%"):
    return full_hero(title, sub, eyebrow, src, alt, tag=tag, pos=pos)


ABOUT_TABS = [("About Us", "/about"), ("History", "/history"), ("FAQ", "/faq"), ("Southern Utah", "/southern-utah")]


def yellow_hero(title_html, current, src=None, alt="", pos="50% 40%"):
    tabs = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == current else "", t) for t, h in ABOUT_TABS)
    return full_hero(title_html, src=src, alt=alt, pos=pos) + '<nav class="tabbar" aria-label="About SunRiver"><ul>%s</ul></nav>' % tabs


def photo_hero(eyebrow, title, sub, src, alt, cta=None, pos="50% 40%"):
    return full_hero(title, sub, eyebrow, src, alt, cta, pos)


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
