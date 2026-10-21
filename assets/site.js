// SunRiver site interactions: header menu, forms, galleries, lightbox, homes-for-sale filters.
(function () {
  // ---------- Header
  var header = document.querySelector('.site-header');
  if (header) {
    var toggle = header.querySelector('.menu-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var open = header.getAttribute('data-menu') === 'open';
        header.setAttribute('data-menu', open ? 'closed' : 'open');
        toggle.setAttribute('aria-expanded', String(!open));
      });
    }
    var items = header.querySelectorAll('.nav-item[data-open]');
    var closeAll = function (except) {
      items.forEach(function (it) {
        if (it !== except) {
          it.setAttribute('data-open', 'false');
          var b = it.querySelector('button.nav-link');
          if (b) b.setAttribute('aria-expanded', 'false');
        }
      });
    };
    var hoverable = window.matchMedia('(hover: hover) and (min-width: 1021px)');
    items.forEach(function (item) {
      var btn = item.querySelector('button.nav-link');
      if (!btn) return;
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = item.getAttribute('data-open') === 'true';
        closeAll(item);
        item.setAttribute('data-open', String(!open));
        btn.setAttribute('aria-expanded', String(!open));
      });
      var t;
      item.addEventListener('mouseenter', function () { if (!hoverable.matches) return; clearTimeout(t); closeAll(item); item.setAttribute('data-open', 'true'); btn.setAttribute('aria-expanded', 'true'); });
      item.addEventListener('mouseleave', function () { if (!hoverable.matches) return; t = setTimeout(function () { item.setAttribute('data-open', 'false'); btn.setAttribute('aria-expanded', 'false'); }, 160); });
    });
    // Life at SunRiver dropdown: the photo follows the item under the pointer (or keyboard focus).
    header.querySelectorAll('.pill-drop').forEach(function (drop) {
      var shots = drop.querySelectorAll('.pd-shot');
      var show = function (i) {
        if (drop.getAttribute('data-active') === i) return;
        drop.setAttribute('data-active', i);
        shots.forEach(function (s) { s.classList.toggle('is-on', s.getAttribute('data-i') === i); });
      };
      drop.querySelectorAll('ul a[data-i]').forEach(function (a) {
        var i = a.getAttribute('data-i');
        a.addEventListener('mouseenter', function () { show(i); });
        a.addEventListener('focus', function () { show(i); });
      });
    });
    document.addEventListener('click', function (e) { if (!header.contains(e.target)) closeAll(null); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); header.setAttribute('data-menu', 'closed'); } });
  }

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Header on scroll: the white bar slims down; photo-page headers come back as a slim white bar.
  if (header) {
    var overlay = header.classList.contains('overlay'), ticking = false;
    var onScroll = function () {
      ticking = false;
      var y = window.scrollY || window.pageYOffset;
      if (overlay) {
        if (y > 220) header.classList.add('is-stuck');
        else if (y <= 8) header.classList.remove('is-stuck');
      } else {
        header.classList.toggle('is-compact', y > 40);
      }
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
    onScroll();
  }

  // ---------- Content settles in once as it scrolls into view (skipped for reduced motion
  // and for anything already on screen when the page loads).
  if (!reduced && 'IntersectionObserver' in window) {
    var groups = ['.fp-grid', '.home-grid', '.grid', '.post-grid', '.h4-live-cards', '.fah-links-grid', '.h4-steps', '.hd-bottom', '.like-row', '.team-grid', '.star-grid', '.amenities', '.hub-links'];
    var singles = 'main section h2, main .lede, main .split > *, .hd-desc, .h4-years-stage > *, .h4-sky h2, .chat .wrap > *';
    var items = [];
    document.querySelectorAll(groups.join(',')).forEach(function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) { c.dataset.rvDelay = Math.min(i % 4, 3) * 70; items.push(c); });
    });
    document.querySelectorAll(singles).forEach(function (el) {
      if (el.closest('.site-header') || items.some(function (it) { return it === el || it.contains(el) || el.contains(it); })) return;
      items.push(el);
    });
    var fold = window.innerHeight;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        io.unobserve(el);
        el.style.transitionDelay = (el.dataset.rvDelay || 0) + 'ms';
        el.classList.add('in');
        var done = function () { el.classList.remove('rv', 'in'); el.style.transitionDelay = ''; el.removeEventListener('transitionend', done); };
        el.addEventListener('transitionend', done);
        setTimeout(done, 1400);
      });
    }, { rootMargin: '0px 0px -5% 0px', threshold: 0.08 });
    items.forEach(function (el) {
      if (el.hidden || el.getBoundingClientRect().top < fold) return;
      el.classList.add('rv');
      io.observe(el);
    });
  }

  // ---------- Hero video: respect reduced motion
  var vid = document.querySelector('.home-hero-media');
  if (vid && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { vid.removeAttribute('autoplay'); vid.pause(); }

  // ---------- Forms: placeholder handler until the forms are wired to the CRM
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.form-note');
      if (note) { note.hidden = false; note.textContent = 'Thanks! A SunRiver team member will reach out soon.'; }
      form.querySelectorAll('input, textarea, button').forEach(function (el) { el.disabled = true; });
    });
  });

  // ---------- Lightbox
  function openLightbox(src, alt) {
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', alt || 'Enlarged image');
    var im = document.createElement('img');
    im.src = src; im.alt = alt || '';
    var close = document.createElement('button');
    close.type = 'button'; close.setAttribute('aria-label', 'Close'); close.innerHTML = '&times;';
    box.appendChild(im); box.appendChild(close);
    var prev = document.activeElement;
    function onKey(e) { if (e.key === 'Escape') done(); }
    function done() { box.remove(); document.removeEventListener('keydown', onKey); if (prev && prev.focus) prev.focus(); }
    box.addEventListener('click', done);
    document.addEventListener('keydown', onKey);
    document.body.appendChild(box);
    close.focus();
  }
  document.querySelectorAll('[data-lightbox]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var im = a.querySelector('img');
      openLightbox(a.getAttribute('href'), im ? im.alt : '');
    });
  });

  // ---------- Gallery viewer (main image + thumbnails)
  document.querySelectorAll('.viewer').forEach(function (viewer) {
    var main = viewer.querySelector('.viewer-main img');
    viewer.querySelectorAll('.thumb').forEach(function (th) {
      th.addEventListener('click', function () {
        if (!main) return;
        main.removeAttribute('srcset');
        main.src = th.getAttribute('data-src');
        main.classList.toggle('is-drawing', th.getAttribute('data-fit') === 'contain');
        var ti = th.querySelector('img');
        if (ti) main.alt = ti.alt;
        viewer.querySelectorAll('.thumb').forEach(function (o) { o.classList.toggle('is-active', o === th); });
      });
    });
    if (main) {
      main.style.cursor = 'zoom-in';
      main.addEventListener('click', function () { openLightbox(main.currentSrc || main.src, main.alt); });
    }
  });

  // ---------- Listing thumbnails: "See more" shows the rest
  document.querySelectorAll('.hd-thumbs .see-more').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.parentNode, open = t.classList.toggle('show-all');
      b.textContent = open ? 'See less' : 'See more';
      b.setAttribute('aria-expanded', String(open));
    });
  });

  // ---------- Homepage floor plan carousel
  document.querySelectorAll('.hp-carousel').forEach(function (car) {
    var track = car.querySelector('.hp-track'), prev = car.querySelector('.hp-prev'), next = car.querySelector('.hp-next');
    if (!track) return;
    var step = function () { var c = track.querySelector('.hp-card'); return c ? c.getBoundingClientRect().width + 29 : 400; };
    var sync = function () {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.hidden = track.scrollLeft <= 2;
      if (next) next.hidden = track.scrollLeft >= max;
    };
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  // ---------- Homes for sale filters
  var form = document.getElementById('home-filters');
  if (form) {
    var cards = Array.prototype.slice.call(document.querySelectorAll('#home-grid .home-card'));
    var count = document.getElementById('home-count');
    var empty = document.getElementById('home-empty');
    var checked = function (name) { return Array.prototype.slice.call(form.querySelectorAll('input[name="' + name + '"]:checked')).map(function (i) { return i.value; }); };
    var radio = function (name) { var r = form.querySelector('input[name="' + name + '"]:checked'); return r ? parseFloat(r.value) : 0; };
    var apply = function () {
      var comm = checked('community'), stat = checked('status'), sq = checked('sqft');
      var beds = radio('beds'), baths = radio('baths'), garage = radio('garage'), hobby = radio('hobby'), shown = 0;
      cards.forEach(function (c) {
        var d = c.dataset, n = parseFloat(d.sqft);
        var ok = (!comm.length || comm.indexOf(d.community) > -1) &&
          (!stat.length || stat.indexOf(d.status) > -1) &&
          (!sq.length || sq.some(function (r) { var p = r.split('-'); return n >= +p[0] && n <= +p[1]; })) &&
          parseFloat(d.beds) >= beds && parseFloat(d.baths) >= baths && parseFloat(d.garage) >= garage &&
          parseFloat(d.hobby) >= hobby;
        c.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = shown;
      empty.hidden = shown > 0;
    };
    var syncUrl = function () {
      var params = new URLSearchParams();
      ['community', 'status', 'sqft'].forEach(function (k) { checked(k).forEach(function (v) { params.append(k, v); }); });
      ['beds', 'baths', 'garage', 'hobby'].forEach(function (k) { if (radio(k)) params.set(k, radio(k)); });
      var q = params.toString();
      history.replaceState(null, '', location.pathname + (q ? '?' + q : ''));
    };
    // Restore filters from the URL so a filtered view can be shared.
    var initial = new URLSearchParams(location.search);
    if (Array.from(initial.keys()).length) {
      form.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = initial.getAll(i.name).indexOf(i.value) > -1; });
    }
    // "2+ / 3+ / 4+" groups are square boxes like the design, but only one can be on at a time.
    form.querySelectorAll('[data-single]').forEach(function (g) {
      g.addEventListener('change', function (e) {
        if (e.target.checked) g.querySelectorAll('input').forEach(function (i) { if (i !== e.target) i.checked = false; });
      });
    });
    form.addEventListener('change', function () { apply(); syncUrl(); });
    form.addEventListener('submit', function (e) {
      e.preventDefault(); apply(); syncUrl();
      var res = document.querySelector('.hfs-results');
      if (res && window.matchMedia('(max-width: 860px)').matches) res.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    form.addEventListener('reset', function () {
      setTimeout(function () {
        form.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = false; });
        apply(); syncUrl();
      }, 0);
    });
    apply();
  }
})();

// Lot map: hover card for each lot (two styles while we choose), click goes to the lot's floor plan
(function () {
  document.querySelectorAll(".lotmap").forEach(function (map) {
    var box = map.querySelector(".lotmap-scroll");
    var card = map.querySelector(".lotmap-card");
    var data = {};
    try { data = JSON.parse(map.querySelector(".lotmap-plans").textContent); } catch (e) {}
    var hideTimer = null, current = null;
    var LABEL = { available: "Available", sold: "Sold", model: "Model home", future: "Future model", sales: "Sales Center", upcoming: "Future release" };
    var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

    function target(g) {
      var p = data[g.getAttribute("data-plan")], st = g.getAttribute("data-status");
      if (p) return p.url;
      if (st === "sales") return "/contact-us";
      if (st === "available" || st === "upcoming") return "/floor-plans";
      if (st === "sold") return "/homes-for-sale";
      return null;
    }

    function html(g) {
      var n = g.getAttribute("data-lot"), st = g.getAttribute("data-status"), p = data[g.getAttribute("data-plan")];
      var url = target(g), label = LABEL[st] || st;
      var detail = map.classList.contains("card-detail");
      var tag = url ? "a" : "div", href = url ? ' href="' + url + '"' : "";
      if (!detail) {
        var name = p ? p.name : (st === "available" ? "Choose your plan" : st === "sold" ? "Sold" : label);
        var meta = "Lot " + n + (p ? " &middot; " + p.sqft + " ft&sup2;" : " &middot; " + label);
        return "<" + tag + ' class="lmc-card"' + href + ">" +
          (p && p.img ? '<span class="lmc-img"><img src="' + p.img + '" alt=""></span>' : "") +
          '<span class="lmc-bar"><span class="lmc-meta">' + meta + '</span><span class="lmc-name">' + esc(name) + "</span>" +
          (url ? '<span class="po-go" aria-hidden="true"></span>' : "") + "</span></" + tag + ">";
      }
      var body;
      if (p) {
        body = '<span class="lmc-eyebrow">Lot ' + n + "</span>" +
          '<span class="lmc-title">The ' + esc(p.name) + "</span>" +
          '<span class="lmc-spec">' + p.sqft + " ft&sup2; | " + esc(p.spec) + "</span>" +
          (st === "sold" ? '<span class="lmc-note">This homesite has sold. The ' + esc(p.name) + " is still available on other homesites.</span>"
                         : '<span class="lmc-price">' + esc(p.price) + "</span>") +
          '<span class="lmc-cta">View the floor plan<span class="lmc-arrow" aria-hidden="true"></span></span>';
      } else if (st === "available" || st === "upcoming") {
        body = '<span class="lmc-eyebrow">Lot ' + n + "</span>" +
          '<span class="lmc-title">' + (st === "upcoming" ? "Coming in a future release" : "Ready for your plan") + "</span>" +
          '<span class="lmc-note">Pair this homesite with one of our seven floor plans, from the Hamlet to the Amberly.</span>' +
          '<span class="lmc-cta">Explore floor plans<span class="lmc-arrow" aria-hidden="true"></span></span>';
      } else if (st === "sold") {
        body = '<span class="lmc-eyebrow">Lot ' + n + '</span><span class="lmc-title">This homesite has sold.</span>' +
          '<span class="lmc-cta">See homes for sale<span class="lmc-arrow" aria-hidden="true"></span></span>';
      } else {
        body = '<span class="lmc-eyebrow">Lot ' + n + '</span><span class="lmc-title">' + label + "</span>" +
          (url ? '<span class="lmc-cta">Talk with our sales team<span class="lmc-arrow" aria-hidden="true"></span></span>' : "");
      }
      return "<" + tag + ' class="lmc-card lmc-detail"' + href + ">" +
        (p && p.img ? '<span class="lmc-img"><img src="' + p.img + '" alt=""><span class="lmc-pill is-' + st + '">' + label + "</span></span>"
                    : '<span class="lmc-pill is-' + st + ' solo">' + label + "</span>") +
        '<span class="lmc-body">' + body + "</span></" + tag + ">";
    }

    function show(g) {
      clearTimeout(hideTimer);
      if (current) current.classList.remove("is-hot");
      current = g; g.classList.add("is-hot");
      card.innerHTML = html(g);
      card.hidden = false;
      var r = g.getBoundingClientRect(), b = box.getBoundingClientRect();
      var cw = card.offsetWidth, ch = card.offsetHeight;
      var x = r.left - b.left + box.scrollLeft + r.width / 2 - cw / 2;
      x = Math.max(box.scrollLeft + 6, Math.min(x, box.scrollLeft + b.width - cw - 6));
      var y = r.top - b.top - ch - 10;
      var below = y < -b.top + 90;  // no room above (under the sticky header): open below the lot
      if (below) y = r.bottom - b.top + 10;
      card.style.left = x + "px"; card.style.top = y + "px";
      card.classList.toggle("is-below", below);
    }
    function hideSoon() {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(function () { card.hidden = true; if (current) current.classList.remove("is-hot"); current = null; }, 180);
    }
    card.addEventListener("mouseenter", function () { clearTimeout(hideTimer); });
    card.addEventListener("mouseleave", hideSoon);

    var touch = false;
    box.addEventListener("pointerdown", function (e) { touch = e.pointerType !== "mouse"; });
    box.querySelectorAll(".lm-lot[data-tip]").forEach(function (g) {
      g.addEventListener("mouseenter", function () { if (!touch) show(g); });
      g.addEventListener("mouseleave", hideSoon);
      g.addEventListener("focus", function () { show(g); });
      g.addEventListener("blur", hideSoon);
      g.addEventListener("click", function () {
        // mouse: straight to the floor plan. touch: first tap opens the card, the card is the link
        if (!touch && target(g)) { location.href = target(g); return; }
        show(g);
      });
      g.addEventListener("keydown", function (e) { if (e.key === "Enter" && target(g)) location.href = target(g); });
    });
    document.addEventListener("click", function (e) { if (!map.contains(e.target)) { card.hidden = true; } });

    // preview switch between the two card styles
    var prev = map.previousElementSibling;
    function setStyle(k) {
      map.classList.toggle("card-light", k === "light");
      map.classList.toggle("card-detail", k === "detail");
      if (prev) prev.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-card") === k ? "true" : "false"); });
      if (current && !card.hidden) show(current);
    }
    if (prev && prev.classList.contains("lotmap-preview")) {
      prev.querySelectorAll("button").forEach(function (b) { b.addEventListener("click", function () { setStyle(b.getAttribute("data-card")); }); });
    }
    if (/[?&]card=detail/.test(location.search)) setStyle("detail");
  });
})();
