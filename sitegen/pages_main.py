"""Hand-built pages, matched to the developers' Vercel build (section order, imagery, URLs)
with SunRiver brand rules applied to the copy (SunRiver members, Zion 31 minutes from
SunRiver Firelight, no golf at Firelight, no rates or percentages, no em dashes)."""
from .lib import (FOUNDERS_BADGE, PHONE, PHONE_TEL, S, SQ, V, VP, add, banner, band, btn, chat_section, esc, faq, img,
                  full_hero, photo, photo_hero, sand_hero, simg, star_list, ul, yellow_hero)
from .figma_assets import FG
from .pages_cms import fp_card, min_price, plan_card
from .pages_home import build_home


def split(left, right, cls=""):
    return '<div class="split %s">%s%s</div>' % (cls, left, right)


def build_main(plans, listings):
    by_slug = {p["slug"]: p for p in plans}
    start_price = min_price(plans)
    available = sum(1 for l in listings if l.get("community") == "SunRiver Firelight" and l.get("status") in ("Move in Ready", "For Sale"))

    # ============================================================== HOME (Figma "Home Clark Life NAV 4")
    build_home(plans)


    # ============================================================== WHY SUNRIVER
    communities = [
        ("SunRiver St. George", "/st-george", V("logo-stgeorge.1u9p9bnhl698p.png"), V("card-stgeorge.0a1o_5i7v8oqz.png"),
         "SunRiver St. George is the original development in SunRiver Communities, with a 35,000+ sq ft community center and an 18-hole championship golf course."),
        ("SunRiver Villas", "/villas", V("logo-villas.29yst90kwcult.png"), V("card-villas.16rkj-wtqpn-t.jpg"),
         "The second development of SunRiver Communities, SunRiver Villas is luxury simplified: a smaller, more exclusive community of luxury patio homes."),
        ("SunRiver Firelight", "/sunriver-firelight", V("logo-firelight.06pprl9ewa1sb.png"), V("card-firelight.3g4iz_6s823i2.jpg"),
         "As the newest development of SunRiver Communities, SunRiver Firelight is an exciting new frontier: luxury single family homes and the perfect landing for all things adventure."),
    ]
    comm_html = "".join('''<a class="community-card" href="%s"><div class="community-img">%s</div><div class="community-body">%s<p>%s</p><span class="btn small">Explore Community</span></div></a>''' % (
        h, img(card, "%s homes" % t), img(logo, t, "community-logo"), d) for t, h, logo, card, d in communities)
    clubs = [("Pottery Club", "Have you ever tried pottery? You need the tools, we've got them.", V("club-pottery.3xzlhsr3zozdr.png")),
             ("Pickleball Club", "Try the sport taking the world by storm. The Pickleball Club is one of SunRiver's most popular groups.", V("club-pickleball.2qlhwsq_t2gxw.jpg")),
             ("Bicycle Club", "Get that helmet on and hit the road. Our bicycle club rides all over Southern Utah.", V("club-bicycle.1i1btbq14b2z4.png")),
             ("Motorcycle Club", "Rev the engine and hit the highway with riders who know every back road in Southern Utah.", V("club-motorcycle.3fgfxbblc-re2.png")),
             ("Woodworking Club", "There's something calming about turning organic wood into something you made.", V("club-woodworking.0nsogau55dg0-.png")),
             ("Golf Club", "For gentlemen and ladies alike, golf is best as a social game. Hit the links at SunRiver St. George.", V("club-golf.0a1o_5i7v8oqz.png"))]
    clubs_html = "".join('<div class="photo-card">%s<h3>%s</h3><p>%s</p></div>' % (photo(p, t), t, d) for t, d, p in clubs)
    more_clubs = [("French Conversation Club", "Parlez-vous fran&ccedil;ais? Hone your language skills."), ("Ukulele Circle", "Ready to learn a new instrument? Try the ukulele on for size."),
                  ("Dancin' to the Oldies", "Groove to the songs from back when music was its best."), ("Mahjong", "Sharpen your tactical and observation skills with this classic tile game."),
                  ("Gardening", "Develop a green thumb with the Gardening group."), ("Creative Writing", "Turn your imagination into ideas on the page."),
                  ("Bocce Ball", "Come learn the sport first played in ancient Rome."), ("Model Railroad Club", "Build and design your dream railroads.")]
    more_html = "".join('<div class="amenity"><h3>%s</h3><p>%s</p></div>' % x for x in more_clubs)
    amen = [("Club House", "At the center of the SunRiver community, the clubhouse is a meeting place for friends, neighbors and people you haven't met yet."),
            ("Pickleball", "SunRiver is at the forefront of the pickleball craze, with fully outfitted courts and a thriving club."),
            ("Golf Course", "SunRiver Golf Club, our 18-hole championship course at SunRiver St. George, is just a golf cart ride away."),
            ("Outdoor Theater", "Perfect for dramatic plays and sidesplitting comedies, the outdoor theater makes room for the performing arts."),
            ("Activities", "With countless clubs and social groups, there's always something happening at SunRiver."),
            ("Cooking Classes", "Learn to cook your next favorite recipe with friends in the full-service test kitchen.")]
    amen_html = "".join('<div class="card"><h3>%s</h3><hr class="rule short"><p>%s</p></div>' % x for x in amen)
    cities = [("Las Vegas", "1.5 hours"), ("Salt Lake", "4 hours"), ("Los Angeles", "6 hours"), ("Phoenix", "6 hours"), ("San Diego", "7 hours"), ("Denver", "8 hours")]
    parks = [("Snow Canyon", "15 min"), ("Zion", "45 min"), ("Lake Powell", "2.5 hours"), ("Grand Canyon", "3 hours"), ("Bryce Canyon", "3 hours"), ("W. Yellowstone", "9 hours")]
    dl = lambda rows: '<dl class="distances">%s</dl>' % "".join("<div><dt>%s</dt><dd>%s</dd></div>" % r for r in rows)
    quotes = [("St. George is a great town and SunRiver is wonderful. We absolutely love living here. It's got everything you could need, the weather is fantastic and the people here are very nice. We feel like we're living in a vacation resort!", "Susan L.", "SunRiver member since 2013"),
              ("When we first moved to SunRiver we had no idea just how wonderful it would be. We have made the best possible friends, and feel like we're in our forever home. What a great place to live!", "Margaret and Fred C.", "SunRiver members since 2018")]
    quotes_html = "".join('<figure class="quote"><blockquote>%s</blockquote><figcaption><strong>%s</strong><span>%s</span></figcaption></figure>' % q for q in quotes)
    add("/why-sunriver", "Why SunRiver", "Why choose SunRiver Communities: three 55+ communities in Southern Utah, over 60 clubs and groups, and an amenity for everyone.", "life", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <div class="stack">
      <h2 class="display">Why choose <span class="yellow">SunRiver Communities?</span></h2>
      <hr class="rule">
      <p class="lede">SunRiver Communities is dedicated to vibrant, active lifestyles across three distinctive communities: SunRiver St. George, SunRiver Villas and SunRiver Firelight. Each is designed around exceptional amenities and a strong sense of community.</p>
    </div>
    <div class="stack">
      <div><h3 class="h3">SunRiver St. George</h3><p>The heart of the community is the 35,000+ sq ft community center, connected by walking and cart paths to open areas, a championship golf course, and tennis and pickleball courts.</p></div>
      <div><h3 class="h3">SunRiver Villas</h3><p>Its own exclusive community center with a lap pool, fitness center, test kitchen and computer center, plus access to the SunRiver 18-hole championship golf course.</p></div>
      <div><h3 class="h3">SunRiver Firelight</h3><p>In Toquerville, with innovative home designs, modern comforts and the natural beauty of red rock country. Peace and activity, in balance.</p></div>
      <div>%s</div>
    </div>
  </div>
</section>
<section class="section deep-bg">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Find the home that <span class="yellow">suits you.</span></h2></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
%s
<section class="section">
  <div class="wrap stack-lg">
    <div class="split"><h2 class="display">Clubs &amp; Groups <span class="yellow">at SunRiver</span></h2><p class="lede">SunRiver Communities is home to over 60 clubs and social groups, and new ones start all the time. Indoors, outdoors, physical or social, chances are there's something for you. Have an idea for a club that isn't listed? Start it.</p></div>
    <div class="grid cols-3">%s</div>
    <div class="stack"><h3 class="h3">More clubs at SunRiver</h3><div class="amenities">%s</div></div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">An amenity <span class="yellow">for everyone!</span></h2><hr class="rule center"></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
%s
<section class="section">
  <div class="wrap split">
    <div class="stack"><p class="eyebrow">SunRiver St. George</p><h2 class="display">18 hole championship golf course</h2><hr class="rule">
      <p class="lede">The crown jewel of golf in St. George. Challenging desert terrain, our own PGA golf pro, and a course that's just a golf cart ride from the front doors at SunRiver St. George.</p>
      <div class="btn-row">%s</div></div>
    <div class="photo ratio-43 shadow">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap split wide-text">
    <div class="stack"><h2 class="display">Energy <span class="yellow">efficiency</span></h2><hr class="rule">
      <p class="lede">A comfortable home is a high performing home, and today that means being energy efficient. Since the early 2000s, SunRiver has made energy efficiency a top priority in every new home it builds.</p></div>
    <p>Many homebuyers don't realize how much energy efficiency matters when choosing where to retire. Our energy page explains what makes a home efficient and why it matters to SunRiver members.</p>
  </div>
</section>
%s
<section class="section">
  <div class="wrap split">
    <div class="photo ratio-43">%s</div>
    <div class="stack"><h2 class="display">Area <span class="yellow">attractions</span></h2><hr class="rule">
      <p>St. George is a gateway to superb national parks and natural wonders, and it's close to several major cities. Beach, mountains or the big city: your weekend destination is nearby.</p>
      <div class="grid cols-2"><div class="stack"><h3 class="h3">Close-by cities</h3>%s</div><div class="stack"><h3 class="h3">Close-by parks</h3>%s</div></div>
      <p class="note">Drive times from SunRiver St. George. Zion National Park is 31 minutes from SunRiver Firelight.</p>
    </div>
  </div>
</section>
%s
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Hear it from <span class="yellow">our members</span></h2><hr class="rule center"></div>
    <div class="grid cols-2">%s</div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="photo ratio-43 shadow">%s</div>
    <div class="stack">%s<p class="lede">Need a place to store your RV and other vehicles between adventures? SunRiver has mini storage, covered RV storage and man caves right here in St. George.</p><div class="btn-row">%s</div></div>
  </div>
</section>
%s''' % (photo_hero("", "Why choose SunRiver?", "Three communities. Over 60 clubs and groups. One way of living.", V("hero.1zxyn0xsm69_i.jpg"), "SunRiver members enjoying the outdoors"),
         btn("Talk With A SunRiver Team Member", "/contact-us"), comm_html,
         banner("Beautiful homes, <strong>beautiful life at SunRiver.</strong>", V("beautiful-homes.3nspyj3umtcic.jpg"), btn("See Our Home Designs", "/floor-plans"), True),
         clubs_html, more_html, amen_html, band(V("cc-exterior.0ufveyw_xw2e8.jpg"), "The SunRiver St. George community center"),
         '<a class="btn" href="https://www.sunrivergolf.com/">Learn More</a>', img(V("golf-banner.154wsobedbefq.jpg"), "SunRiver Golf Club fairway"),
         banner("Save <strong>while you save</strong>", V("energy-band.2om6a87nh9cox.png"), btn("Learn About Our Energy Efficient Homes", "/energy"), True),
         img(V("area-attractions.27g-2mrv4a84e.png"), "Red rock landscape near St. George"), dl(cities), dl(parks),
         banner("Beauty <strong>all around</strong>", V("beauty-band.1lup9pnv-v6wk.jpg"), btn("Learn About Southern Utah", "/southern-utah"), True),
         quotes_html, img(V("storage-photo.2cjrewvecpfj2.jpg"), "Covered RV storage at Adventure Storage"),
         img(V("adventure-storage-logo.2nuk60xxu39gw.png"), "Adventure Storage", "storage-logo"), '<a class="btn" href="https://www.adventurestorage.info/">Learn More</a>',
         chat_section()))

    # ============================================================== FIND A HOME
    find_comm = [
        ("SunRiver Villas", "/villas", V("logo-villas.2spd35ri4p34_.png"), V("card-villas.3ij3vmkyez9ep.png"), "Our latest community featuring luxury patio homes", "", ("Homes for Sale", "/homes-for-sale")),
        ("SunRiver Firelight", "/sunriver-firelight", V("logo-firelight.3r9_zvrixrchn.png"), V("card-firelight.3s9-nzz50zfg3.jpg"), "Our newest community featuring new single family homes", start_price, ("Floor Plans", "/floor-plans")),
        ("SunRiver St. George", "/st-george", V("logo-stgeorge.06euqq55p6vjl.png"), V("card-stgeorge.3v7aeoytroq-i.jpg"), "Our first community featuring beautifully designed homes", "", ("Homes for Sale", "/homes-for-sale")),
    ]
    fc_html = "".join('''<div class="community-card on-sand"><div class="community-img">%s</div><div class="community-body">%s<p>%s</p>%s<div class="btn-row">%s%s</div></div></div>''' % (
        img(card, "%s homes" % t), img(logo, t, "community-logo"), d, '<p class="starting">Starting at <strong>%s</strong></p>' % sp if sp else "",
        btn("Explore Community", h, "small"), btn(l2[0], l2[1], "small blue-btn")) for t, h, logo, card, d, sp, l2 in find_comm)
    # Figma OFFICIAL "Homes for Sale / Model Homes" (6:206): photo hero with the Founders tab, every floor plan as a
    # card, then the two big link cards. The sections after that are carried over from the Netlify build.
    hfs_pick = next((l for l in sorted(listings, key=lambda l: l.get("status") != "Move in Ready") if l.get("photo") and l.get("community") == "SunRiver Firelight"), None)
    hfs_img = simg(hfs_pick["photo"], "A SunRiver Firelight home for sale", 998, sizes="(max-width: 600px) 100vw, 499px") if hfs_pick else img(V("parade-home.05ayhbavvyl2k.jpg"), "A SunRiver Firelight home for sale")
    add("/find-a-home", "Find a Home", "Find your home at SunRiver Firelight: %d floor plans starting at %s and %d homes available now." % (len(plans), start_price, available), "homes-overlay", '''
<section class="fah-hero">
  %s
  <div class="wrap fah-hero-inner">
    <h1>Find your home at SunRiver Firelight</h1>
    <p>New home sales are focused at<br> SunRiver Firelight in Toquerville.<br> Jump straight to what you&rsquo;re looking for.</p>
  </div>
</section>
<section class="fah-plans">
  <div class="wrap">
    <h2 class="visually-hidden">SunRiver Firelight floor plans</h2>
    <div class="fp-grid">%s</div>
  </div>
</section>
<section class="fah-links">
  <div class="wrap fah-links-grid">
    <a class="fl-card" href="/floor-plans"><span class="fl-img">%s</span><span class="fl-bar"><span class="fl-kicker">%d unique</span><span class="fl-title">Floor Plans</span><span class="fl-arrow" aria-hidden="true"></span></span></a>
    <a class="fl-card tall" href="/homes-for-sale"><span class="fl-img">%s</span><span class="fl-bar"><span class="fl-kicker">%d available now</span><span class="fl-title">Homes for Sale</span><span class="fl-btn">View all homes for sale</span></span></a>
  </div>
</section>
''' % (img(FG("fah-hero"), "SunRiver Firelight homes with red rock mesas behind them", "fah-hero-img", "eager"),
         "".join(fp_card(p) for p in plans), img(FG("fah-card"), "A SunRiver Firelight model home"), len(plans), hfs_img, available) + '''
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Find the community <span class="yellow">that fits you</span></h2><hr class="rule center"></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
<section class="founders-band">%s
  <div class="wrap split">
    <div class="stack"><p class="eyebrow">SunRiver Firelight Founders Club</p><h2 class="display">Be part of history at SunRiver Firelight</h2>
      <p class="lede">Become a member of the SunRiver Firelight Founders Club and be among the first 74 homeowners to help shape this new community.</p><div class="btn-row">%s</div></div>
    <div class="badge-wrap">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap split">
    <div class="stack"><h2 class="display">No mortgage payments <span class="yellow">for life!*</span></h2><hr class="rule">
      <p class="lede">See how you could qualify to own a brand new SunRiver home and never make another mortgage payment.</p>
      <p class="note">*HECM FHA insured mortgage. Must be 62 or older to qualify. Program details are provided by Brandon Hansen of Cherry Creek Mortgage.</p>
      <div class="btn-row">%s</div></div>
    <div class="photo ratio-43 shadow">%s</div>
  </div>
</section>
%s
<section class="section">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="h2">View our latest SunRiver Villas community commercial</h2><hr class="rule center"></div>
    <div class="embed narrow-embed"><iframe src="https://player.vimeo.com/video/350204945" title="SunRiver Villas community commercial" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>
  </div>
</section>
%s''' % (fc_html,
         img(V("founders-band.41tlj-oascbvv.jpg"), "", "founders-bg"), btn("Learn more", "/founders-club"), img(FOUNDERS_BADGE, "SunRiver Firelight Founders Club badge"),
         btn("Learn More", "/no-mortgage-payments-for-life"),
         img(V("no-mortgage.1br4wnm6v72gl.jpg"), "Brandon Hansen with SunRiver members"),
         banner("The grass is <strong>greener!</strong>", V("golf-band.3n4euz5zc69-k.jpg"), '<a class="btn" href="https://www.sunrivergolf.com/">Explore SunRiver Golf Course</a>', True),
         chat_section()))

    # ============================================================== ABOUT
    add("/about", "About", "SunRiver Communities is Utah's premier 55+ active adult community builder, established in 1998.", "about", '''
%s
<section class="section">
  <div class="wrap narrow stack center">
    <h2 class="display">SunRiver is Utah's premier 55+ active adult <span class="yellow">community builder</span></h2>
    <hr class="rule center">
    <p class="lede">Established in 1998, SunRiver Communities has become a focal point for resort-style living in the greater St. George area. For more than twenty years, wide open spaces and easy breezes have made SunRiver home for thousands of members. Today there are three communities, the original SunRiver St. George, SunRiver Villas and the new SunRiver Firelight in Toquerville, with an amenity and a lifestyle for everyone ready to live young.</p>
  </div>
</section>
<section class="section sand tight">
  <div class="wrap stats">
    <div class="stat"><strong>1998</strong><span>SunRiver was founded with a vision of an active adult community.</span></div>
    <div class="stat"><strong>2,600+</strong><span>Homes built for SunRiver members.</span></div>
    <div class="stat"><strong>60+</strong><span>Clubs and groups, and growing.</span></div>
  </div>
</section>
<section class="section">
  <div class="wrap stack-lg center">
    <div class="photo shadow team-photo">%s</div>
    <div>%s</div>
  </div>
</section>
%s
%s''' % (yellow_hero("A team with <strong>vision</strong>", "/about", V("hero.1zxyn0xsm69_i.jpg"), "SunRiver members enjoying the outdoors"), img(V("team.1kwlwm69zlbnz.png"), "The SunRiver Communities team"),
         btn("Contact Us", "/contact-us"), band(V("aerial.3dl3zwtjejebp.jpg"), "Aerial view of SunRiver and the surrounding red rock country"), chat_section()))

    # ============================================================== HISTORY
    tl = [("1998", "Construction Begins", "Construction begins on the first homes, and eight new model homes and the Sales Center are completed.", V("1998-construction.14k7dqwbgy9yi.jpg")),
          ("1999", "Community Center", "The Community Center celebrates its Grand Opening.", V("1999-community-center.0eeg3p_lul9-e.jpg")),
          ("2002", "Golf Course", "The SunRiver golf course opens and is ready for play.", V("2002-golf-course.2_gj2x6dp904b.jpg")),
          ("2005", "Community Center Expansion", "The Community Center expansion opens with a ballroom, outdoor pool, library, and game and multi-purpose rooms.", None),
          ("2006", "1000th Home", "SunRiver sells its 1000th home to Craig and Deanna Hall, and the Reflections gated community opens.", V("2006-1000th-home.4258sbh8qzwn8.jpg")),
          ("2016", "SunRiver Villas", "SunRiver Villas begins: a new active adult resort community with its own community center.", V("2016-villas.0gwincf_04c2m.jpg")),
          ("2018", "Hampton Inn &amp; Suites", "Hampton Inn &amp; Suites at SunRiver opens with a well-attended Grand Opening.", V("2018-hampton-inn.16s935p4q0_01.jpg")),
          ("2022", "SunRiver Firelight", "SunRiver announces plans for a 1,200+ home community in Toquerville, Utah, the gateway to Zion National Park.", V("2022-firelight.3c2h6miza7eiz.png"))]
    tl_html = "".join('<li class="tl-row"><div class="tl-year">%s</div><div class="tl-content"><h3>%s</h3><p>%s</p></div>%s</li>' % (
        y, t, d, '<div class="tl-img">%s</div>' % img(p, "%s, %s" % (t, y)) if p else '<div class="tl-img empty"></div>') for y, t, d, p in tl)
    add("/history", "History", "The history of SunRiver Communities, from the first homes in 1998 to SunRiver Firelight in Toquerville.", "about", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <div class="stack"><h2 class="display">20 years young <span class="yellow">and counting</span></h2><hr class="rule"></div>
    <div class="stack">
      <p class="lede">The vision for SunRiver St. George began when some of Las Vegas stockbroker Darcy Stewart's clients invited him to a play at Sun City, Nevada. He noticed the people there were having fun and actually enjoying retirement.</p>
      <p>Seeing happy, active retirees sparked a dream: an active adult golf course community his father would enjoy living in. Instead of placing it in a metropolitan area of millions, he pictured a small city with every amenity members would want within reach and none of the traffic. With that vision, and 690 acres of dusty desert just south of Bloomington, SunRiver St. George was born.</p>
    </div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Our <span class="yellow">History</span></h2><hr class="rule center"></div>
    <ol class="history">%s</ol>
  </div>
</section>
%s''' % (yellow_hero("A team with <strong>experience</strong>", "/history", V("cc-exterior.0ufveyw_xw2e8.jpg"), "The SunRiver St. George community center"), tl_html, chat_section()))

    # ============================================================== SOUTHERN UTAH
    dest = [("Zion National Park", "The most majestic national park in Utah, just 31 minutes from SunRiver Firelight.", V("zion.3lmfdu4qx4jcf.png")),
            ("Las Vegas", "Shows, dining and a weekend away, about 90 minutes from SunRiver.", V("las-vegas.3na-wjrysew92.png")),
            ("Bryce Canyon", "Crimson hoodoos, the spire-shaped rock formations you won't see anywhere else.", V("bryce.3wvrrj9gm1xpt.png")),
            ("Tuacahn", "Broadway in the desert, in a stunning amphitheater set inside a red rock canyon.", V("tuacahn.0kqgs0dzsldk7.png")),
            ("Moab", "Home to Arches National Park, Delicate Arch, Balanced Rock and Devils Garden.", V("moab.0znw55-q9vii6.png")),
            ("Snow Canyon", "Right in St. George's backyard, the area's most popular state park and a perfect place to hike.", V("snow-canyon.0klzvey5gqkxa.png")),
            ("Lake Powell", "Rent a houseboat with friends on the border of Utah and Arizona and unwind.", V("lake-powell.010uva9_3k1ge.png")),
            ("Shakespeare Festival", "Every summer in Cedar City, the Tony Award-winning festival stages world-class theater.", V("shakespeare.1kcokbih9lyah.png")),
            ("Grand Canyon", "One of the Seven Natural Wonders of the World, a few hours from St. George.", V("grand-canyon.0h96i5x02d6f4.png"))]
    dest_html = "".join('<div class="photo-card">%s<h3>%s</h3><p>%s</p></div>' % (photo(p, t), t, d) for t, d, p in dest)
    add("/southern-utah", "Southern Utah", "Southern Utah around SunRiver: Zion, Snow Canyon, Tuacahn, Bryce Canyon and more, all within reach.", "about", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <h2 class="display">North of the border, south of heaven, <span class="yellow">right where you belong.</span></h2>
    <p class="lede">Known for near year-round sunshine, Washington County sits in the heart of Southern Utah's Color Country. Red rock vistas, warm desert temperatures and open space make SunRiver an ideal basecamp. SunRiver St. George hosts an annual art festival, golf tournaments throughout the year and portions of the Huntsman World Senior Games.</p>
  </div>
</section>
<section class="section sand" id="destinations">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Beauty as far as <span class="yellow">the eye can see.</span></h2><hr class="rule center"></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
%s
%s''' % (yellow_hero("Explore <strong>Southern Utah</strong>", "/southern-utah", V("beauty-band.1lup9pnv-v6wk.jpg"), "Red rock country in Southern Utah"), dest_html,
         banner("Have more questions? <strong>Let's talk!</strong>", V("aerial.3dl3zwtjejebp.jpg"), btn("Contact Us", "/contact-us")), chat_section()))

    # ============================================================== FAQ
    local = [
        ("What is the weather like in Southern Utah?", "<p>Washington County has mild, low humidity winters and over 300 sunny days a year. The desert climate and 2,760 foot elevation support year-round recreation, including golf, tennis, fishing, water sports, hiking and bicycling.</p>"),
        ("What is the population of Washington County?", "<p>Washington County, including St. George, Hurricane, Santa Clara and Ivins, had a population of 197,680 in 2022.</p>"),
        ("What is the cost of living in Washington County?", "<p>The cost of living in Washington County is generally lower than the national average, with housing, utilities and health care standing out.</p>"),
        ("What outdoor activities are there in Washington County?", "<p>Washington County is a gateway to Arches, Bryce Canyon, Capitol Reef, Canyonlands, Grand Canyon, Zion and Lake Powell, plus many state parks. Red rock trails, three reservoirs, parks, sports complexes, indoor and outdoor pools and 13 public and private golf courses make it easy to stay active all year.</p>"),
        ("What is the predominant religion among SunRiver members and in Washington County?", "<p>About half of SunRiver members come from 20 different states outside the West, so religious affiliations are more diverse than in much of Southern Utah. The Church of Jesus Christ of Latter-day Saints is the predominant religion in Washington County, and other faiths are well represented.</p>"),
        ("What is the crime rate in Washington County?", "<p>Crime is generally very low in St. George, with violent and property crime rates in Washington County well below the national average.</p>"),
        ("What is there to do for evening entertainment?", "<p>St. George offers more entertainment than many larger cities. Tuacahn Center for the Arts stages Broadway in the Desert each summer and concerts year-round. The Tony Award-winning Utah Shakespeare Festival runs June into October in Cedar City. The O.C. Tanner Amphitheater hosts a summer concert series against red canyon walls, and local theater companies, Utah Tech University's fine arts center and area high schools stage strong productions.</p><p>St. George also has multi-screen movie theaters, bowling and miniature golf. Las Vegas is about 90 minutes away and Mesquite, Nevada about 30.</p>"),
    ]
    clubs_list = "American Legion, Auxiliary, Bingo, Bridge, Canasta, Chess, Hand and Foot, Mexican Train, Dominoes, Pinochle, Texas Cards, Computer Club, Arts and Crafts, Beading, Carving, Dance, Casual Dining, Dog Park, Genealogy, Couples Golf, Ladies Golf, Investment, Library, Meditation, Jam Sessions, SunRiver Singers, Photography, Red Hatters, Science, Singles, Social, Bicycle, Bocce Ball, Bowling, Hiking, Horseshoes, Lawn Bowling, Pickleball, Table Tennis, Theater, RV Club".split(", ")
    facilities = "Ballroom, Billiard Room, Community Center, Computer Lab, Fitness Room, Game Room, Horseshoe Pits, Lapidary Center, Lawn Bowling, Library, Multi-Purpose Room, Pickleball Courts, Pools, Pottery Studio, Tennis Courts, Woodworking Shop".split(", ")
    tags = lambda xs: '<ul class="tag-list">' + "".join("<li>%s</li>" % c for c in xs) + "</ul>"
    stg = [
        ("What clubs and activities are available at SunRiver St. George?", "<p>There's a club for virtually every interest, and new clubs keep forming.</p>" + tags(clubs_list)),
        ("Are pets allowed?", "<p>Yes. Domestic animals are welcome, and SunRiver St. George even has a dog park.</p>"),
        ("Does SunRiver St. George have a homeowners association?", "<p>Yes. SunRiver St. George HOA dues are $172 per month. Homes in the Reflections gated community have additional private amenities, with an additional $70 per month in dues.</p><p>SunRiver St. George HOA, 4275 Country Club Drive, St. George, UT 84790. Phone (435) 287-3061. <a href=\"https://pmprollc.com\">pmprollc.com</a></p>"),
        ("What do the HOA dues cover at SunRiver St. George?", "<p>Dues cover maintenance of all front yards, common areas, the community center, pool, sports courts and other amenities, plus association staffing and management.</p><p>Members may add rear yard maintenance for $54 per month or request walking mowers instead of riding mowers for $10 per month. Plant maintenance, irrigation repairs and rock refresh are available as needed for one-time fees.</p>"),
        ("What are the CC&amp;Rs?", "<p>SunRiver St. George is subject to Covenants, Conditions and Restrictions that are actively enforced to keep a happy, healthy, beautiful environment for every SunRiver member.</p>"),
        ("What facilities are at the SunRiver St. George Community Center?", "<p>A full array of amenities:</p>" + tags(facilities)),
        ("Is the SunRiver Golf Club a public course?", "<p>Yes. The SunRiver Golf Course at SunRiver St. George is public, with preferential rates and tee times for SunRiver members. The SunRiver Men's and Ladies' Golf Associations are active and always welcome new players. Call the Pro Shop at (435) 986-1000 for information or a tee time.</p>"),
        ("What are the green fees at the SunRiver Golf Club?", "<p>St. George is known for affordable golf, and SunRiver Golf Course is no exception. Call the Pro Shop at (435) 986-1000 for current fees.</p>"),
    ]
    add("/faq", "FAQ", "Answers about SunRiver Communities, Washington County, HOA dues, clubs and the SunRiver Golf Club.", "about", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <h2 class="display">You've got questions? <span class="yellow">We've got answers.</span></h2>
    <p class="lede">SunRiver is a hub of activity for the greater St. George area, from the annual kite festival and art festival to golf tournaments and portions of the Huntsman World Senior Games.</p>
  </div>
</section>
<section class="section sand">
  <div class="wrap narrow stack-lg">
    <div class="faq-group"><h2 class="h2">Local area</h2>%s</div>
    <div class="faq-group"><h2 class="h2">SunRiver St. George</h2>%s</div>
  </div>
</section>
%s''' % (yellow_hero("A team with <strong>answers</strong>", "/faq", V("neighborhood-walk.2u4xr239zlka_.jpg"), "SunRiver members walking through the neighborhood"), "".join(faq(q, a) for q, a in local), "".join(faq(q, a) for q, a in stg), chat_section()))

    # ============================================================== SUNRIVER FIRELIGHT
    mix = [("Brand New Homes", "Customize the location and design of your dream home."),
           ("Outdoor Living", "In the heart of Southwest Utah, SunRiver Firelight puts the region's natural wonders at your doorstep."),
           ("Prime Location", "Just 15 minutes from downtown St. George, with easy access to the city when you want it."),
           ("Designed For You", "Spacious homes with three and four car garages, with room for the bikes, kayaks and gear you love."),
           ("Mild Seasons", "Cooler temperatures than St. George, without the hassle of snow."),
           ("Community", "SunRiver is more than a place to live. It's a community of people who refuse to slow down.")]
    mix_html = "".join('<div class="star-item"><h3>%s</h3><p>%s</p></div>' % x for x in mix)
    fl_clubs = [("Hiking Club", V("club-hiking.3s1-w8hg6a1nh.jpg")), ("Yoga Club", V("club-yoga.0jzome1ix55zy.jpg")),
                ("Bicycle Club", V("club-bicycle.1i1btbq14b2z4.png")), ("Pickleball Club", V("club-pickleball.3iqae91xix18y.jpg"))]
    fl_clubs_html = "".join('<div class="photo-card">%s<h3>%s</h3></div>' % (photo(p, "SunRiver members, %s" % t, "ratio-34"), t) for t, p in fl_clubs)
    week = [("Monday", "Chair Yoga", V("week-yoga.2bdtfft43esgw.jpg")), ("Tuesday", "Outdoor Concert", V("week-concert.2_hct2pei-rk2.jpg")),
            ("Wednesday", "Pickleball Club", V("week-pickleball.3iqae91xix18y.jpg")), ("Thursday", "Club Pool Party", V("week-pool.405xnpp6542w2.jpg")),
            ("Friday", "Zion Tour", V("week-hike.13z6azl5t3od2.jpg"))]
    week_html = "".join('<div class="day">%s<span class="dname">%s</span><span class="act">%s</span></div>' % (photo(p, t, ""), d, t) for d, t, p in week)
    fl_amen = [("The Clubhouse", "At the heart of SunRiver Firelight will be the 17,000+ sq ft Clubhouse, the hub for social, recreational and wellness activities. Fitness rooms, event spaces and dedicated areas for hobbies and clubs give members a place to stay active, meet new friends and join community events.", V("amenity-clubhouse.1s09xtqihpiiw.jpg")),
               ("Swimming Pool", "SunRiver Firelight members will enjoy a 4,000 sq ft swimming pool for laps, sunning on the deck or a poolside gathering with neighbors.", V("amenity-pool.3xoam7a_jzu33.jpg")),
               ("Pickleball Arena", "Designed for players of every level, the Pickleball Arena will have dedicated courts for daily play, friendly competition and conversation after the game.", V("amenity-pickleball.2602yc92h05vt.jpg"))]
    fl_amen_html = "".join('<div class="split amen-row%s"><div class="photo ratio-32 shadow">%s</div><div class="stack"><h3 class="h2">%s</h3><hr class="rule short"><p class="serif big-serif">%s</p></div></div>' % (
        " flip" if i % 2 else "", img(p, t), t, d) for i, (t, d, p) in enumerate(fl_amen))
    ev = by_slug.get("evergreen") or plans[0]
    add("/sunriver-firelight", "SunRiver Firelight", "SunRiver Firelight in Toquerville, Utah: SunRiver's newest 55+ community puts Zion National Park in your backyard.", "life", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <div class="stack">
      <p class="eyebrow">Live A Little Closer</p>
      <h2 class="display">SunRiver Firelight</h2>
      <hr class="rule">
      <p class="lede">As the newest development of SunRiver Communities, SunRiver Firelight is an exciting new frontier: luxury single family homes and the perfect landing for all things adventure. With Springdale and Zion National Park nearby, you'll wonder how you ever lived anywhere else.</p>
      <p>With the new 17,000+ sq ft Clubhouse on the way and miles of outdoor trails, you'll never want to leave. #liveyoung</p>
    </div>
    <div class="badge-wrap">%s</div>
  </div>
</section>
%s
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="serif-display">Just the right <span class="yellow">mix</span></h2></div>
    <div class="star-grid">%s</div>
    <div class="center">%s</div>
  </div>
</section>
%s
<section class="section tight">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="h2">Live a little closer</h2><hr class="rule center"></div>
    <div class="drive-times">
      <div><strong>15</strong><span>Minutes to St. George</span></div>
      <div><strong>20</strong><span>Minutes to Cedar City</span></div>
      <div><strong>31</strong><span>Minutes to Zion National Park</span></div>
    </div>
    <p class="center lede" style="margin-inline:auto">Flowing through SunRiver Firelight is the new Toquerville Parkway, with direct access to I-15 and Zion National Park, and a beautiful new Clubhouse just for SunRiver members.</p>
  </div>
</section>
<section class="section deep-bg">
  <div class="wrap stack-lg">
    <div class="split"><div class="stack"><p class="eyebrow">So much time, so much to do!</p><h2 class="display">Lifestyle</h2></div><p class="lede">Come join one of our many clubs.</p></div>
    <div class="grid cols-4">%s</div>
  </div>
</section>
<section class="section">
  <div class="wrap stack-lg">
    <div class="center stack"><p class="eyebrow">Over 60 clubs &amp; groups</p><h2 class="h2">A week at SunRiver Firelight</h2><hr class="rule center"></div>
    <div class="week">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Amenities</h2><hr class="rule center"></div>
    %s
  </div>
</section>
%s
<section class="section">
  <div class="wrap split">
    <div class="stack"><p class="eyebrow">Phase 1 &amp; 2</p><h2 class="display">Phase 1 &amp; 2 homesites</h2><hr class="rule">
      <p class="lede">Choose your homesite and build the home instead of just buying it. A sales agent can walk you through what is available today.</p>
      <div class="btn-row">%s</div></div>
    <a class="photo shadow" href="%s" data-lightbox>%s</a>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Homes</h2><hr class="rule center"></div>
    <div class="grid cols-3 homes-trio">
      <div class="photo ratio-34 shadow">%s</div>
      <div class="photo ratio-34 shadow">%s</div>
      <div class="stack"><p class="eyebrow">Featured floor plan</p>%s<div class="btn-row">%s</div></div>
    </div>
  </div>
</section>
%s
%s''' % (photo_hero("", "SunRiver's newest community puts Zion in your backyard.", "", V("hero.2h_vl62bxoy8t.jpg"), "SunRiver Firelight homes with red rock mountains behind", btn("Talk with an Agent", "/contact-us")),
         img(V("badge.3uv840yemxfy7.png"), "SunRiver Firelight badge"),
         band(V("clubhouse-rendering.1ka003naw87xl.jpg"), "Rendering of the SunRiver Firelight Clubhouse"), mix_html, btn("Contact Sales Today", "/contact-us"),
         band(V("grand-view.0qm1t8yvr616g.png"), "Grand view of SunRiver Firelight and the surrounding red rock country"),
         fl_clubs_html, week_html, fl_amen_html,
         banner("Phase 1 &amp; 2 homesites, <strong>March 2026</strong>", V("homesites-aerial.0o-k9ic3-z5oy.jpg"), tall=True),
         btn("Contact a Sales Agent Today", "/contact-us"), V("site-map.0x3u4v7ysjd38.jpg"), img(V("site-map.0x3u4v7ysjd38.jpg"), "Site map of SunRiver Firelight Phase 1 and 2 homesites, model homes and Clubhouse"),
         img(V("couple-couch.00eu4vj9i0gdx.jpg"), "SunRiver members relaxing at home"), img(V("couple-front.24z3-z26uive0.jpg"), "SunRiver members in front of their SunRiver Firelight home"),
         plan_card(ev), btn("Explore More Plans", "/floor-plans", "blue-btn"),
         banner("Looking for something <strong>more immediate?</strong>", V("parade-home.05ayhbavvyl2k.jpg"), btn("Explore Homes For Sale", "/homes-for-sale"), True),
         chat_section()))

    # ============================================================== ST. GEORGE
    stg_amen = [("Golf Course", "Our 18-hole championship course is just a golf cart ride away."), ("Fitness", "A fully stocked fitness center and fitness classes free to members."),
                ("Swimming", "An indoor lap pool plus an outdoor swimming pool and spa."), ("Pickleball", "14 pickleball courts and a thriving club. Come play with us."),
                ("Restaurant", "Guru's Sports Bar and Grill, one of St. George's best dining options."), ("Dog Park", "A place for your four-legged friends to play. SunRiver loves pets."),
                ("Lawn Bowling", "A large lawn bowling field for enthusiasts and first-timers."), ("Trailhead", "A trail that runs from SunRiver throughout sunny St. George."),
                ("Pottery", "A big pottery and lapidary studio next to the woodworking shop."), ("Woodworking", "A full service woodworking studio. Come get your hands dirty."),
                ("Tennis", "Multiple tennis courts next to the pickleball courts."), ("Walking Paths", "Convenient walking loops scattered throughout the community."),
                ("Horseshoes", "Plenty of space for a friendly game of horseshoes."), ("Pool Room", "Play a few rounds in the community center pool room."),
                ("Basketball", "A half court for when you're ready to work up a sweat.")]
    stg_amen_html = "".join('<div class="star-item"><h3>%s</h3><p>%s</p></div>' % x for x in stg_amen)
    peek = [(V("cc-exterior.0ufveyw_xw2e8.jpg"), "Community center exterior"), (V("cc-hallway.1q5jw6mq4fj0s.jpg"), "Community center hallway"),
            (V("cc-dining.3xb8l1r1bvj23.jpg"), "Community center dining area"), (V("cc-billiards.1qmjemn1vq503.jpg"), "Community center billiards room")]
    peek_html = "".join(photo(p, a, "") for p, a in peek)
    stg_clubs = [("Pottery Club", "Have you ever tried pottery? You need the tools, we've got them.", V("club-pottery.3b4_sjk07gaqp.jpg")),
                 ("Bicycle Club", "Get that helmet on and hit the road. Our bicycle club rides all over Southern Utah.", V("club-bicycle.1zgkikb7b_8hu.jpg")),
                 ("Motorcycle Club", "Rev the engine and hit the highway with riders who know every back road.", V("club-motorcycle.41yxh2688w-4s.jpg")),
                 ("Woodworking Club", "There's something calming about turning organic wood into something you made.", V("club-woodworking.0nsogau55dg0-.jpg")),
                 ("Golf Club", "For gentlemen and ladies alike, golf is best as a social game. Hit the links with us.", V("club-golf.0mu0lz830f8ds.jpg"))]
    stg_clubs_html = "".join('<div class="photo-card">%s<h3>%s</h3><p>%s</p></div>' % (photo(p, t), t, d) for t, d, p in stg_clubs)
    resale = lambda name: '''<section class="section">
  <div class="wrap narrow center stack">
    <h2 class="display">Looking for a new <span class="yellow">SunRiver home?</span></h2><hr class="rule center">
    <p class="lede">New home sales are now focused at SunRiver Firelight in Toquerville. Member resales in %s appear on our Homes for Sale page as they become available.</p>
    <div class="btn-row" style="justify-content:center">%s%s</div>
  </div>
</section>''' % (name, btn("Explore SunRiver Firelight", "/sunriver-firelight"), btn("Homes for Sale", "/homes-for-sale", "blue-btn"))
    add("/st-george", "SunRiver St. George", "SunRiver St. George, the original 55+ active adult community from SunRiver Communities, established in 1998.", "life", '''
%s
<section class="section">
  <div class="wrap narrow center stack">
    <p class="eyebrow">Our First Community</p>
    <h2 class="display">SunRiver St. George</h2>
    <hr class="rule center">
    <p class="lede">Established in 1998 and nearing completion, SunRiver St. George is the original SunRiver community. With a 35,000+ sq ft community center, an 18-hole championship golf course, a restaurant and over 60 clubs and social groups, it has become a thriving community that embodies resort-style, active adult living. SunRiver members have access to all of it, along with the friendships and quality of life that come with it.</p>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">An amenity <span class="yellow">for everyone</span></h2><hr class="rule center"></div>
    <div class="star-grid">%s</div>
  </div>
</section>
<section class="section">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="h2">A peek inside the Community Center</h2><hr class="rule center"></div>
    <div class="gallery">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">The right club <span class="yellow">for you!</span></h2><hr class="rule center"></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
%s
%s''' % (photo_hero("SunRiver St. George", "Where it all started.", "The original SunRiver community, established in 1998.", V("cc-exterior.0ufveyw_xw2e8.jpg"), "The SunRiver St. George community center"),
         stg_amen_html, peek_html, stg_clubs_html, resale("SunRiver St. George"), chat_section()))

    # ============================================================== VILLAS
    vil_amen = [("Club House", "Separate from SunRiver St. George, the 5,000 sq ft clubhouse is the private center of the SunRiver Villas community."),
                ("Lap Pool", "Just outside the clubhouse, the lap pool is ideal for staying active, cooling off and relaxing in the St. George sun."),
                ("Fitness Center", "The clubhouse includes an exclusive, state-of-the-art fitness center."),
                ("Pickleball", "SunRiver Villas has two pickleball courts of its own, right next to the clubhouse."),
                ("Golf Course", "SunRiver's 18-hole championship golf course is a short cart ride away."),
                ("Test Kitchen", "Host large meals, cooking demonstrations, classes and other culinary get-togethers.")]
    vil_amen_html = "".join('<div class="star-item"><h3>%s</h3><p>%s</p></div>' % x for x in vil_amen)
    vil_clubs = ["<strong>Bike Club.</strong> Ready to get back on the bike and enjoy the scenery? Join the bike club.",
                 "<strong>Horseshoes.</strong> A horseshoe area to play with your friends.",
                 "<strong>Bocce Ball.</strong> Haven't tried bocce? Come learn the sport first played in ancient Rome.",
                 "<strong>Dog Park.</strong> A place for your four-legged friends to play.",
                 "<strong>Yoga Club.</strong> Find your practice with the help of the yoga club."]
    add("/villas", "SunRiver Villas", "SunRiver Villas: luxury patio homes with a private clubhouse, lap pool, fitness center and test kitchen in St. George, Utah.", "life", '''
%s
<section class="section">
  <div class="wrap narrow center stack">
    <p class="eyebrow">The Simple Life</p>
    <h2 class="display">SunRiver Villas</h2>
    <hr class="rule center">
    <p class="lede">The second development of SunRiver Communities, SunRiver Villas is luxury simplified. This community of luxury patio homes is smaller and more exclusive, with a modern community center, a lap pool, fitness center, test kitchen and computer center, plus access to SunRiver's 18-hole championship golf course. Just turn the key and you're home.</p>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">An amenity <span class="yellow">for everyone</span></h2><hr class="rule center"></div>
    <div class="star-grid">%s</div>
    <div class="grid cols-3">%s%s%s</div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="stack">
      <h2 class="display">A community that loves to <span class="yellow">get together</span></h2><hr class="rule">
      <p class="lede">From live concerts at the community center to clubs for nearly every interest, the SunRiver Villas keep the calendar full.</p>
      %s
    </div>
    <div class="grid cols-2"><div class="photo ratio-34 shadow">%s</div><div class="photo ratio-34 shadow">%s</div></div>
  </div>
</section>
%s
%s''' % (photo_hero("SunRiver Villas", "The simple life, done well.", "Luxury patio homes with a private clubhouse in St. George.", V("hero-golf-cart.0rtq3isd-80lt.jpg"), "A smiling couple riding in a golf cart at SunRiver Villas"),
         vil_amen_html, photo(V("cc-1.1p47nj6_u330q.jpg"), "SunRiver Villas clubhouse"), photo(V("cc-2.0j4sw-9f5al96.jpg"), "SunRiver Villas clubhouse"), photo(V("cc-3.14i3w90tvu8ut.jpg"), "SunRiver Villas clubhouse"),
         star_list(vil_clubs), img(V("concert.3jd7d6v9e7cyc.jpg"), "Live concert at SunRiver Villas"), img(V("yoga-sunset.43efwz95kg7zl.jpg"), "SunRiver members practicing yoga at sunset"),
         resale("the SunRiver Villas").replace('class="section"', 'class="section sand"', 1), chat_section()))

    # ============================================================== CONTACT
    team = [("Dalan Madsen", "Broker / Sales Manager", "dalan@sunriver.com", "(435) 229-5023", V("dalan.0fx0mplw8vyem.jpg")),
            ("Andrea Nicely", "REALTOR&reg;", "andrea@sunriver.com", "(435) 668-8212", V("andrea.36c3xzauk54-3.jpg")),
            ("Marlo Rossner", "REALTOR&reg;", "leimomir@hotmail.com", "(435) 669-2667", V("marlo.2iuy1abjtkppc.jpg")),
            ("Paul Warburton", "REALTOR&reg;", "paulw@sunriver.com", "(435) 669-5939", V("paul.2wxmecg-jx8o7.jpg")),
            ("Margaret Anderson", "REALTOR&reg;", "margaret@sunriver.com", "(435) 668-0905", V("margaret.2hiia2zwqqlxn.jpg")),
            ("Carol Boisvert", "REALTOR&reg;", "carolb@sunriver.com", "(435) 467-9401", V("carol.3nqxgved6-8wd.jpg"))]
    tel = lambda t: "tel:+1" + "".join(ch for ch in t if ch.isdigit())
    team_html = "".join('<div class="person">%s<p class="role">%s</p><h3>%s</h3><p><a href="mailto:%s">%s</a><br>M: <a href="%s">%s</a></p></div>' % (
        photo(p, "Portrait of %s" % n, ""), r, n, e, e, tel(t), t) for n, r, e, t, p in team)
    add("/contact-us", "Contact Us", "Contact the SunRiver sales team in Toquerville and St. George, Utah. Sales Office (435) 688-1000.", "visit", '''
%s
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div class="stack-lg">
      <div class="stack"><h2 class="display">Let's <span class="yellow">talk.</span></h2><hr class="rule"><p class="lede">Fill out the form and a representative from SunRiver Communities will respond as soon as possible. Or email us at <a href="mailto:info@sunriver.com">info@sunriver.com</a>.</p></div>
      <div class="grid cols-2">
        <div class="office"><h3>SunRiver Firelight Sales Office</h3><p>182 Cottonwood Dr<br>Toquerville, UT 84737<br><a href="%s">%s</a></p><p>Mon to Fri 9am to 5pm<br>Sat 10am to 5pm<br>Sun 11am to 5pm</p></div>
        <div class="office"><h3>SunRiver Communities Sales Office</h3><p>1404 W Sun River Pkwy, Suite #200<br>St. George, UT 84790</p><p>Mon to Fri 9am to 5pm<br>Sat and Sun closed</p></div>
        <div class="office"><h3>SunRiver St. George HOA</h3><p>4275 Country Club Drive<br>St. George, UT 84790<br>(435) 287-3061<br><a href="https://pmprollc.com">pmprollc.com</a></p></div>
        <div class="office"><h3>SunRiver Villas HOA</h3><p>1404 W Sun River Pkwy, Suite #250<br>St. George, UT 84790<br>(435) 773-6456<br><a href="http://www.swmlife.com">swmlife.com</a></p></div>
      </div>
    </div>
    <form class="chat-form light" data-demo novalidate aria-label="Contact form">
      <div class="row">
        <div><label for="c-first">First Name</label><input id="c-first" name="firstname" type="text" autocomplete="given-name" required></div>
        <div><label for="c-last">Last Name</label><input id="c-last" name="lastname" type="text" autocomplete="family-name" required></div>
      </div>
      <div><label for="c-email">Email Address</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
      <div><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
      <fieldset><legend>Which community?</legend><div class="checks">
        <label><input type="checkbox" name="community" value="firelight">SunRiver Firelight</label><label><input type="checkbox" name="community" value="stgeorge">SunRiver St. George</label>
        <label><input type="checkbox" name="community" value="villas">SunRiver Villas</label><label><input type="checkbox" name="community" value="discovery">Discovery Villas stay</label></div></fieldset>
      <div><label for="c-msg">Message</label><textarea id="c-msg" name="message"></textarea></div>
      <p class="consent">By clicking "Submit", I authorize SunRiver to contact me about this request via the contact information I provide. I understand calls or texts may use automated technology. I can opt out at any time on the SunRiver website or by unsubscribing. This consent is not required to complete my request.</p>
      <button class="btn" type="submit">Submit</button>
      <p class="form-note" hidden style="color:var(--sunriver-blue)"></p>
    </form>
  </div>
</section>
<section class="section sand" id="team">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Meet the <span class="yellow">team</span></h2><hr class="rule center"></div>
    <div class="team-grid">%s</div>
  </div>
</section>''' % (full_hero("Contact Us", "Have questions? We've got answers.", src=V("hero.2wct_5z-9ksc6.jpg"), alt="",
                   cta='<a class="hero-phone" href="%s">Sales Office %s</a>' % (PHONE_TEL, PHONE)), PHONE_TEL, PHONE, team_html))

    # ============================================================== FOUNDERS CLUB
    add("/founders-club", "Founders Club", "Join the SunRiver Firelight Founders Club: two years of HOA dues paid by SunRiver and first pick of premium homesites for the first 74 homeowners.", "visit", '''
%s
<section class="section">
  <div class="wrap narrow center stack">
    <p class="lede">As a Founder, you're not just buying a home, you're becoming part of SunRiver Firelight's future. Your energy and community spirit will make this an amazing place to live.</p>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Founders Club <span class="yellow">exclusives</span></h2><hr class="rule center"><p class="lede">Be among the first 74 founding families to start the community.</p></div>
    <div class="star-grid cols-3">
      <div class="star-item"><h3>SunRiver pays your HOA dues for 2 full years</h3><p>An exclusive benefit for those who help launch the SunRiver Firelight community.</p></div>
      <div class="star-item"><h3>First pick of premium homesites</h3><p>The best locations, close to where the future community amenities will be.</p></div>
      <div class="star-item"><h3>Largest homesites available</h3><p>Secure the most desirable properties in the community.</p></div>
    </div>
  </div>
</section>
<section class="section deep-bg">
  <div class="wrap narrow center stack">
    <h2 class="display">Be a Founding Member and enjoy <span class="yellow">two years of no HOA payments</span></h2><hr class="rule center">
    <p class="lede">Two full years of HOA dues paid by SunRiver is our way of thanking you for being part of the beginning.</p>
    <div class="btn-row" style="justify-content:center">%s</div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="grid cols-2"><div class="photo ratio-34 shadow">%s</div><div class="photo ratio-34 shadow">%s</div></div>
    <div class="stack">
      <h2 class="display">Shape the <span class="yellow">community</span></h2><hr class="rule">
      <p class="lede">As a founding member, you'll help define the clubs and groups that matter to you, influence community programming and the social calendar, build lasting friendships with fellow SunRiver members, and shape the culture of SunRiver Firelight from day one.</p>
      <h3 class="h3">Why SunRiver Firelight? Why now?</h3>
      %s
      <div class="btn-row">%s</div>
    </div>
  </div>
</section>
%s
<section class="section tight"><div class="wrap"><p class="note center">Founders Club benefits apply to the first 74 lots within the SunRiver Firelight community. Ask a sales agent for full details.</p></div></section>
%s''' % (full_hero("Be part of history at SunRiver Firelight", "Your exclusive invitation to shape Southern Utah's newest 55+ community.", "SunRiver Firelight Founders Club",
                   V("hero-biking.2u6pg0mr8v0zj.jpg"), "SunRiver members biking near SunRiver Firelight", btn("Contact a Sales Agent", "/contact-us"),
                   extra='<div class="fh-badge">%s</div>' % img(FOUNDERS_BADGE, "SunRiver Firelight Founders Club badge", loading="eager")), btn("Contact a Sales Agent Today", "/contact-us"),
         img(V("pickleball.2djjcxkbj1i0d.jpg"), "Two SunRiver members playing pickleball"), img(V("hike.07ka4q1elcjrm.jpg"), "Two SunRiver members resting on red rocks"),
         star_list(["<strong>A track record since 1998.</strong> SunRiver has built and sold over 2,500 homes across Southern Utah.",
                    "<strong>A growing 55+ destination.</strong> Southern Utah is one of the most sought-after places to live your greatest chapter.",
                    "<strong>Near Zion National Park.</strong> World-class recreation 31 minutes from home."]),
         btn("Let's Talk", "/contact-us"), band(V("neighborhood-walk.2u4xr239zlka_.jpg"), "SunRiver members walking through the neighborhood"), chat_section()))

    # ============================================================== DISCOVERY VILLAS
    add("/discovery-villas", "Discovery Villas", "Spend three days and two nights in a designer-furnished villa at SunRiver Firelight. Tour the homes for $399.", "visit", '''
%s
<section class="section">
  <div class="wrap split">
    <div class="stack">
      <h2 class="display">See SunRiver Firelight the way <span class="yellow">you'll live it.</span></h2><hr class="rule">
      <p class="lede">Spend three days and two nights in a designer-furnished villa and make this community your basecamp while you explore. Tour the homes, walk the neighborhood and picture your greatest chapter, at your own pace, with no compromises.</p>
      <p class="serif price-callout">3 days, 2 nights <span class="yellow">$399</span></p>
      <div class="btn-row"><a class="btn" href="/discovery-villas/book">Request your stay</a><a class="btn blue-btn" href="%s">Or call us %s</a></div>
    </div>
    <div class="photo ratio-34 shadow">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Close to everything that makes <span class="yellow">Southern Utah special</span></h2><hr class="rule center"></div>
    <div class="grid cols-3 dv-near">%s%s%s</div>
    <div class="center btn-row" style="justify-content:center"><a class="btn" href="/discovery-villas/book">Request your stay</a><a class="btn blue-btn" href="%s">Call to book your stay</a></div>
  </div>
</section>
%s''' % (full_hero("Consider it undercover research.", "Three days and two nights at SunRiver Firelight, for $399.", "Discovery Villas",
                     FG("dv-living"), "Inside a designer-furnished Discovery Villa"),
         PHONE_TEL, PHONE, img(FG("dv-firepit"), "SunRiver members around the fire pit at the Discovery Villas", "dv-photo"),
         '<div class="photo">%s</div>' % simg("ff6cad819fb35b52154d3d5e8b3644f73c0d438f-992x698.png", "Nearby Southern Utah destination and drive time", 600, sizes="33vw"),
         '<div class="photo">%s</div>' % simg("01f99f1f0973eab00b77baec91841deb780f8ca9-992x698.webp", "Nearby Southern Utah destination and drive time", 600, sizes="33vw"),
         '<div class="photo">%s</div>' % simg("05d265df0de538b14de74d884253e01c596a2490-992x698.png", "Nearby Southern Utah destination and drive time", 600, sizes="33vw"),
         PHONE_TEL, chat_section("Plan your stay", "Questions about the Discovery Villas? Send us a note and we'll help you pick your dates.")))

    # ============================================================== MORTGAGE
    loans = [("The HECM for Purchase", "The Home Equity Conversion Mortgage for Purchase uses a one-time down payment to buy a home, with no required monthly mortgage payments for as long as you live in the home. HUD insured."),
             ("The Bridge Loan", "A short term option for buying a new home before selling your current one, without spending money on unnecessary fees."),
             ("The Senior Line of Credit", "For homeowners 62 and older, an FHA insured HECM line of credit on a new purchase or an existing home, with flexible payments or no payments and access to funds over your lifetime."),
             ("The Retirement Loan", "A low down payment loan built for seniors, with a payment that can be fixed for life and the security of owning your home."),
             ("The Recasting Loan", "Buy now, then pay down the principal with a lump sum when your previous home sells and reset your monthly payment to where you want it, without new loan paperwork.")]
    loans_html = "".join('<div class="card"><h3>%s</h3><hr class="rule short"><p>%s</p></div>' % x for x in loans)
    add("/no-mortgage-payments-for-life", "Mortgage Options", "Mortgage options for seniors with Brandon Hansen of Cherry Creek Mortgage, including the HECM for Purchase.", "homes", '''
%s
<section class="section">
  <div class="wrap split" style="grid-template-columns:minmax(0,.7fr) minmax(0,1.3fr)">
    <div class="stack"><div class="photo ratio-34 shadow">%s</div>%s</div>
    <div class="stack">
      <p class="eyebrow">Meet Brandon Hansen</p>
      <h2 class="display">A mortgage specialist for SunRiver members.</h2><hr class="rule">
      <p class="lede">Brandon Hansen is a Senior Adviser and Managing Broker with Cherry Creek Mortgage, with offices in St. George and at SunRiver St. George.</p>
      <p>His focus is senior clients, with loans designed for borrowers 62 and older. Brandon is a licensed Investment Adviser Representative, holds all lines of insurance with the State of Utah, and is a leading Senior HECM FHA Insured lender in Utah.</p>
      <p><strong>Office: (435) 674-9200</strong><br><a href="https://www.brandonhansenmortgage.com">brandonhansenmortgage.com</a></p>
      <p class="note">All rate and program questions are answered directly by Brandon Hansen. SunRiver does not publish rates.</p>
    </div>
  </div>
</section>
<section class="section sand">
  <div class="wrap split" style="align-items:start">
    <div class="stack"><h2 class="display">Five ways to <span class="yellow">arrive.</span></h2><hr class="rule"><div class="photo">%s</div></div>
    <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">%s</div>
  </div>
</section>
%s''' % (full_hero("Mortgage options for seniors", eyebrow="Mortgage Options", src=V("hero.2y-1-elem3cii.jpg")), img(V("brandon-hansen.0156dosmff1qe.jpg"), "Portrait of Brandon Hansen"),
         img(V("ccmc-logo.0n4e-3057h95z.png"), "Cherry Creek Mortgage logo", "partner-logo"), img(V("loans.3_6r2qstk9_se.png"), "SunRiver members reviewing loan options"),
         loans_html, chat_section("Have more questions?", "Reach out and a representative from Brandon Hansen and Associates will get back to you as soon as possible.")))

    # ============================================================== ENERGY
    add("/energy", "Energy Efficient Homes", "How SunRiver builds energy efficient homes, measured with the HERS Index and verified by independent testing.", "homes", '''
%s
<section class="section">
  <div class="wrap split wide-text">
    <div class="stack"><h2 class="display">What is an energy efficient <span class="yellow">home?</span></h2><hr class="rule">
      <p class="lede">A comfortable home is a high performing home, and that means being energy efficient. Since the early 2000s, SunRiver Construction has made energy efficiency a top priority in every home it builds.</p></div>
    <div class="photo plain">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap grid cols-2" style="align-items:start">
    <div class="card"><p class="eyebrow">HERS Rating</p><h3>Measured, not guessed.</h3><hr class="rule short"><p>SunRiver uses the Home Energy Rating System Index, or HERS rating, on every home in the community. It is the industry standard for measuring a home's energy efficiency: the lower the HERS rating, the more efficient the home.</p></div>
    <div class="card"><p class="eyebrow">Thorough home testing</p><h3>Tested for airtightness.</h3><hr class="rule short"><p>Home Energy Rater Kim Ewers consults with homebuilders on how to improve the performance of the homes they build. Blower door and duct leakage tests show how airtight construction is. Air that leaks out has to be replaced by outside air that must be cooled again, and lost A/C air is one of the biggest energy wasters in a home.</p></div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="photo ratio-43 shadow">%s</div>
    <div class="stack"><p class="eyebrow">Live In</p><h2 class="display">Built to keep you comfortable.</h2><hr class="rule"><p class="lede">Low-e windows, concrete roof tiles and hybrid gas and electric heating and cooling come standard in every SunRiver home.</p><div class="btn-row">%s</div></div>
  </div>
</section>
%s''' % (full_hero("Energy efficient homes", eyebrow="How We Build", src=V("hero.1irv6-1-qgzsa.png")), img(V("hers-arrow.2ho2zyizzj715.png"), "HERS Index scale from zero energy home to standard new home, with a SunRiver home score highlighted"),
         img("/assets/img/energy-blower-door.webp", "A blower door pressure and flow gauge set up for a home airtightness test", attrs='style="object-position:50% 44%"'), btn("See Floor Plans", "/floor-plans"), chat_section()))

    # ============================================================== INCENTIVES
    offers = [(S("4edfb3b104b35d496a67f074dff826f2fe6c00b1-80x80.png"), "2 Years of HOA Paid by SunRiver", "Founding Members enjoy two full years of HOA dues covered by SunRiver, a $4,800 value just for joining early."),
              (S("7710fce952588e0410ff8a5ec1c14d741c80bc4c-80x80.webp"), "$10,000 Design Center Credit", "Start a new build and receive a $10,000 credit toward your home finishes, upgrades and personal touches at the SunRiver Design Center."),
              (S("758de1a49f26315d86a9bbcb3b26e5101d24f0a8-80x80.webp"), "Washer &amp; Dryer Included", "Close on a move-in ready home during the current offer window and receive a brand-new washer and dryer at no extra cost. Ask a sales agent for the current deadline.")]
    offers_html = "".join('<div class="offer-card">%s<h3>%s</h3><p>%s</p></div>' % (img(i, "", "offer-icon"), t, d) for i, t, d in offers)
    add("/incentives", "Incentives", "Current offers for new SunRiver Firelight homebuyers, including two years of HOA dues paid and a $10,000 Design Center credit.", "homes", '''
%s
<section class="section">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">For new SunRiver Firelight <span class="yellow">homebuyers</span></h2><hr class="rule center"></div>
    <div class="grid cols-3">%s</div>
    <p class="note center">*Current offers only apply to the first 74 lots within the SunRiver Firelight community.</p>
    <div class="center">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap split">
    <div class="grid cols-2"><div class="photo ratio-23 shadow">%s</div><div class="photo ratio-23 shadow">%s</div></div>
    <div class="stack">
      <h2 class="display">Join the SunRiver Firelight <span class="yellow">Founders Club</span></h2><hr class="rule">
      <p class="lede">Limited to the first 74 homeowners. Exclusive benefits include:</p>
      %s
      <div class="btn-row">%s</div>
    </div>
  </div>
</section>
%s''' % (sand_hero("Incentives", "SunRiver Firelight current offers", src=V("hero.2h_vl62bxoy8t.jpg"), alt="SunRiver Firelight homes with red rock mountains behind"), offers_html, btn("View Move-In Ready Homes", "/homes-for-sale"),
         simg("d9ab6fb431a69357ceac184260508988c17b1498-1000x1500.jpg", "SunRiver members at SunRiver Firelight", 600, sizes="25vw"),
         simg("59eed49c03774313b75eafb9a0b4e31556bad280-1354x1458.webp", "SunRiver Firelight home interior", 600, sizes="25vw"),
         star_list(["<strong>Zero HOA fees for 2 full years.</strong> SunRiver pays your HOA dues for you.",
                    "<strong>First pick of premium homesites.</strong> Best locations, largest homesites.",
                    "<strong>Introductory pricing.</strong> There's no better time than now."]),
         btn("Learn about the Founders Club", "/founders-club"), chat_section()))

    # ============================================================== REALTOR BENEFITS
    rb = [("Paid at the Start", "SunRiver pays your commission at the start of construction, when your client makes their down payment. Ask our Sales Manager for current commission details."),
          ("Building a Home", "Building is the only way to get your buyer exactly what they want. Our onsite design team keeps the process efficient and simple."),
          ("Move-In Ready Homes", "Buyers are often on a timeline. We keep many of our most popular plans completed or close to completion, so you can close in 30 days or less."),
          ("Proven Product", "Active adult living fits Southern Utah perfectly. With the full amenity package SunRiver is known for and over 50 clubs and groups, your buyers will truly live young."),
          ("Live a Little Closer", "SunRiver Firelight is 15 minutes from St. George and much closer to what makes this area amazing: Zion, Cedar City and Brian Head. At 3,500 feet, the temperatures are cooler, with no snow to shovel."),
          ("Proven Partnership", "SunRiver has built over 2,600 homes with the help of Washington County Realtors. We work well together and protect the relationship you have with your client.")]
    rb_html = "".join('<div class="card"><h3>%s</h3><hr class="rule short"><p>%s</p></div>' % x for x in rb)
    add("/realtor-benefits", "Realtor Benefits", "Partner with Southern Utah's premier 55+ builder. Why Realtors love selling SunRiver Firelight.", "", '''
%s
<section class="section">
  <div class="wrap stack-lg">
    <div class="split"><h2 class="display">SunRiver <span class="yellow">loves Realtors!</span></h2><p class="lede">Buyers deserve representation, your unbiased opinion and your local expertise.</p></div>
    <div class="grid cols-3">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap narrow center stack">
    <h2 class="display">Bring your clients <span class="yellow">home</span></h2><hr class="rule center">
    <p class="lede">Schedule a tour of our model homes and see the SunRiver difference.</p>
    <div class="btn-row" style="justify-content:center">%s</div>
  </div>
</section>''' % (sand_hero("Selling with SunRiver", "Partner with Southern Utah's premier 55+ builder and grow your business.", "", "h1", V("hero.1zxyn0xsm69_i.jpg"), "SunRiver members enjoying the outdoors"), rb_html, btn("Contact Us", "/contact-us#team")))

    # ============================================================== AMENITIES VIDEO
    add("/amenities-video", "The Future Heart of SunRiver Firelight", "Phase 1 of the SunRiver Firelight Clubhouse is underway: a fitness center, the Clubhouse, a lap pool and four pickleball courts.", "life", '''
%s
<section class="section">
  <div class="wrap split">
    <div class="stack">
      <p class="lede">Phase 1 of the Clubhouse at SunRiver Firelight is now underway, and for the first time you can take a look inside what's coming.</p>
      <p>Designed to bring neighbors together, this first phase includes a fitness center and the Clubhouse, a lap pool and four pickleball courts.</p>
      <h2 class="h3">A place to gather</h2>
      <p>The Clubhouse is being designed as the center of community life: the place where SunRiver members meet friends, stay active, join clubs and groups, and enjoy everything that makes SunRiver Firelight special.</p>
    </div>
    <div class="photo ratio-43 shadow">%s</div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="display">Phase 1 amenities <span class="yellow">include</span></h2><hr class="rule center"></div>
    <div class="star-grid cols-3">
      <div class="star-item"><h3>Fitness Center &amp; the Clubhouse</h3><p>A welcoming space for exercise, events, clubs and everyday connection.</p></div>
      <div class="star-item"><h3>Lap Pool</h3><p>Perfect for swimming, relaxing and enjoying the Southern Utah sunshine.</p></div>
      <div class="star-item"><h3>Four Pickleball Courts</h3><p>A place for fun, activity and friendly competition.</p></div>
    </div>
    <p class="center lede" style="margin-inline:auto">Construction has already begun, and now is the perfect time to be among the first to experience it.</p>
    <div class="center">%s</div>
  </div>
</section>
%s''' % (sand_hero("SunRiver Firelight", "The future heart of SunRiver Firelight", "Explore Phase 1 of the SunRiver Firelight Clubhouse, including a fitness center, lap pool and pickleball courts.", src=S("00a771c4786df837151167618e14dcacac89a759-2048x1506.webp", 2400), alt="Rendering of the SunRiver Firelight Clubhouse"),
         simg("00a771c4786df837151167618e14dcacac89a759-2048x1506.webp", "Rendering of the SunRiver Firelight Clubhouse", 1000, sizes="(max-width: 860px) 100vw, 50vw"),
         btn("Talk with an Agent", "/contact-us"), chat_section()))

    # ============================================================== LIVE IN / OUT / ON
    lives = [
        ("/live-in", "Live In", "Floor Plans. The Design Center. How We Build.", V("live-in.0-iialxva3p9u.jpg"),
         "Homes built for the way you actually live: open kitchens for gathering, hobby rooms for picking things back up, and extended garages for the gear.",
         [("Floor Plans", "Seven plans, five of them open as model homes.", "/floor-plans"), ("Homes for Sale", "Move-in ready homes at SunRiver Firelight.", "/homes-for-sale"),
          ("Energy Efficient Homes", "How the homes are built.", "/energy"), ("Incentives", "Current offers for new homebuyers.", "/incentives")]),
        ("/live-out", "Live Out", "Southern Utah. Trails and Nearby Adventure.", V("live-out.2z9c8sf8gogme.jpg"),
         "Zion is 31 minutes from SunRiver Firelight. Snow Canyon is closer. Six national parks are within a few hours, and trails leave right from the neighborhood.",
         [("Southern Utah", "Zion, Snow Canyon and the region around the community.", "/southern-utah"), ("Why SunRiver?", "The lifestyle, in one place.", "/why-sunriver"),
          ("Bucketlist Living", "Trips, trails and days out from the blog.", "/bucketlistliving"), ("Discovery Villas", "Stay three days and two nights and explore.", "/discovery-villas")]),
        ("/live-on", "Live On", "Clubs and Activities. Events Calendar. Bucketlist.", V("live-on.2kwzvtocledst.jpg"),
         "Real friendships don't happen by accident, so we build the conditions for them. Over 60 clubs and groups, and a calendar that stays full.",
         [("Why SunRiver?", "Clubs, groups and the people who make the place.", "/why-sunriver"), ("Bucketlist Living", "Stories and events from SunRiver members.", "/bucketlistliving"),
          ("The Clubhouse", "The future heart of SunRiver Firelight.", "/amenities-video"), ("Founders Club", "Help shape the community from day one.", "/founders-club")]),
    ]
    for path, t, sub, pic, intro, links in lives:
        links_html = "".join('<a class="hub-link" href="%s"><strong>%s</strong><span>%s</span></a>' % (h, a, b) for a, b, h in links)
        add(path, t, "%s at SunRiver: %s" % (t, sub), "life", '''
%s
<section class="section">
  <div class="wrap split">
    <div class="photo ratio-43 shadow">%s</div>
    <div class="stack"><h2 class="display">%s</h2><hr class="rule"><p class="lede">%s</p></div>
  </div>
</section>
<section class="section sand">
  <div class="wrap stack-lg">
    <div class="center stack"><h2 class="h2">Start exploring</h2><hr class="rule center"></div>
    <div class="hub-links">%s</div>
  </div>
</section>
%s''' % (sand_hero("Life at SunRiver", t, sub, src=pic, alt="%s at SunRiver" % t), img(pic, "%s at SunRiver" % t, loading="eager"), t, intro, links_html, chat_section()))

    # ============================================================== PRIVACY POLICY
    add("/privacy-policy", "Privacy Policy", "SunRiver Communities privacy policy and SMS terms.", "", PRIVACY.replace("%s", full_hero("Privacy Policy", "Effective Date: January 1, 2026"), 1))

    # ============================================================== 404
    add("/404", "Page Not Found", "This page could not be found.", "", '''
%s
<section class="section tight"><div class="wrap center"><div class="btn-row" style="justify-content:center">%s%s</div></div></section>''' % (
        sand_hero("Page not found", "Looks like you took a wrong trail.", "The page you're looking for isn't here. Head back to the start or reach out and we'll point you the right way."),
        btn("Back to start", "/"), btn("Contact Us", "/contact-us", "blue-btn")))


PRIVACY = '''
%s
<section class="section">
  <div class="wrap narrow legal">
    <p>At SunRiver, we are committed to protecting your privacy. This Privacy Policy outlines how we collect, use, store, and safeguard your information when you visit our website or engage with us online.</p>
    <h2>Information We Collect</h2>
    <p>We may collect the following types of information:</p>
    <p><strong>1. Personal Information.</strong> When you fill out a form, request information, schedule a tour, or contact us, we may collect personal details such as:</p>
    ''' + ul(["Name", "Email address", "Phone number", "Mailing address", "Preferences related to home buying, communities, or services"]) + '''
    <p><strong>2. Non-Personal Information.</strong> When you browse our website, we may collect anonymous data such as:</p>
    ''' + ul(["Browser type", "IP address", "Device type", "Pages visited", "Time spent on the site", "Referring websites"]) + '''
    <p>This data is used to improve website performance, content, and user experience.</p>
    <h2>How We Use Your Information</h2>
    <p>We use collected information to:</p>
    ''' + ul(["Respond to your inquiries and provide customer service", "Send updates, promotional materials, or newsletters (you can opt out at any time)", "Improve our website, services, and marketing efforts", "Track and analyze website usage to enhance user experience", "Personalize your interaction with SunRiver Firelight and other SunRiver communities"]) + '''
    <h2>Sharing of Information</h2>
    <p>We do not sell, rent, or lease your personal information to third parties.</p>
    <p>We may share your information with trusted service providers who assist us in operating our website, marketing, or customer support, under strict confidentiality agreements.</p>
    <p>We may also disclose information when required to do so by law or in connection with a legal obligation, investigation, or government request.</p>
    <h2>Cookies and Tracking Technologies</h2>
    <p>Our website uses cookies and other tracking tools (such as Google Analytics) to collect and store certain information automatically. Cookies help us improve functionality, remember your preferences, and analyze traffic patterns.</p>
    <p>You can control cookie settings through your browser and choose to disable cookies, though some features of the site may not function properly without them.</p>
    <h2>Email Communications</h2>
    <p>By providing your email address, you consent to receive occasional marketing and informational emails from SunRiver. You may unsubscribe at any time by clicking the link at the bottom of any email.</p>
    <h2>Data Security</h2>
    <p>We take reasonable measures to protect your personal data from unauthorized access, loss, or misuse. However, no method of transmission over the internet is completely secure, and we cannot guarantee absolute security.</p>
    <h2>Your Rights and Choices</h2>
    <p>You have the right to:</p>
    ''' + ul(["Access, correct, or delete your personal information", "Opt out of marketing communications", "Request details about the data we collect or how it's used"]) + '''
    <p>To make a request or update your preferences, please contact us at <a href="mailto:info@sunriver.com">info@sunriver.com</a>.</p>
    <h2>Children's Privacy</h2>
    <p>SunRiver.com is intended for users age 18 and older. We do not knowingly collect personal information from children under 13. If we become aware that such data has been collected, we will delete it promptly.</p>
    <h2>Changes to This Policy</h2>
    <p>We may update this Privacy Policy occasionally to reflect changes in our practices or legal requirements. The most current version will always be posted here, with the effective date at the top.</p>
    <h2>SMS/Text Messaging Terms and Conditions</h2>
    <p><strong>Consent to Receive SMS Messages:</strong> If you consent to receive SMS communications from SunRiver, you agree to receive property updates, community announcements, appointment reminders, promotional offers, and customer service text messages from us.</p>
    <p><strong>How to Opt-Out:</strong> Reply STOP to unsubscribe from SMS messages at any time.</p>
    <p><strong>How to Get Help:</strong> Reply HELP for assistance or contact us at info@sunriver.com.</p>
    <p><strong>Message and Data Rates:</strong> Msg&amp;Data rates may apply according to your mobile carrier's plan.</p>
    <p><strong>Message Frequency:</strong> Messaging frequency may vary based on your interactions with us and community updates.</p>
    <p><strong>Information Collected via SMS:</strong> When you opt in to SMS communications, we collect:</p>
    ''' + ul(["Your mobile phone number", "Your name (if provided)", "Property preferences and inquiry details", "Your interaction history with our SMS service"]) + '''
    <p><strong>How We Use Your SMS Information:</strong></p>
    ''' + ul(["To send requested property information and updates about SunRiver Firelight", "To provide customer service and respond to your inquiries", "To send appointment reminders for tours and meetings", "To share community news and development updates", "To send promotional offers for SunRiver properties (if you have opted in)"]) + '''
    <p><strong>Sharing of SMS Information:</strong> No mobile opt-in message consent will be shared with third parties or affiliates for marketing purposes. We may share your information with service providers who assist in delivering SMS services, but they are contractually obligated to keep your information confidential and use it only for providing services to us.</p>
    <p><strong>Your Consent:</strong> By opting in to receive SMS messages, you confirm that you are the mobile account holder or have authorization to receive texts at the provided number.</p>
    <h2>How We Share Your Information</h2>
    <p>We do not sell your personal information to third parties. We may share your information in the following circumstances:</p>
    <p><strong>Service Providers:</strong> We may share your information with trusted third-party service providers who assist us with website hosting, email delivery, SMS messaging, customer relationship management, and other business operations. These providers are contractually obligated to protect your information and use it only for the purposes we specify.</p>
    <p><strong>Legal Requirements:</strong> We may disclose your information if required by law, court order, or government regulation, or if we believe disclosure is necessary to protect our rights or the safety of others.</p>
    <p><strong>Business Transfers:</strong> If SunRiver is involved in a merger, acquisition, or sale of assets, your information may be transferred as part of that transaction.</p>
    <p><strong>With Your Consent:</strong> We may share your information with third parties when you have given us explicit permission to do so.</p>
    <p>We implement reasonable security measures to protect your personal information from unauthorized access, disclosure, alteration, or destruction. However, no method of transmission over the internet or electronic storage is completely secure, and we cannot guarantee absolute security.</p>
    <p>You have the following rights regarding your personal information:</p>
    <p><strong>Access and Correction:</strong> You may request access to or correction of your personal information by contacting us at info@sunriver.com.</p>
    <p><strong>Opt-Out of Marketing:</strong> You may opt out of marketing emails by clicking the "unsubscribe" link in any marketing email or by contacting us directly. You may opt out of SMS messages by replying STOP.</p>
    <p><strong>Do Not Track:</strong> Our website does not currently respond to "Do Not Track" signals from browsers.</p>
    <h2>Third-Party Links</h2>
    <p>Our website may contain links to third-party websites. We are not responsible for the privacy practices of these external sites. We encourage you to review the privacy policies of any third-party websites you visit.</p>
    <h2>Changes to This Privacy Policy</h2>
    <p>We may update this Privacy Policy from time to time. Any changes will be posted on this page with an updated effective date. We encourage you to review this Privacy Policy periodically.</p>
    <h2>Contact Us</h2>
    <p>For questions about this Privacy Policy or your personal data, contact:<br>SunRiver Communities<br>1404 W Sun River Pkwy, Suite #200<br>St. George, UT 84790<br>Email: <a href="mailto:info@sunriver.com">info@sunriver.com</a><br>Website: www.sunriver.com</p>
  </div>
</section>'''
