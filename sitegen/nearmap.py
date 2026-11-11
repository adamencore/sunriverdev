"""'What's near SunRiver Firelight' map for Live Out, redrawn as an SVG from the sales team's printed flier
(Adam's photo of it, Nov 11 2026). Coordinates are in the flier's own space (1400 x 1050). Places and spellings
follow the flier, with typos fixed. Sky Mountain Golf Course is left off (no golf at SunRiver Firelight)."""

from .lib import esc

ROADS = [
    # I-15
    "M 110 960 L 300 700 L 455 425 C 520 360 590 330 640 300 L 735 220 L 812 50",
    # Toquerville loop (Toquerville Blvd and the old highway)
    "M 790 120 L 800 178 C 790 230 800 270 812 300 C 830 340 805 380 812 430 C 818 470 840 500 915 538",
    "M 800 178 C 830 182 826 230 840 270 C 870 320 900 360 902 420 C 905 470 912 505 915 538",
    # State Street through LaVerkin and Hurricane
    "M 915 538 L 978 610 L 985 662 C 980 720 965 770 935 820 C 915 855 900 880 870 950",
    # SR 9 to Zion
    "M 985 636 L 1075 632 C 1100 600 1120 520 1140 440 C 1155 400 1205 395 1225 430 C 1245 470 1250 520 1300 550 L 1395 575",
    # Hurricane to I-15 (SR 9 west)
    "M 360 962 L 470 940 L 560 918 L 700 902 L 860 892",
]

PINS = [  # (x, y of the pin tip, label, label x, label y, anchor, lines)
    (900, 92, "Kolob Canyon Visitors Center", 918, 76, "start", ["Kolob Canyon", "Visitors Center"]),
    (780, 130, "Sapp Bros Travel Center", 798, 118, "start", ["Sapp Bros", "Travel Center"]),
    (740, 196, "Chief Toquer Reservoir", 706, 214, "start", ["Chief Toquer", "Reservoir"]),
    (442, 404, "Zion Vineyards", 455, 373, "start", None),
    (516, 410, "Casa Tequilana", 528, 412, "start", None),
    (497, 422, "Mainly Pizza", 500, 434, "start", None),
    (170, 672, "Red Cliffs Reserve", 120, 630, "start", None),
    (1333, 506, "Zion National Park", 1300, 532, "start", ["Zion National", "Park"]),
    (1324, 600, "Balcony One", 1272, 614, "start", None),
    (945, 628, "Davis Food & Drug", 928, 624, "end", None),
    (948, 655, "True Value Hardware", 940, 651, "end", None),
    (997, 650, "Maverick", 1010, 654, "start", None),
    (1001, 680, "Family Dollar", 1013, 684, "start", None),
    (937, 702, "El Rancho", 920, 688, "end", None),
    (922, 770, "Stage Coach Grille", 906, 746, "end", None),
    (1012, 746, "Hurricane Valley Fire Station 43", 1022, 744, "start", ["Hurricane Valley", "Fire Station 43"]),
    (984, 786, "Red Fort Cuisine of India", 996, 787, "start", None),
    (897, 816, "River Rock Roasting", 887, 811, "end", None),
    (962, 826, "Zion Canyon Hot Springs", 975, 826, "start", None),
    (862, 858, "Yu Kitchen 3", 876, 864, "start", None),
    (813, 880, "Las Lupitas Mexican Grille", 800, 846, "end", ["Las Lupitas", "Mexican Grille"]),
    (653, 860, "Applebee's", 641, 846, "end", None),
    (620, 882, "Lonny Boy's BBQ", 628, 878, "start", None),
    (505, 868, "Lin's Market", 492, 852, "end", None),
    (536, 896, "Arby's", 550, 881, "start", None),
    (459, 904, "McDonald's", 446, 892, "end", None),
    (862, 906, "Bonrue Bakery", 876, 907, "start", None),
    (858, 946, "Main Street Cafe", 850, 950, "end", None),
    (805, 912, "Pizza Wagon", 766, 914, "start", ["Pizza", "Wagon"]),
    (748, 916, "Taco Bell", 714, 920, "start", ["Taco", "Bell"]),
    (692, 916, "Rooster Run Cafe", 640, 920, "start", ["Rooster", "Run Cafe"]),
    (616, 926, "Cafe Rio", 603, 948, "end", None),
    (516, 936, "Coral Cliffs Cinema", 498, 968, "start", None),
    (455, 937, "Walgreens", 446, 968, "end", None),
    (430, 946, "Jimmy John's", 418, 922, "end", None),
    (406, 952, "Bucks Ace Hardware", 393, 940, "end", None),
]

TOWNS = [("Anderson Junction", 690, 82, ["Anderson", "Junction"]), ("Toquerville", 900, 300, None), ("Leeds", 450, 456, None),
         ("LaVerkin", 860, 590, None), ("Hurricane", 895, 938, None), ("Quail Creek State Park", 380, 742, ["Quail Creek", "State Park"])]


# Driving miles and minutes from the Sales Center (182 Cottonwood Dr, Toquerville). Routed with OpenStreetMap
# (OSRM), Nov 11 2026. Zion National Park uses the 31 minutes the brand quotes. Approximate spots (no exact address
# found): Chief Toquer Reservoir, Mainly Pizza, Yu Kitchen 3, Cafe Rio.
DIST = {
    "Kolob Canyon Visitors Center": ("16.1", 20),
    "Sapp Bros Travel Center": ("3.2", 8),
    "Chief Toquer Reservoir": ("2.8", 6),
    "Zion Vineyards": ("8.8", 16),
    "Casa Tequilana": ("7.3", 12),
    "Mainly Pizza": ("7.3", 12),
    "Red Cliffs Reserve": ("12.2", 26),
    "Zion National Park": ("24", 31),
    "Balcony One": ("9", 15),
    "Davis Food & Drug": ("3.6", 8),
    "True Value Hardware": ("3.6", 8),
    "Maverick": ("3.5", 7),
    "Family Dollar": ("3.6", 7),
    "El Rancho": ("3.7", 7),
    "Stage Coach Grille": ("4", 8),
    "Hurricane Valley Fire Station 43": ("3.8", 8),
    "Red Fort Cuisine of India": ("3.9", 8),
    "River Rock Roasting": ("3.6", 7),
    "Zion Canyon Hot Springs": ("4.7", 10),
    "Yu Kitchen 3": ("6", 12),
    "Las Lupitas Mexican Grille": ("6.6", 13),
    "Applebee's": ("7.1", 14),
    "Lonny Boy's BBQ": ("7.1", 15),
    "Lin's Market": ("7.2", 15),
    "Arby's": ("7.2", 15),
    "McDonald's": ("7.4", 15),
    "Bonrue Bakery": ("6.2", 12),
    "Main Street Cafe": ("6.3", 13),
    "Pizza Wagon": ("6.4", 13),
    "Taco Bell": ("6.5", 13),
    "Rooster Run Cafe": ("6.8", 14),
    "Cafe Rio": ("7", 15),
    "Coral Cliffs Cinema": ("7.2", 15),
    "Walgreens": ("7.5", 16),
    "Jimmy John's": ("7.5", 16),
    "Bucks Ace Hardware": ("6.7", 14),
}


def _text(x, y, anchor, lines, cls):
    if len(lines) == 1:
        return '<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>' % (cls, x, y, anchor, esc(lines[0]))
    tsp = "".join('<tspan x="%s" dy="%s">%s</tspan>' % (x, 0 if i == 0 else "1.1em", esc(l)) for i, l in enumerate(lines))
    return '<text class="%s" x="%s" y="%s" text-anchor="%s">%s</text>' % (cls, x, y, anchor, tsp)


def svg():
    pin = "M0 0 C -4 -9 -11 -14 -11 -22 A 11 11 0 1 1 11 -22 C 11 -14 4 -9 0 0 Z"
    out = ['<svg class="nm-svg" viewBox="60 30 1340 945" role="img" aria-labelledby="nm-title">',
           '<title id="nm-title">Map of shops, restaurants and parks within 5 and 10 miles of SunRiver Firelight</title>',
           '<defs><clipPath id="nm-clip"><rect x="60" y="30" width="1340" height="945" rx="28"/></clipPath>'
           '<path id="nm-pin" d="%s"/></defs>' % pin,
           '<g clip-path="url(#nm-clip)">',
           '<rect x="60" y="30" width="1340" height="945" class="nm-bg"/>',
           '<path class="nm-lake" d="M 302 690 C 330 708 340 728 368 742 C 382 768 368 798 358 828 C 350 856 338 884 323 902 C 308 907 294 893 297 864 C 301 826 289 796 294 766 C 297 736 289 708 302 690 Z"/>']
    out += ['<path class="nm-road-casing" d="%s"/><path class="nm-road" d="%s"/>' % (d, d) for d in ROADS]
    out.append('<path class="nm-arrow" d="M 880 92 C 855 92 845 80 842 64 M 832 74 L 842 62 L 852 74"/>')
    out.append('<path class="nm-arrow" d="M 1310 520 C 1305 490 1320 455 1335 448 M 1324 446 L 1336 446 L 1336 458"/>')
    for name, x, y, lines in TOWNS:
        out.append(_text(x, y, "start" if name not in ("Toquerville", "LaVerkin", "Hurricane") else "start", lines or [name], "nm-town"))
    for x, y, name, lx, ly, anchor, lines in PINS:
        d = DIST.get(name)
        dist = ' data-mi="%s" data-min="%s"' % d if d else ""
        aria = "%s, %s miles away" % (name, d[0]) if d else name
        out.append('<g class="nm-place" data-place="%s"%s tabindex="0" role="button" aria-label="%s">'
                   '<g transform="translate(%s %s)"><g class="nm-pin-g"><circle r="15" cy="-20" class="nm-hit"/><use href="#nm-pin" class="nm-pin"/>'
                   '<circle cy="-22" r="4.2" class="nm-pin-dot"/></g></g>%s</g>' % (
            esc(name), dist, esc(aria), x, y, _text(lx, ly, anchor, lines or [name], "nm-label")))
    out.append('<g class="nm-home" data-home="755 360"><path d="M755 318 L766 345 L795 347 L772 365 L780 393 L755 377 L730 393 L738 365 L715 347 L744 345 Z"/></g>')
    out.append(_text(731, 402, "start", ["SunRiver", "Firelight"], "nm-home-label"))
    out.append('</g></svg>')
    return "".join(out)


def section():
    return '''
    <div class="nm">
      <div class="nm-head"><h3>What's near SunRiver Firelight</h3><p>Groceries, coffee, dinner and Zion, all a short drive from home. Distances are driving miles from the Sales Center.</p></div>
      <div class="nm-map" data-nm-window>
        <div class="nm-stage">%s</div>
        <div class="nm-tip" role="status" aria-live="polite" hidden><strong></strong><span></span></div>
        <div class="nm-ctrl" role="group" aria-label="Map zoom">
          <button type="button" data-nm="in" aria-label="Zoom in">+</button>
          <button type="button" data-nm="out" aria-label="Zoom out">&minus;</button>
          <button type="button" data-nm="fit" class="nm-fit">Fit</button>
        </div>
        <p class="nm-hint"><span class="nm-hint-lg">Drag to move. Double-click or use + and &minus; to zoom. Hover a pin for distance.</span><span class="nm-hint-sm">Drag to move, pinch to zoom, tap a pin</span></p>
      </div>
    </div>''' % svg()
