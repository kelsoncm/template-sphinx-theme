// newtheme-sphinx-theme: alternância de tema claro/escuro, lembrada por visitante.
(function () {
  var root = document.documentElement;
  var KEY = 'newtheme-theme';

  try {
    var saved = localStorage.getItem(KEY);
    if (saved === 'light' || saved === 'dark') { root.setAttribute('data-theme', saved); }
  } catch (e) { /* armazenamento indisponível */ }

  function current() {
    var theme = root.getAttribute('data-theme');
    if (theme) { return theme; }
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  document.addEventListener('click', function (event) {
    var button = event.target.closest && event.target.closest('[data-nt-theme-toggle]');
    if (!button) { return; }
    var next = current() === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem(KEY, next); } catch (e) { /* armazenamento indisponível */ }
  });
})();
