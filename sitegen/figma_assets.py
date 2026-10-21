"""Imagery exported from Figma.
Homepage: file "SunRiver Website 2026", frame "Home Clark Life NAV 4" (node 625:214); nav dropdown photo from
"Home Clark Life NAV 6" (node 660:2).
Find a Home, Homes for Sale and the listing template: file "OFFICIAL SunRiver Website" (P3Ozmr47Say3ms57lX4htZ),
frames "Homes for Sale / Model Homes" (6:206), "Homes for Sale Filter Simple" (6:267), "Homes for Sale Home Detail" (6:503).

Each entry is cropped exactly the way the Figma layer frames it, then resized and saved as WebP into
/media/fg at build time (Pillow, see requirements.txt).

Source order during a build:
  1. the Figma export URL (temporary, issued 2026-10-15, expires about 2026-10-22)
  2. the copy already published on the live Netlify site (every deploy republishes it)
On Netlify the build fails if neither works, so a deploy never ships with missing homepage images.
To swap an image later, put a new export URL in FIGMA_IDS (or drop a file at assets/fg/<name>.webp,
which always wins).
"""
import hashlib
import io
import os
import urllib.request
from pathlib import Path

FIGMA = "https://www.figma.com/api/mcp/asset/"
SELF = "https://sunriverdev.netlify.app"
ROOT = Path(__file__).resolve().parent.parent

FIGMA_IDS = {
    "hero": "207d3e9c-31b1-4f94-b947-4fe104483f39",      # couple biking, 2517x4096
    "couple": "2146057e-48fd-40c8-91a1-54b603f4c01d",    # SRF Couple No BKGRD (transparent PNG)
    "sky": "a06e0d46-a8be-4b9f-bc31-60d90fa31364",       # YOUR NEW LIFESTYLE AWAITS band
    "years1": "58032232-5039-4662-b8ed-c4564f544380",    # collage, Rectangle 196
    "years2": "1c7fa975-2582-49e3-bc46-6c702dd9c031",    # collage, Rectangle 189
    "years3": "ccd5576c-7388-4d7f-8d5a-c00f13eea312",    # collage, Rectangle 194
    "years4": "c604a917-32e7-4e93-ab19-cff90f5bf2cd",    # collage, Rectangle 190
    "begin": "10979461-908c-472f-ba95-06b4be7fd098",     # Where you begin background
    "navphoto": "3fd9cc08-4015-4170-b19e-d7f9a7f52030",  # 20190613_SunRiverVillas_2990, nav dropdown (OFFICIAL "Home NAV Live In/Out/On", 14:1198)
    # OFFICIAL file, exports issued 2026-10-19 (expire about 2026-10-26; the live-site copy takes over after that)
    "fah_hero": "9d943a9d-39c2-4942-a3eb-4cda27c34448",  # Discovery Villas Row 1, Find a Home hero
    "fah_card": "1cdb7ead-eb9a-4826-97b8-e94300fe4170",  # Rectangle 202, FLOOR PLANS card
    "hfs_band": "eac1e2af-712e-4c45-971b-f762936946b7",  # Rectangle 133, Homes for sale band
    "li_bedroom": "https://s3-alpha-sig.figma.com/img/344f/a386/5f6b6a2704e33ef7c82c80dfbd29ead3?Expires=1793577600&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=Oje4m6hKwL7HaUGOZHLt7xdt4O-7KE0ja-EqDJpt7GPOf8TzF8NsRlXa8T-FfytjiUjRcrlhyup5DQu6u0UYDmlg6ywIBfPw2FT3Zhi3hzsC~n-YXU0OV~myE-4WGsQnnJ1MauyWYuYlcQrPh1IvtqpZg5UmsCAYNpN1GrUJ~050iPhkB5hFOruCI1TXMogggiSssVmMAkH5wKjvK5j4aW0BHioo5u9wrxCj-16rhs8ByCIznxDG~pcK6YNYSuiSkWuP6ChCYQIASRq~-O1lxbmAfBC0Pl~DrIkV1PyYpLfRSKEwUSBUqFD7h6YZzSb4C652Sh2QSN~xGviSZ7xaVg__",  # Live In, 04 / The Design Center
    "sales_team": "87d320a1-aa84-40ac-bb9b-cba4b8e53d03",  # SunRiver Sales Team 2 (cut out)
    # Full-size originals read from the Figma file in the browser (signed links, valid to about 2026-11-02)
    "fl_founders": "https://s3-alpha-sig.figma.com/img/fd9f/7abe/de346e9455042f21a68b4c8ae301db70?Expires=1793577600&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=YPmnYtHA4agoa8Q2QtxD3NhwNnVnctzfBynAwAINEqKv5hH~iagQHLgsepW2KblzdeNxKxWUaWRi8H2qihhomeMs~Ne~kJglJe2L5VQoXWJycxXcmR83UNNIru8zaJAajTlzdOua78wTHe-0zqE3lgM0h7vNtlAiAECtvKI-gAiZD6AoxbgMyfA9ef339dRoT0V3dX8AftA0l3lTIcn-Ra~ys1DUcUTYAmCFKsAx4qMe8cWA-v7NjKS~Gbiacx515yX3wv6~Rf58w3D~E3HjGP6jvOsol7WBSnct0AlU4Qx6B9Njs~cUDScisQf8nmqHJSielk~Ml~FFwztT~wwKhg__",
    "fl_smart": "https://s3-alpha-sig.figma.com/img/270c/d40a/707fa627e86465d4c80c7f845c21a219?Expires=1793577600&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=NrO9GO~lihKhrwkPl3Pzd-OwoORYCDhEWMKTN2vgI-A~2YRFujqn4Sm8rTxocVq1wq67LyQhJ~ZgBykk3GShyvHixakUszXaN8hMGQU3aXHP3Rpee8fgi3sDJeVFZtcbPjlVkJ12lAheiruwEX6D5dowawcSJmxz8LKsqyJTfFy3khMyemhHAWt0wtAr2bfQfOEZ9t7tcg~vFgQ23U1sIANoIJGMt5b2zygR8xoud6r-MZIhZXyuS41OqkpWX1nvT7cdAiv3xbMYn7ZKYm4Uaw~qXcEGA0yHR32RBMsZTmmjhDakNi1ESHm0FuHtXylY34Tnqn8Wddnd8RudxbrZMw__",
    "li_hero": "https://s3-alpha-sig.figma.com/img/7883/f3a5/247799052dce918b2474e9de97e2fda4?Expires=1793577600&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=X-NTor9119a6Q3pUOJXMXkKsdKOdXnWDmDjIjLLq0SLeudvLxeGShn7hJgUFo1VHbDOLoFHEwF5NkDrOfZ03SekOoc5OxhmcHQImZM4hjJBzdmzzQGSHj67Ew9HbtBexATst5InaZ9VrC0o-LyUWggBy7-YpfTpK-dtRocgwnVxobWiVUBCbiD4oVMw5I8eXbTdlayPDHLb8382Bo9HSWN8wt3NSiNyQ6aoGZJgj7RfTVD2pNT12GkxjJHNmtxxYDE9rSU-h5MyLrpyBBfElW~w375CYVbLV81~bAkQEThXZn2uELhk2ONUB0E4y88WosNkBkyaqNNu7eX8SKvGJNw__",
    "fl_trails": "https://s3-alpha-sig.figma.com/img/20de/bfe4/e9f6cdf4c07e2d8c2925b3d0b7dbe921?Expires=1793577600&Key-Pair-Id=APKAQ4GOSFWCW27IBOMQ&Signature=W8~8tUJpQcbxR7qCtBx4lBAen6QV2rhcYRhpi4lixh2O0j-URjWrFl4yr85EwfCpKSVY~ykrTQ2uftEUhGxsntjoK3LTAN~ub49q5SORqHFwZGOmyaGjbO~j75JpzR7qxokGwKMqVmdogLpuYXFNYV6Wp0FcTKFGYCXEqDhW6kh-09~qmZt3Iz-1iYLLRnEdq~gb2qre4jLoJEFOVC5nLFvry~y3BBGdHf1S5xtFTcwa6bRfpZWqSUY9wlJxJxevy4yasmev-g0tPyhtvP1sSNutv1FkN4h~1SFSDwI3wPJXigiIzjf1Or-TBkPnxOMWXCVlzbFjLkHDqVC0U-1UxA__",
}

# name: (source, frame w, frame h, image left %, top %, width %, height %, output width, options)
# Percentages are the image placement inside its Figma frame, straight from the design.
SPECS = {
    "hero-wide": ("hero", 1440, 932, 0.03, -150.94, 107.8, 270.79, 2400, {}),
    "hero-tall": ("hero", None, None, 0, 0, 100, 100, 1200, {}),
    "couple": ("couple", 758, 556, 0, -78.2, 100, 199.64, 1516, {"alpha": True}),
    "sky": ("sky", 1478, 261, -41.68, -59.2, 178.35, 504.98, 2400, {}),
    "years-1": ("years1", 458, 255, -38.23, -39.22, 149.33, 178.82, 916, {}),
    "years-2": ("years2", 340, 571.3, -24.58, -49.56, 141.36, 149.56, 680, {}),
    "years-3": ("years3", 269, 298, -37.91, -0.11, 169.14, 101.8, 538, {}),
    "years-4": ("years4", 315, 527, -75.46, 0, 250.92, 100, 630, {}),
    "begin": ("begin", 1455, 760, -17.85, -31.43, 127.64, 162.89, 2400, {"mirror": True}),
    "nav-photo": ("navphoto", 503, 351, -15.69, -8.44, 100, 95.68, 548, {"region": (50, 12, 274, 290)}),  # Home NAV Live In/Out/On dropdown
    "fah-hero": ("fah_hero", 1440, 611, -44.55, -3.18, 156.08, 206.54, 2400, {}),
    "fah-card": ("fah_card", 499, 261, -26.92, -35.94, 135.74, 146.06, 998, {}),
    "hfs-band": ("hfs_band", 1476, 238, 0, 4.38, 100, 348.39, 2400, {}),
    "hfs-hero": ("hfs_band", None, None, 0, 0, 100, 100, 2400, {"fallback": "hfs-band"}),
    "li-bedroom": ("li_bedroom", None, None, 0, 0, 100, 100, 1200, {}),
    "sales-team": ("sales_team", 442.233, 309.218, -4.06, -0.02, 108.11, 100.3, 884, {"alpha": True}),
    "fl-founders": ("fl_founders", None, None, 0, 0, 100, 100, 2400, {"mirror": True}),
    "fl-trails": ("fl_trails", None, None, 0, 0, 100, 100, 2400, {"alpha": True, "trim": (0, 0.27, 0, 0)}),  # empty sky above the peaks trimmed
    "li-hero": ("li_hero", None, None, 0, 0, 100, 100, 1536, {}),
    "fl-smart": ("fl_smart", None, None, 0, 0, 100, 100, 1536, {}),
}

USED = set()


def FG(name):
    """Local URL for a homepage image. The query string changes whenever the crop or source changes,
    so browsers holding a cached copy (media is cached for a year) fetch the new one."""
    USED.add(name)
    spec = SPECS[name]
    v = hashlib.md5(repr((spec, FIGMA_IDS[spec[0]])).encode("utf-8")).hexdigest()[:8]
    return "/media/fg/%s.webp?v=%s" % (name, v)


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "sunriver-netlify-build"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _render(Image, ImageOps, raw, spec):
    src, cw, ch, left, top, wp, hp, out_w, opt = spec
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGBA" if opt.get("alpha") else "RGB")
    iw, ih = im.size
    if cw:
        disp_w, disp_h = wp / 100.0 * cw, hp / 100.0 * ch
        off_x, off_y = left / 100.0 * cw, top / 100.0 * ch
        rx, ry, rw, rh = opt.get("region", (0, 0, cw, ch))
        box = ((rx - off_x) / disp_w * iw, (ry - off_y) / disp_h * ih,
               (rx + rw - off_x) / disp_w * iw, (ry + rh - off_y) / disp_h * ih)
        box = tuple(int(round(v)) for v in (max(0, box[0]), max(0, box[1]), min(iw, box[2]), min(ih, box[3])))
        im = im.crop(box)
    if opt.get("trim"):  # fractions of the source to cut away: (left, top, right, bottom)
        l, t, r, b = opt["trim"]
        w0, h0 = im.size
        im = im.crop((int(w0 * l), int(h0 * t), int(w0 * (1 - r)), int(h0 * (1 - b))))
    if opt.get("mirror"):
        im = ImageOps.mirror(im)
    if im.width > out_w:
        im = im.resize((out_w, int(round(im.height * out_w / float(im.width)))), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=80, method=6)
    return buf.getvalue()


def build(dist, on_netlify):
    """Write every used image into dist/media/fg. Returns {local path: fallback url} for any that failed."""
    out_dir = Path(dist) / "media" / "fg"
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = ImageOps = None
    online = os.environ.get("OFFLINE") != "1"
    raw_cache, failed = {}, {}
    for name in sorted(USED):
        local = "/media/fg/%s.webp" % name
        dest = out_dir / (name + ".webp")
        override = ROOT / "assets" / "fg" / (name + ".webp")
        if override.exists():
            dest.write_bytes(override.read_bytes())
            continue
        done = False
        if online and Image is not None:
            src = SPECS[name][0]
            try:
                if src not in raw_cache:
                    raw_cache[src] = _get(FIGMA_IDS[src] if FIGMA_IDS[src].startswith("http") else FIGMA + FIGMA_IDS[src] + ".png")
                dest.write_bytes(_render(Image, ImageOps, raw_cache[src], SPECS[name]))
                done = True
            except Exception as e:  # noqa: BLE001
                print("  figma export unavailable for %s (%s)" % (name, e.__class__.__name__))
        if not done and online:
            # the live site's copy, or for a new crop of an existing image, the live copy of the older crop
            for alt in [local] + (["/media/fg/%s.webp" % SPECS[name][8]["fallback"]] if SPECS[name][8].get("fallback") else []):
                try:
                    dest.write_bytes(_get(SELF + alt))
                    done = True
                    break
                except Exception:  # noqa: BLE001
                    pass
        if not done:
            if on_netlify:
                raise RuntimeError("Figma image %s could not be built from Figma or the live site" % name)
            failed[local] = SELF + local
    print("  homepage images: %d built, %d linked to the live site" % (len(USED) - len(failed), len(failed)))
    return failed
