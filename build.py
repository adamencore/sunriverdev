#!/usr/bin/env python3
"""Build the SunRiver website into ./dist (Netlify runs this on every push; see netlify.toml).

  python3 build.py              build with live CMS data (falls back to /data snapshots locally)
  OFFLINE=1 python3 build.py    skip the CMS and use the snapshots
  MIRROR=0 python3 build.py     skip copying dev-site media (pages point at the remote files)

Structure
  sitegen/lib.py         shared chrome (header, footer, chat form) and helpers
  sitegen/data.py        Sanity CMS queries (floor plans, homes for sale, blog posts)
  sitegen/pages_cms.py   floor plans, homes for sale, Bucketlist Living
  sitegen/pages_main.py  every other page
  assets/                styles.css, site.js, images we host ourselves
"""
import os
import shutil
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from sitegen import figma_assets, lib  # noqa: E402
from sitegen.data import ON_NETLIFY, get_all  # noqa: E402
from sitegen.pages_cms import build_blog, build_floor_plans, build_homes  # noqa: E402
from sitegen.pages_main import build_main  # noqa: E402

DIST = ROOT / "dist"

REDIRECTS = """
# Earlier builds of this site used flat .html files
/index.html                              /                              301
/sunriver-firelight.html                 /sunriver-firelight            301
/sunriver-firelight-floor-plans.html     /floor-plans                   301
/st-george.html                          /st-george                     301
/villas.html                             /villas                        301
/southern-utah.html                      /southern-utah                 301
/faq.html                                /faq                           301
/contact.html                            /contact-us                    301
/discovery-villas.html                   /discovery-villas              301
/founders-club.html                      /founders-club                 301
/no-mortgage-payments-for-life.html      /no-mortgage-payments-for-life 301
/energy.html                             /energy                        301
/bucketlist-living.html                  /bucketlistliving              301
/privacy-policy.html                     /privacy-policy                301
/about.html                              /about                         301
/history.html                            /history                       301
/find-a-home.html                        /find-a-home                   301
/homes-for-sale.html                     /homes-for-sale                301
/sunriver-best-55-plus-community-utah.html  /why-sunriver               301

# URLs from the current sunriver.com, so old links keep working after launch
/contact                                 /contact-us                    301
/sunriver-firelight-floor-plans          /floor-plans                   301
/floorplans                              /floor-plans                   301
/sunriver-best-55-plus-community-utah    /why-sunriver                  301
/bucketlist-living                       /bucketlistliving              301
/bucketlist-living/*                     /bucketlistliving/:splat       301
/calendar                                /bucketlistliving              302
/calendar/*                              /bucketlistliving              302
/mortgage-options                        /no-mortgage-payments-for-life 301
/bucketlistliving  page=:p               /bucketlistliving/page/:p      301!
"""
PLAN_SLUGS = ["hamlet", "august", "tara", "evergreen", "elmwood", "astoria", "amberly"]


def download(item):
    local, remote = item
    dest = DIST / local.lstrip("/")
    if dest.exists() and dest.stat().st_size > 0:
        return local, True
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            req = urllib.request.Request(remote, headers={"User-Agent": "sunriver-netlify-build"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if not data:
                raise ValueError("empty response")
            dest.write_bytes(data)
            return local, True
        except Exception:  # noqa: BLE001
            time.sleep(1 + attempt)
    return local, False


def main():
    started = time.time()
    print("Loading content")
    plans, listings, posts = get_all()

    print("Rendering pages")
    build_main(plans, listings)
    build_floor_plans(plans)
    build_homes(listings)
    build_blog(posts)

    if DIST.exists():
        keep = DIST / "media"
        shutil.rmtree(keep / "fg", ignore_errors=True)
        for p in DIST.iterdir():
            if p != keep:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)

    # Mirror the dev site's static media so pages don't depend on another team's deployment.
    failed = []
    mirror_on = os.environ.get("MIRROR", "1" if ON_NETLIFY else "0") == "1"
    if mirror_on:
        download(("/favicon.ico", lib.VERCEL + "/favicon.ico"))
        print("Mirroring %d media files" % len(lib.MIRROR))
        with ThreadPoolExecutor(max_workers=8) as pool:
            for local, ok in pool.map(download, sorted(lib.MIRROR.items())):
                if not ok:
                    failed.append(local)
        if failed:
            print("  %d files could not be mirrored, linking to the dev site instead: %s" % (len(failed), ", ".join(failed)))
    else:
        failed = list(lib.MIRROR)
    fallback = {local: lib.MIRROR[local] for local in failed}
    print("Building homepage images from Figma")
    fallback.update(figma_assets.build(DIST, ON_NETLIFY))

    for path, doc in lib.PAGES.items():
        for local, remote in fallback.items():
            if local.startswith("/media/fg/"):
                doc = doc.replace(local + "?", remote + "?")
                continue
            doc = doc.replace('"%s"' % local, '"%s"' % remote).replace("(%s)" % local, "(%s)" % remote).replace("%s " % local, "%s " % remote)
        if path == "/404":
            out = DIST / "404.html"
        else:
            out = DIST / path.lstrip("/") / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding="utf-8")

    rules = REDIRECTS.strip("\n") + "\n" + "".join("/%-40s /floor-plans/%-20s 301\n/%-40s /floor-plans/%-20s 301\n" % (s, s, s + ".html", s) for s in PLAN_SLUGS)
    (DIST / "_redirects").write_text(rules, encoding="utf-8")

    print("Built %d pages in %.1fs (%d floor plans, %d listings, %d posts)" % (len(lib.PAGES), time.time() - started, len(plans), len(listings), len(posts)))


if __name__ == "__main__":
    main()
