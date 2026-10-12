// SunRiver site interactions: header menus, mobile nav, demo form handling.
(function () {
  var header = document.querySelector('.site-header');
  if (!header) return;

  var toggle = header.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = header.getAttribute('data-menu') === 'open';
      header.setAttribute('data-menu', open ? 'closed' : 'open');
      toggle.setAttribute('aria-expanded', String(!open));
    });
  }

  var items = header.querySelectorAll('.nav-item');
  function closeAll(except) {
    items.forEach(function (it) {
      if (it !== except) {
        it.setAttribute('data-open', 'false');
        var b = it.querySelector('.nav-link');
        if (b) b.setAttribute('aria-expanded', 'false');
      }
    });
  }
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
    if (window.matchMedia('(hover: hover) and (min-width: 981px)').matches) {
      var t;
      item.addEventListener('mouseenter', function () { clearTimeout(t); closeAll(item); item.setAttribute('data-open', 'true'); btn.setAttribute('aria-expanded', 'true'); });
      item.addEventListener('mouseleave', function () { t = setTimeout(function () { item.setAttribute('data-open', 'false'); btn.setAttribute('aria-expanded', 'false'); }, 160); });
    }
  });
  document.addEventListener('click', function (e) { if (!header.contains(e.target)) closeAll(null); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(null); header.setAttribute('data-menu', 'closed'); } });

  // Forms: placeholder handler until the form is wired to the CRM.
  document.querySelectorAll('form[data-demo]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.form-note');
      if (note) { note.hidden = false; note.textContent = 'Thanks! A SunRiver team member will reach out soon.'; }
      form.querySelectorAll('input, textarea, button').forEach(function (el) { el.disabled = true; });
    });
  });
})();
