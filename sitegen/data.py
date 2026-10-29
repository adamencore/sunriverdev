"""CMS data. On Netlify the build reads live content from the developers' Sanity project
(public, read-only API). Locally it falls back to the snapshots in /data when the API
can't be reached. A failed fetch on Netlify fails the build so a broken deploy never ships."""
import json
import os
import re
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
                    'mlsNumber,description,price,squareFootage,status,statusDate,askForPricing,isNew,youtubeShortIds,"photo":photo.asset._ref,'
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


def apply_overrides(name, rows):
    """data/overrides.json: per-slug field corrections layered over the CMS rows."""
    try:
        fixes = json.loads((ROOT / "data" / "overrides.json").read_text(encoding="utf-8")).get(name) or {}
    except FileNotFoundError:
        return rows
    for r in rows:
        slug = r.get("slug")
        slug = slug.get("current") if isinstance(slug, dict) else slug
        if slug in fixes:
            r.update(fixes[slug])
    return rows


def load(name):
    return apply_overrides(name, _load(name))


def _load(name):
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


def _street(a):
    """'Home 26, 992 W Frank Ave, Toquerville, UT' -> '992 w frank ave'"""
    a = re.sub(r"^\s*home\s+\d+\s*,\s*", "", (a or "").lower())
    a = a.split(",")[0]
    return re.sub(r"\b(drive|dr)\b\.?", "dr", re.sub(r"\s+", " ", a)).strip()


def mls_listings(sanity):
    """The homes for sale, matched to the live sunriver.com/homes-for-sale MLS feed (data/mls_listings.json).
    A home also in Sanity keeps its photos, gallery, videos and page address; MLS sets price, status and specs."""
    src = json.loads((ROOT / "data" / "mls_listings.json").read_text(encoding="utf-8"))["listings"]
    by_street = {_street(l.get("address")): l for l in sanity}
    by_mls = {l.get("mlsNumber"): l for l in sanity if l.get("mlsNumber")}
    out = []
    for m in src:
        base = dict(by_mls.get(m["mls"]) or by_street.get(_street(m["address"])) or {})
        title = m.get("plan") or base.get("title") or "Single Family"
        addr = "%s%s, %s" % ("Home %d, " % m["lot"] if m.get("lot") else "", m["address"], m["city"])
        slug = base.get("slug") or re.sub(r"[^a-z0-9]+", "-", ("%s %s" % (title, m["address"])).lower()).strip("-")
        base.update({"title": title, "slug": slug, "address": addr, "status": m["status"], "price": m["price"], "askForPricing": False,
                     "squareFootage": m["sqft"], "beds": m["beds"], "baths": m["baths"], "garageSpaces": m["garage"],
                     "hobbyRooms": m.get("hobby", base.get("hobbyRooms") or 0), "community": m["community"], "mlsNumber": m["mls"],
                     "statusDate": base.get("statusDate") or "2026-10-29"})
        if not base.get("photo"):
            base["photo"], base["photoAlt"], base["gallery"] = m["photo"], "%s, %s" % (title, m["address"]), []
        out.append(base)
    print("  homes for sale: %d from the MLS feed (%d matched to Sanity listings)" % (len(out), sum(1 for m in src if by_mls.get(m["mls"]) or by_street.get(_street(m["address"])))))
    return out


def get_all():
    plans = [normalize_plan(p) for p in load("floorPlans")]
    listings = mls_listings(load("homeListings"))
    posts = [p for p in load("posts")
             if p.get("slug") and p.get("title") and not p["title"].startswith("[PENDING") and block_text(p.get("body"))]
    return plans, listings, posts
