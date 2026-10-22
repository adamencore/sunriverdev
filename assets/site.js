// SunRiver site interactions: header menu, forms, galleries, lightbox, homes-for-sale filters.
(function () {
  // ---------- Header
  var header = document.querySelector('.site-header');
  if (header) {
    var toggle = header.querySelector('.menu-toggle');
    if (toggle) {
      // Mobile: the menu button opens the full-screen menu sheet (Figma "Mobile Nav")
      var sheet = document.getElementById('m-nav');
      var openSheet = function () {
        if (!sheet) return;
        sheet.hidden = false; void sheet.offsetWidth; sheet.classList.add('is-open');
        document.body.classList.add('m-nav-lock'); toggle.setAttribute('aria-expanded', 'true');
        var c = sheet.querySelector('.m-nav-close'); if (c) c.focus();
      };
      var closeSheet = function () {
        if (!sheet || sheet.hidden) return;
        sheet.classList.remove('is-open'); document.body.classList.remove('m-nav-lock'); toggle.setAttribute('aria-expanded', 'false');
        setTimeout(function () { if (!sheet.classList.contains('is-open')) sheet.hidden = true; }, 280);
        toggle.focus();
      };
      toggle.setAttribute('aria-controls', 'm-nav');
      toggle.addEventListener('click', openSheet);
      if (sheet) {
        sheet.querySelector('.m-nav-close').addEventListener('click', closeSheet);
        sheet.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { if (a.hash && a.pathname === location.pathname) closeSheet(); }); });
        document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSheet(); });
        // drill-down: Life at SunRiver slides to its own panel, Back slides home
        var panels = sheet.querySelectorAll('.m-nav-panel');
        var goPanel = function (name) {
          sheet.classList.toggle('at-life', name === 'life');
          panels.forEach(function (p) { var on = p.getAttribute('data-panel') === name; p.inert = !on; p.setAttribute('aria-hidden', on ? 'false' : 'true'); });
          var opener = sheet.querySelector('[data-go="life"]'); if (opener) opener.setAttribute('aria-expanded', name === 'life' ? 'true' : 'false');
          var f = sheet.querySelector('.m-nav-panel[data-panel="' + name + '"] ' + (name === 'life' ? '.m-nav-back' : '.m-nav-row')); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 60);
        };
        sheet.querySelectorAll('[data-go]').forEach(function (b) { b.addEventListener('click', function () { goPanel(b.getAttribute('data-go')); }); });
        toggle.addEventListener('click', function () { goPanel('main'); var c = sheet.querySelector('.m-nav-close'); if (c) c.focus(); });
      }
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

  // ---------- Header on scroll (like tripointehomes.com): logo and nav scroll away with the page.
  // Scrolling back up brings the nav pill back, floating at the top, without the logo; at the very top
  // the full header (logo included) is back in place.
  if (header) {
    var lastY = window.scrollY || 0, ticking = false, H = function () { return header.offsetHeight + 40; };
    var onScroll = function () {
      ticking = false;
      var y = window.scrollY || window.pageYOffset, dy = y - lastY;
      var menuOpen = header.getAttribute('data-menu') === 'open';
      if (y <= 4) {
        header.classList.remove('is-fixed', 'is-shown', 'is-anim');
      } else if (!header.classList.contains('is-fixed')) {
        if (y > H()) { header.classList.add('is-fixed'); void header.offsetWidth; header.classList.add('is-anim'); }
      } else if (Math.abs(dy) > 4 && !menuOpen) {
        if (dy < 0) header.classList.add('is-shown');
        else {
          header.classList.remove('is-shown');
          header.querySelectorAll('.nav-item[data-open="true"]').forEach(function (n) { n.setAttribute('data-open', 'false'); var b = n.querySelector('.nav-link'); if (b) b.setAttribute('aria-expanded', 'false'); });
        }
      }
      if (Math.abs(dy) > 4) lastY = y;
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
      var wasOpen = card.classList.contains("is-open");
      card.innerHTML = html(g);
      card.hidden = false;
      card.classList.toggle("is-moving", wasOpen);  // already open: glide to the new lot instead of popping
      var r = g.getBoundingClientRect(), b = box.getBoundingClientRect();
      var cw = card.offsetWidth, ch = card.offsetHeight;
      var x = r.left - b.left + box.scrollLeft + r.width / 2 - cw / 2;
      x = Math.max(box.scrollLeft + 6, Math.min(x, box.scrollLeft + b.width - cw - 6));
      var y = r.top - b.top - ch - 10;
      var below = y < 8 || r.top - ch - 10 < 90;  // no room above in the window (or under the sticky header): open below
      if (below) y = Math.min(r.bottom - b.top + 10, b.height - ch - 8);
      card.style.left = x + "px"; card.style.top = y + "px";
      card.classList.toggle("is-below", below);
      if (!wasOpen) { void card.offsetWidth; }
      card.classList.add("is-open");
    }
    function close() {
      card.classList.remove("is-open");
      if (current) current.classList.remove("is-hot");
      current = null;
      setTimeout(function () { if (!card.classList.contains("is-open")) card.hidden = true; }, 200);
    }
    function hideSoon() {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(close, 140);
    }
    map.addEventListener("lotmap:close", close);
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
    document.addEventListener("click", function (e) { if (!map.contains(e.target)) close(); });

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

// Lot map window: drag to pan, pinch, ctrl/trackpad-pinch wheel or the buttons to zoom
(function () {
  document.querySelectorAll(".lotmap-window").forEach(function (win) {
    var stage = win.querySelector(".lotmap-stage");
    var map = win.closest(".lotmap");
    var hint = win.querySelector(".lotmap-hint");
    var zin = win.querySelector('[data-zoom="in"]'), zout = win.querySelector('[data-zoom="out"]');
    var W = 1000, H = 1000 * 1049.15 / 622.66, MAXK = 4.5;
    var fit = 1, s = 1, x = 0, y = 0;

    function closeCard() { map && map.dispatchEvent(new CustomEvent("lotmap:close")); }
    function dismissHint() { if (hint) hint.classList.add("is-gone"); }
    function clamp() {
      var vw = win.clientWidth, vh = win.clientHeight, sw = W * s, sh = H * s;
      x = sw <= vw ? (vw - sw) / 2 : Math.min(0, Math.max(vw - sw, x));
      y = sh <= vh ? (vh - sh) / 2 : Math.min(0, Math.max(vh - sh, y));
    }
    function apply(ease) {
      clamp();
      stage.classList.toggle("is-easing", !!ease);
      stage.style.transform = "translate(" + x + "px," + y + "px) scale(" + s + ")";
      var zoomed = s > fit * 1.01;
      win.classList.toggle("is-zoomed", zoomed);
      if (zin) zin.disabled = s >= fit * MAXK * 0.99;
      if (zout) zout.disabled = !zoomed;
    }
    function zoomAt(ns, px, py, ease) {
      ns = Math.max(fit, Math.min(fit * MAXK, ns));
      x = px - (px - x) * (ns / s); y = py - (py - y) * (ns / s); s = ns;
      apply(ease); closeCard(); dismissHint();
    }
    function reset(ease) {
      fit = Math.min(win.clientWidth / W, win.clientHeight / H);
      s = fit; x = 0; y = 0; apply(ease);
    }
    reset(false);
    var lastW = win.clientWidth;
    window.addEventListener("resize", function () {
      if (win.clientWidth === lastW) return;
      lastW = win.clientWidth;
      var rel = s / fit; fit = Math.min(win.clientWidth / W, win.clientHeight / H); s = fit * rel; apply(false);
    });

    win.querySelectorAll("[data-zoom]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.stopPropagation();
        var k = b.getAttribute("data-zoom"), cx = win.clientWidth / 2, cy = win.clientHeight / 2;
        if (k === "in") zoomAt(s * 1.6, cx, cy, true);
        else if (k === "out") zoomAt(s / 1.6, cx, cy, true);
        else { reset(true); closeCard(); }
      });
    });

    // trackpad pinch and ctrl + wheel zoom; a plain wheel still scrolls the page
    win.addEventListener("wheel", function (e) {
      if (!e.ctrlKey && !e.metaKey) return;
      e.preventDefault();
      var r = win.getBoundingClientRect();
      zoomAt(s * Math.exp(-e.deltaY * 0.01), e.clientX - r.left, e.clientY - r.top, false);
    }, { passive: false });

    // drag to pan (mouse, pen, one finger once zoomed) and two-finger pinch
    var pts = {}, start = null, moved = false, pinch = null;
    function count() { return Object.keys(pts).length; }
    win.addEventListener("pointerdown", function (e) {
      if (e.target.closest(".lotmap-zoom, .lotmap-card")) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      moved = false;
      if (count() === 1) start = { px: e.clientX, py: e.clientY, x: x, y: y };
      if (count() === 2) {
        var p = Object.values(pts), r = win.getBoundingClientRect();
        pinch = { d: Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y), s: s,
                  cx: (p[0].x + p[1].x) / 2 - r.left, cy: (p[0].y + p[1].y) / 2 - r.top, x: x, y: y };
      }
    });
    win.addEventListener("pointermove", function (e) {
      if (!pts[e.pointerId]) return;
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      if (pinch && count() >= 2) {
        var p = Object.values(pts), d = Math.hypot(p[0].x - p[1].x, p[0].y - p[1].y);
        var ns = Math.max(fit, Math.min(fit * MAXK, pinch.s * d / pinch.d));
        x = pinch.cx - (pinch.cx - pinch.x) * (ns / pinch.s); y = pinch.cy - (pinch.cy - pinch.y) * (ns / pinch.s); s = ns;
        moved = true; apply(false); closeCard(); dismissHint();
        return;
      }
      if (!start) return;
      // a finger on the un-zoomed map scrolls the page instead of panning
      if (e.pointerType === "touch" && s <= fit * 1.01) return;
      var dx = e.clientX - start.px, dy = e.clientY - start.py;
      if (!moved && Math.hypot(dx, dy) < 5) return;
      if (!moved) { moved = true; win.classList.add("is-dragging"); closeCard(); dismissHint(); try { win.setPointerCapture(e.pointerId); } catch (err) {} }
      x = start.x + dx; y = start.y + dy; apply(false);
    });
    function up(e) {
      delete pts[e.pointerId];
      if (count() < 2) pinch = null;
      if (count() === 0) { start = null; win.classList.remove("is-dragging"); }
    }
    win.addEventListener("pointerup", up);
    win.addEventListener("pointercancel", up);
    // a drag should not count as a click on the lot it ends on
    win.addEventListener("click", function (e) { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true);
    win.addEventListener("dblclick", function (e) {
      if (e.target.closest(".lotmap-zoom, .lotmap-card")) return;
      var r = win.getBoundingClientRect();
      zoomAt(s * 1.8, e.clientX - r.left, e.clientY - r.top, true);
    });
    win.addEventListener("mousedown", function (e) { if (e.detail > 1) e.preventDefault(); });
  });
})();

// Header logo colors: look at what the logo actually sits on (the hero photo under it, with the
// hero's white wash, or the page background) and pick colors that read. The blue wordmark stays blue
// unless the background is dark (then white); the sun rays and "Communities" stay brand yellow
// wherever yellow has enough contrast, otherwise they follow the wordmark color.
(function () {
  var header = document.querySelector(".site-header");
  var logo = header && header.querySelector(".logo-svg");
  if (!logo) return;
  var BLUE = [50, 90, 150], YELLOW = [245, 175, 28], WHITE = [255, 255, 255];
  function lum(c) {
    var a = c.map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
  }
  function lab(c) {
    var v = c.map(function (x) { x /= 255; return x <= 0.04045 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    var X = (v[0] * 0.4124 + v[1] * 0.3576 + v[2] * 0.1805) / 0.95047, Y = v[0] * 0.2126 + v[1] * 0.7152 + v[2] * 0.0722, Z = (v[0] * 0.0193 + v[1] * 0.1192 + v[2] * 0.9505) / 1.08883;
    var f = function (t) { return t > 0.008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116; };
    return [116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))];
  }
  // how different two colors look (CIE76): yellow on a blue sky reads even at similar brightness; yellow on tan does not
  function dE(a, b) { var p = lab(a), q = lab(b); return Math.sqrt(Math.pow(p[0] - q[0], 2) + Math.pow(p[1] - q[1], 2) + Math.pow(p[2] - q[2], 2)); }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function hex(c) { return "rgb(" + c.join(",") + ")"; }
  function apply(wordBg, accentBg) {
    var word = contrast(BLUE, wordBg) >= 3 || contrast(BLUE, wordBg) >= contrast(WHITE, wordBg) ? BLUE : WHITE;
    // brand yellow unless it would wash out (very light or yellow-toned spots); then match the wordmark
    var yOk = contrast(YELLOW, accentBg) >= 2 || dE(YELLOW, accentBg) >= 60;
    var accent = yOk ? YELLOW : (contrast(word, accentBg) >= contrast(YELLOW, accentBg) ? word : YELLOW);
    header.style.setProperty("--logo-word", hex(word));
    header.style.setProperty("--logo-accent", hex(accent));
    header.setAttribute("data-logo", (word === WHITE ? "light" : "dark") + "-" + (accent === YELLOW ? "yellow" : "mono"));
  }
  function parseColor(str) { var m = str && str.match(/\d+(\.\d+)?/g); return m ? m.slice(0, 4).map(Number) : null; }
  function pageColor(el) {
    for (; el && el !== document.documentElement; el = el.parentElement) {
      var c = parseColor(getComputedStyle(el).backgroundColor);
      if (c && (c.length < 4 || c[3] > 0.5)) return c.slice(0, 3);
    }
    var b = parseColor(getComputedStyle(document.body).backgroundColor);
    return b && (b.length < 4 || b[3] > 0) ? b.slice(0, 3) : WHITE;
  }
  // The white wash at the top of the page heroes: about 60% white at the top, gone by ~42% of the height
  function washAt(hero, y) {
    if (!hero.matches(".fh-hero, .hfs-hero, .li-hero")) return 0;
    var t = y / hero.offsetHeight;
    return t < 0.26 ? 0.6 - (0.42 * t / 0.26) : t < 0.42 ? 0.18 * (1 - (t - 0.26) / 0.16) : 0;
  }
  // Average color of a box (page coordinates relative to the hero) as drawn by the hero's cover-fit image
  function sample(img, hero, box) {
    var W = hero.offsetWidth, H = hero.offsetHeight, iw = img.naturalWidth, ih = img.naturalHeight;
    var cs = getComputedStyle(img), pos = (cs.objectPosition || "50% 50%").split(" ");
    var px = parseFloat(pos[0]) / 100, py = parseFloat(pos[1] || "50%") / 100;
    var sc = Math.max(W / iw, H / ih), dw = iw * sc, dh = ih * sc, ox = (W - dw) * px, oy = (H - dh) * py;
    var k = 0.25, cv = document.createElement("canvas");
    cv.width = Math.max(1, Math.round(box.w * k)); cv.height = Math.max(1, Math.round(box.h * k));
    var ctx = cv.getContext("2d");
    ctx.drawImage(img, (box.x - ox) / sc, (box.y - oy) / sc, box.w / sc, box.h / sc, 0, 0, cv.width, cv.height);
    var d = ctx.getImageData(0, 0, cv.width, cv.height).data, r = 0, g = 0, b = 0, n = 0;
    for (var i = 0; i < d.length; i += 4) { r += d[i]; g += d[i + 1]; b += d[i + 2]; n++; }
    var c = [r / n, g / n, b / n], a = washAt(hero, box.y + box.h / 2);
    return c.map(function (v) { return Math.round(v * (1 - a) + 255 * a); });
  }
  var NS = "http://www.w3.org/2000/svg", VB = logo.viewBox.baseVal;
  function brandAccent() { return header.classList.contains("is-home") ? WHITE : YELLOW; }
  function pick(bg) {
    var word = contrast(BLUE, bg) >= 3 || contrast(BLUE, bg) >= contrast(WHITE, bg) ? BLUE : WHITE;
    var brand = brandAccent();
    var ok = brand === WHITE ? contrast(WHITE, bg) >= 1.3 :  // homepage: white accents per the Figma, unless the spot is nearly white
      (contrast(YELLOW, bg) >= 2 || dE(YELLOW, bg) >= 60);
    var accent = ok ? brand : (contrast(word, bg) >= contrast(brand, bg) ? word : brand);
    return [word, accent];
  }
  function ensureDefs() {
    var defs = logo.querySelector("defs.lg-maps");
    if (defs) return defs;
    defs = document.createElementNS(NS, "defs"); defs.setAttribute("class", "lg-maps");
    ["lg-map-word", "lg-map-accent"].forEach(function (id) {
      var p = document.createElementNS(NS, "pattern"), im = document.createElementNS(NS, "image");
      p.setAttribute("id", id); p.setAttribute("patternUnits", "userSpaceOnUse");
      p.setAttribute("x", VB.x); p.setAttribute("y", VB.y); p.setAttribute("width", VB.width); p.setAttribute("height", VB.height);
      im.setAttribute("x", VB.x); im.setAttribute("y", VB.y); im.setAttribute("width", VB.width); im.setAttribute("height", VB.height);
      im.setAttribute("preserveAspectRatio", "none");
      p.appendChild(im); defs.appendChild(p);
    });
    logo.insertBefore(defs, logo.firstChild);
    return defs;
  }
  function paintMaps(img, hero, box) {
    var W = hero.offsetWidth, H = hero.offsetHeight, iw = img.naturalWidth, ih = img.naturalHeight;
    var cs = getComputedStyle(img), pos = (cs.objectPosition || "50% 50%").split(" ");
    var px = parseFloat(pos[0]) / 100, py = parseFloat(pos[1] || "50%") / 100;
    var sc = Math.max(W / iw, H / ih), ox = (W - iw * sc) * px, oy = (H - ih * sc) * py;
    // one cell for about every 5px of logo, read from a 4x larger copy and averaged
    var cols = Math.max(8, Math.round(box.w / 5)), rows = Math.max(4, Math.round(box.h / 5)), K = 4;
    var cv = document.createElement("canvas"); cv.width = cols * K; cv.height = rows * K;
    var ctx = cv.getContext("2d");
    ctx.drawImage(img, (box.x - ox) / sc, (box.y - oy) / sc, box.w / sc, box.h / sc, 0, 0, cv.width, cv.height);
    var d = ctx.getImageData(0, 0, cv.width, cv.height).data;
    var mw = document.createElement("canvas"), ma = document.createElement("canvas");
    mw.width = ma.width = cols; mw.height = ma.height = rows;
    var dw = mw.getContext("2d").createImageData(cols, rows), da = ma.getContext("2d").createImageData(cols, rows);
    var whiteParts = 0;
    for (var r = 0; r < rows; r++) {
      var wash = washAt(hero, box.y + (r + 0.5) * box.h / rows);
      for (var c = 0; c < cols; c++) {
        var R = 0, G = 0, B = 0;
        for (var y = 0; y < K; y++) for (var x = 0; x < K; x++) {
          var i = ((r * K + y) * cv.width + c * K + x) * 4; R += d[i]; G += d[i + 1]; B += d[i + 2];
        }
        var n = K * K, bg = [R / n, G / n, B / n].map(function (v) { return Math.round(v * (1 - wash) + 255 * wash); });
        var pr = pick(bg), o = (r * cols + c) * 4;
        if (pr[0] === WHITE) whiteParts++;
        dw.data[o] = pr[0][0]; dw.data[o + 1] = pr[0][1]; dw.data[o + 2] = pr[0][2]; dw.data[o + 3] = 255;
        da.data[o] = pr[1][0]; da.data[o + 1] = pr[1][1]; da.data[o + 2] = pr[1][2]; da.data[o + 3] = 255;
      }
    }
    mw.getContext("2d").putImageData(dw, 0, 0); ma.getContext("2d").putImageData(da, 0, 0);
    // soften the edges between colors: blur a larger copy (the SVG scales it up smoothly as well)
    var soft = function (m) {
      var o = document.createElement("canvas"); o.width = cols * 4; o.height = rows * 4;
      var x = o.getContext("2d"); x.imageSmoothingEnabled = true; x.filter = "blur(3px)";
      x.drawImage(m, -1, -1, o.width + 2, o.height + 2);
      return o.toDataURL("image/png");
    };
    var defs = ensureDefs(), ims = defs.querySelectorAll("image");
    ims[0].setAttribute("href", soft(mw)); ims[1].setAttribute("href", soft(ma));
    header.style.setProperty("--logo-word", "url(#lg-map-word)");
    header.style.setProperty("--logo-accent", "url(#lg-map-accent)");
    header.setAttribute("data-logo", "map-" + Math.round(100 * whiteParts / (rows * cols)));
  }
  var probe = null;
  function run() {
    if (header.classList.contains("is-fixed")) return;
    var lr = logo.getBoundingClientRect();
    if (!lr.width) return;
    var cx = lr.left + lr.width / 2, cy = lr.top + lr.height / 2;
    header.style.pointerEvents = "none";
    var under = document.elementFromPoint(Math.max(0, cx), Math.max(0, cy));
    header.style.pointerEvents = "";
    var hero = under && under.closest(".fah-hero, .h4-hero");
    var img = hero && hero.querySelector("img");
    if (!hero || !img) { var bg = pageColor(under); apply(bg, bg); return; }
    var hr = hero.getBoundingClientRect();
    var rel = function (x, y, w, h) { return { x: x - hr.left, y: y - hr.top, w: w, h: h }; };
    // Paint a color map behind every part of the logo: each spot of the wordmark and accents gets the
    // color that reads on the photo right behind it, with soft blends where the photo changes.
    var go = function (src) {
      try { paintMaps(src, hero, rel(lr.left, lr.top, lr.width, lr.height)); }
      catch (e) { /* image not readable here: keep the brand colors */ }
    };
    if (img.src.indexOf(location.origin) === 0) {
      if (img.complete && img.naturalWidth) go(img); else img.addEventListener("load", function () { go(img); }, { once: true });
    } else {
      // photos from the image CDN
      if (!probe || probe.dataset.for !== img.currentSrc) {
        probe = new Image(); probe.dataset.for = img.currentSrc;
        // same file, small, through the site's own /cdn-img/ proxy (netlify.toml) so the canvas may read it
        var u = img.currentSrc || img.src;
        probe.src = u.replace(/^https:\/\/cdn\.sanity\.io\/images\/[^/]+\/[^/]+\//, "/cdn-img/").replace(/([?&])w=\d+/, "$1w=800")
          .replace(/^https:\/\/sunriver-website\.vercel\.app\/_next\/static\/media\//, "/vimg/")
          .replace(/^https:\/\/sunriverdev\.netlify\.app\//, "/");
      }
      if (probe.complete && probe.naturalWidth) go(probe); else probe.onload = function () { go(probe); };
    }
  }
  var t;
  function later() { clearTimeout(t); t = setTimeout(run, 120); }
  run();
  window.addEventListener("load", run);
  window.addEventListener("resize", later);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
})();

// Live In flip cards: hover flips them on desktop; a tap flips them on touch screens
document.querySelectorAll(".li-flip").forEach(function (c) {
  c.addEventListener("click", function () { c.classList.toggle("is-flipped"); });
  c.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); c.classList.toggle("is-flipped"); } });
  c.addEventListener("mouseleave", function () { c.classList.remove("is-flipped"); });
});
