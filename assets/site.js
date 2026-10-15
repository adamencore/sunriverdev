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
    document.addEventListener('click', function (e) { if (!header.contains(e.target)) closeAll(null); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); header.setAttribute('data-menu', 'closed'); } });
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
      var comm = checked('community'), stat = checked('status'), sq = checked('sqft'), hobby = checked('hobby').length > 0;
      var beds = radio('beds'), baths = radio('baths'), garage = radio('garage'), shown = 0;
      cards.forEach(function (c) {
        var d = c.dataset, n = parseFloat(d.sqft);
        var ok = (!comm.length || comm.indexOf(d.community) > -1) &&
          (!stat.length || stat.indexOf(d.status) > -1) &&
          (!sq.length || sq.some(function (r) { var p = r.split('-'); return n >= +p[0] && n <= +p[1]; })) &&
          parseFloat(d.beds) >= beds && parseFloat(d.baths) >= baths && parseFloat(d.garage) >= garage &&
          (!hobby || d.hobby === '1');
        c.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = shown;
      empty.hidden = shown > 0;
    };
    var syncUrl = function () {
      var params = new URLSearchParams();
      ['community', 'status', 'sqft'].forEach(function (k) { checked(k).forEach(function (v) { params.append(k, v); }); });
      ['beds', 'baths', 'garage'].forEach(function (k) { if (radio(k)) params.set(k, radio(k)); });
      if (checked('hobby').length) params.set('hobby', '1');
      var q = params.toString();
      history.replaceState(null, '', location.pathname + (q ? '?' + q : ''));
    };
    // Restore filters from the URL so a filtered view can be shared.
    var initial = new URLSearchParams(location.search);
    if (Array.from(initial.keys()).length) {
      form.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = initial.getAll(i.name).indexOf(i.value) > -1; });
      form.querySelectorAll('input[type="radio"]').forEach(function (i) { i.checked = (initial.get(i.name) || '0') === i.value; });
    }
    form.addEventListener('change', function () { apply(); syncUrl(); });
    form.addEventListener('reset', function () {
      setTimeout(function () {
        form.querySelectorAll('input[type="checkbox"]').forEach(function (i) { i.checked = false; });
        apply(); syncUrl();
      }, 0);
    });
    apply();
  }
})();
