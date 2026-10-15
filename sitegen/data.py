"""CMS data. On Netlify the build reads live content from the developers' Sanity project
(public, read-only API). Locally it falls back to the snapshots in /data when the API
can't be reached. A failed fetch on Netlify fails the build so a broken deploy never ships."""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://ib6s13lu.apicdn.sanity.io/v2024-01-01/data/query/production?query="
ON_NETLIFY = os.environ.get("NETLIFY") == "true"
NOT_DRAFT = '!(_id in path("drafts.**"))'

QUERIES = {
    "floorPlans": '*[_type=="floorPlan" && %s]|order(squareFootage asc){name,"slug":slug.current,badge,bedrooms,bathrooms,features,'
                  'gallery[]{alt,"asset":asset._ref},matterportId,planDiagram{alt,"asset":asset._ref},priceRange,specLine,squareFootage,width}' % NOT_DRAFT,
    "homeListings": '*[_type=="homeListing" && %s]{title,"slug":slug.current,address,baths,beds,community,garageSpaces,hobbyRooms,'
                    'mlsNumber,price,squareFootage,status,statusDate,askForPricing,isNew,youtubeShortIds,"photo":photo.asset._ref,'
                    '"photoAlt":photo.alt,"gallery":gallery[].asset._ref}' % NOT_DRAFT,
    "posts": '*[_type=="post" && %s && defined(body)]|order(publishDate desc){title,"slug":slug.current,publishDate,excerpt,categories,'
             '"cover":coverImage.asset._ref,body}' % NOT_DRAFT,
}


def fetch(query):
    req = urllib.request.Request(API + urllib.parse.quote(query), headers={"User-Agent": "sunriver-netlify-build"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))["result"]


def normalize_plan(p):
    """Snapshot rows store slug as an object; the live query flattens it."""
    if isinstance(p.get("slug"), dict):
        p["slug"] = p["slug"].get("current")
    return p


def load(name):
    if os.environ.get("OFFLINE") != "1":
        try:
            rows = fetch(QUERIES[name])
            print("  %s: %d rows from Sanity" % (name, len(rows)))
            return rows
        except Exception as e:  # noqa: BLE001
            if ON_NETLIFY:
                print("ERROR: could not load %s from Sanity: %s" % (name, e), file=sys.stderr)
                raise
            print("  %s: Sanity unreachable (%s), using snapshot" % (name, e.__class__.__name__))
    rows = json.loads((ROOT / "data" / (name + ".json")).read_text(encoding="utf-8"))
    print("  %s: %d rows from snapshot" % (name, len(rows)))
    return rows


def block_text(body):
    out = []
    for b in body or []:
        if b.get("_type") == "block":
            out.append("".join(c.get("text", "") for c in b.get("children", [])))
    return " ".join(out).strip()


def get_all():
    plans = [normalize_plan(p) for p in load("floorPlans")]
    listings = load("homeListings")
    posts = [p for p in load("posts")
             if p.get("slug") and p.get("title") and not p["title"].startswith("[PENDING") and block_text(p.get("body"))]
    return plans, listings, posts
