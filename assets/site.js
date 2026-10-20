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

// Lot map tooltip
(function () {
  document.querySelectorAll(".lotmap-scroll").forEach(function (box) {
    var tip = box.querySelector(".lotmap-tip");
    function show(g) {
      var r = g.getBoundingClientRect(), b = box.getBoundingClientRect();
      tip.textContent = g.getAttribute("data-tip");
      tip.style.left = (r.left - b.left + box.scrollLeft + r.width / 2) + "px";
      tip.style.top = (r.top - b.top + 6) + "px";
      tip.hidden = false;
    }
    box.querySelectorAll(".lm-lot[data-tip]").forEach(function (g) {
      g.addEventListener("mouseenter", function () { show(g); });
      g.addEventListener("focus", function () { show(g); });
      g.addEventListener("click", function () { show(g); });
      g.addEventListener("mouseleave", function () { tip.hidden = true; });
      g.addEventListener("blur", function () { tip.hidden = true; });
    });
  });
})();
