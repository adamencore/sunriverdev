"""Homepage, built from the Figma frame "Home Clark Life NAV 4" (node 625:214) in "SunRiver Website 2026".

Section order and measurements follow the 1440px design. Brand rules applied to the copy:
Zion is 31 minutes from SunRiver Firelight, and "members" instead of "residents".
"""
from .figma_assets import FG
from .lib import V, VP, add, chat_section, esc, img, simg
from .pages_cms import plan_image

WAVE_BLUE = ('<svg class="story-wave" viewBox="0 0 1713 421" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M260.627 294.377C146.792 288.469 55.0918 371.684 23.4709 414.03H1346.07C1336.95 388.425 1312.87 328.648 1289.52 294.377C1260.33 251.539 1085.2 136.318 939.26 177.679C793.318 219.041 720.346 335.739 565.282 359.374C410.219 383.009 402.921 301.763 260.627 294.377Z" fill="#fff" fill-opacity=".03"/>'
             '<path d="M306.454 164.108C131.348 164.108 14.5942 353.049 0 421L1713 409.182C1701.07 375.705 1682.36 208.917 1651.82 164.108C1613.66 108.098 1384.66 -42.5504 1193.82 11.5285C1002.99 65.6074 907.576 218.187 704.817 249.09C502.057 279.992 492.897 164.108 306.454 164.108Z" fill="#fff" fill-opacity=".07"/></svg>')
WAVE_SAND = ('<svg class="live-wave" viewBox="0 0 1713 421" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M306.454 164.108C131.348 164.108 14.5942 353.049 0 421L1713 409.182C1701.07 375.705 1682.36 208.917 1651.82 164.108C1613.66 108.098 1384.66 -42.5504 1193.82 11.5285C1002.99 65.6074 907.576 218.187 704.817 249.09C502.057 279.992 492.897 164.108 306.454 164.108Z" fill="#fff" fill-opacity=".55"/></svg>')


def build_home(plans):
    lives = [
        ("Live In", VP("/images/home-v2/icon-home.svg"), "Open kitchens built for gathering. Hobby rooms, because people at this stage are picking things back up, not putting them down. Extended three-car garages, because you have bikes, kayaks, and gear. Customization throughout, so you're building the home instead of just buying it.", "See All Floor Plans", "/floor-plans"),
        ("Live Out", VP("/images/home-v2/icon-nature.svg"), "Zion 31 minutes away. Snow Canyon closer. Six national parks within a few hours. And Costco, banking, doctors, and restaurants all within reach. You aren't trading convenience for the view. You get both.", "Explore Southern Utah", "/southern-utah"),
        ("Live On", VP("/images/home-v2/icon-users.svg"), "Move. Connect. Grow. Real friendships don't happen by accident, so we build the conditions for them. Most people arrive planning to do one thing and end up doing five.", "Clubs &amp; Groups", "/why-sunriver"),
    ]
    live_cards = "".join('''<div class="lv-card"><span class="lv-icon">%s</span><h3>%s</h3><hr><p>%s</p><a class="lv-btn" href="%s">%s</a></div>''' % (
        img(icon, ""), t.upper(), d, href, label) for t, icon, d, label, href in lives)

    plan_cards = "".join('''<a class="hp-card" href="/floor-plans/%s">
  <span class="hp-img">%s</span>
  <span class="hp-bar"><span class="hp-sqft">%s</span><span class="hp-name">%s</span><span class="hp-go" aria-hidden="true"></span></span>
</a>''' % (p["slug"], simg(plan_image(p), "%s exterior rendering at SunRiver Firelight" % p["name"], 916, sizes="458px") if plan_image(p) else "",
           p["squareFootage"], esc(p["name"])) for p in plans)

    steps = [("Visit SunRiver Firelight", "Walk the models. See the landscape. Meet people who live here."),
             ("Find your home", "A lot to build on, or a home that's ready now."),
             ("Become a Member", "Keys, a tour, and an invitation to your first event.")]
    steps_html = "".join('<li><span class="st-num">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, d) for i, (t, d) in enumerate(steps))

    body = '''
<section class="h4-hero">
  <picture>
    <source media="(max-width: 760px)" srcset="%(hero_tall)s">
    <img class="h4-hero-img" src="%(hero_wide)s" alt="A SunRiver couple riding bikes in Southern Utah" fetchpriority="high">
  </picture>
  <div class="wrap h4-hero-inner">
    <h1>A 55+ community in Southern Utah for people who refuse to slow down.</h1>
    <p class="h4-eyebrow">SunRiver Firelight</p>
    <a class="btn h4-hero-btn" href="/why-sunriver">Life at SunRiver</a>
  </div>
</section>

<section class="h4-story">
  %(wave_blue)s
  <div class="wrap h4-story-inner">
    <div class="h4-couple">%(couple)s</div>
    <div class="h4-story-text">
      <h2>Most people think retirement means slowing down.</h2>
      <hr>
      <p>You've watched how that goes. A beautiful home with nobody in it to share. Days without enough in them worth leaving for. A calendar that empties out and then stays empty.</p>
      <p>Nobody sees it coming. It just happens, quietly, a little at a time.</p>
    </div>
  </div>
</section>

<section class="h4-live">
  %(wave_sand)s
  <div class="wrap h4-live-inner">
    <div class="h4-live-head"><span class="h4-tag">#LIVEYOUNG</span><h2><span class="yellow">Here, it </span>means more.</h2></div>
    <div class="h4-live-cards">%(live_cards)s</div>
  </div>
</section>

<section class="h4-sky">%(sky)s<h2>YOUR <strong>NEW LIFESTYLE</strong> AWAITS</h2></section>

<section class="h4-years">
  <div class="h4-years-stage">
    <h2 class="hy-title">We've been doing this for 25 years.</h2>
    <div class="hy-text">
      <p>We understand what it feels like to be ready for this season, yet unsure where and how it happens. We've heard every hesitation: Will I fit in? Am I making the right call? Will the amenities really arrive?</p>
      <p>We've built and sold over 2,500 homes across Southern Utah. Our members come back to visit years after they moved. What we've learned is people arrive here thinking they're buying a house only to realize they're starting their best chapter.</p>
      <p class="hy-record">This isn't theoretical. It's our record.</p>
    </div>
    <div class="hy-img hy-1">%(y1)s</div>
    <div class="hy-img hy-2">%(y2)s</div>
    <div class="hy-frame hy-3"><div>%(y3)s</div></div>
    <div class="hy-frame hy-4"><div>%(y4)s</div></div>
  </div>
</section>

<section class="h4-homes">
  <h2 class="wrap">Find the home that suits you.</h2>
  <div class="hp-carousel">
    <button class="hp-arrow hp-prev" type="button" aria-label="Previous floor plans" hidden></button>
    <div class="hp-track" tabindex="0" aria-label="Floor plans">%(plan_cards)s</div>
    <button class="hp-arrow hp-next" type="button" aria-label="More floor plans"></button>
  </div>
  <div class="center"><a class="btn h4-big-btn" href="/floor-plans">View All Floor Plans</a></div>
</section>

<section class="h4-begin">
  %(begin)s
  <div class="wrap h4-begin-inner">
    <h2>Where you begin</h2>
    <hr>
    <ol class="h4-steps">%(steps)s</ol>
    <a class="btn sand-btn h4-begin-btn" href="/contact-us">Schedule a Visit</a>
  </div>
</section>

%(chat)s''' % dict(
        hero_tall=FG("hero-tall"), hero_wide=FG("hero-wide"), wave_blue=WAVE_BLUE, wave_sand=WAVE_SAND,
        couple=img(FG("couple"), "A smiling SunRiver couple", loading="eager"),
        live_cards=live_cards, sky=img(FG("sky"), ""),
        y1=img(FG("years-1"), "SunRiver members hiking in red rock country"), y2=img(FG("years-2"), "SunRiver members riding bikes"),
        y3=img(FG("years-3"), "SunRiver members at a yoga class"), y4=img(FG("years-4"), "A SunRiver member playing pickleball"),
        plan_cards=plan_cards, begin=img(FG("begin"), "", "h4-begin-bg"), steps=steps_html, chat=chat_section())

    add("/", "SunRiver Firelight | 55+ Community in Southern Utah",
        "SunRiver Firelight is a 55+ community in Toquerville, Utah, for people who refuse to slow down. Zion is 31 minutes away and five model homes are open now.",
        "home-overlay", body, body_class="home")
