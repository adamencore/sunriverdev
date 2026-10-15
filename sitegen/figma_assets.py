"""Homepage imagery exported from the Figma file "SunRiver Website 2026", frame "Home Clark Life NAV 4" (node 625:214).

Each entry is cropped exactly the way the Figma layer frames it, then resized and saved as WebP into
/media/fg at build time (Pillow, see requirements.txt).

Source order during a build:
  1. the Figma export URL (temporary, issued 2026-10-15, expires about 2026-10-22)
  2. the copy already published on the live Netlify site (every deploy republishes it)
On Netlify the build fails if neither works, so a deploy never ships with missing homepage images.
To swap an image later, put a new export URL in FIGMA_IDS (or drop a file at assets/fg/<name>.webp,
which always wins).
"""
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
    "navphoto": "bb3e9fb1-6b96-49fe-a1dd-2464d4a7f94d",  # 20190613_SunRiverVillas_2990, nav dropdown
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
    "nav-photo": ("navphoto", 295.049, 205.597, 0, -0.16, 100, 95.68, 566, {"region": (0, 8, 283, 147)}),
}

USED = set()


def FG(name):
    USED.add(name)
    return "/media/fg/%s.webp" % name


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
                    raw_cache[src] = _get(FIGMA + FIGMA_IDS[src] + ".png")
                dest.write_bytes(_render(Image, ImageOps, raw_cache[src], SPECS[name]))
                done = True
            except Exception as e:  # noqa: BLE001
                print("  figma export unavailable for %s (%s)" % (name, e.__class__.__name__))
        if not done and online:
            try:
                dest.write_bytes(_get(SELF + local))
                done = True
            except Exception:  # noqa: BLE001
                pass
        if not done:
            if on_netlify:
                raise RuntimeError("Homepage image %s could not be built from Figma or the live site" % name)
            failed[local] = SELF + local
    print("  homepage images: %d built, %d linked to the live site" % (len(USED) - len(failed), len(failed)))
    return failed
