// script.js – Acolher accessibility features
(function(){
  const root = document.documentElement;
  const increaseBtn = document.getElementById('increase-text');
  const decreaseBtn = document.getElementById('decrease-text');
  const contrastBtn = document.getElementById('toggle-contrast');
  const storageKey = 'acolher-settings';

  // Load saved settings
  let saved = {};
  try {
    saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
  } catch(e) {
    saved = {};
  }

  if (saved.fontSize) setFontSize(saved.fontSize);
  if (saved.highContrast) document.body.classList.add('high-contrast');

  function setFontSize(multiplier){
    root.style.fontSize = multiplier + 'rem';
    try {
      localStorage.setItem(storageKey, JSON.stringify({...saved, fontSize: multiplier}));
    } catch(e){}
  }

  function adjustFont(delta){
    const current = parseFloat(getComputedStyle(root).fontSize);
    const rem = current / 16;
    const newRem = Math.max(0.8, Math.min(1.6, rem + delta));
    setFontSize(newRem);
  }

  if (increaseBtn) increaseBtn.addEventListener('click', () => adjustFont(0.1));
  if (decreaseBtn) decreaseBtn.addEventListener('click', () => adjustFont(-0.1));
  if (contrastBtn) contrastBtn.addEventListener('click', () => {
    document.body.classList.toggle('high-contrast');
    const isHigh = document.body.classList.contains('high-contrast');
    saved.highContrast = isHigh;
    try {
      localStorage.setItem(storageKey, JSON.stringify(saved));
    } catch(e){}
  });
})();

// ── Clean URLs (Esconde .html e index.html da barra de endereços) ──
(function setupCleanUrls() {
  function getCleanPath(pathname) {
    if (pathname.endsWith('/index.html')) {
      return pathname.slice(0, -10) || '/';
    }
    if (pathname === '/index.html' || pathname === 'index.html') {
      return '/';
    }
    if (pathname.endsWith('.html')) {
      return pathname.slice(0, -5);
    }
    return pathname;
  }

  function cleanUrlBar() {
    if (window.location.protocol !== 'http:' && window.location.protocol !== 'https:') return;
    try {
      const currentPath = window.location.pathname;
      const cleanPath = getCleanPath(currentPath);
      if (cleanPath !== currentPath) {
        const fullCleanUrl = cleanPath + window.location.search + window.location.hash;
        window.history.replaceState(null, '', fullCleanUrl);
      }
    } catch (e) {}
  }

  // Executa imediatamente na inicialização
  cleanUrlBar();
  window.addEventListener('hashchange', cleanUrlBar);

  // Normaliza os links internos no carregamento do DOM
  document.addEventListener('DOMContentLoaded', () => {
    const isWeb = window.location.protocol === 'http:' || window.location.protocol === 'https:';

    document.querySelectorAll('a[href]').forEach(a => {
      let href = a.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:')) {
        return;
      }

      if (isWeb) {
        // Na web (GitHub Pages / Vercel), remove index.html e .html dos links
        if (href.startsWith('index.html#')) {
          a.setAttribute('href', './' + href.slice(10));
        } else if (href === 'index.html') {
          a.setAttribute('href', './');
        } else if (href.endsWith('.html')) {
          a.setAttribute('href', href.slice(0, -5));
        }
      } else {
        // No protocolo local file://, garante que os links tenham .html
        if (href === './' || href === '.') {
          a.setAttribute('href', 'index.html');
        } else if (href.startsWith('./#')) {
          a.setAttribute('href', 'index.html' + href.slice(2));
        } else if (!href.includes('.html') && !href.startsWith('#')) {
          a.setAttribute('href', href + '.html');
        }
      }
    });
  });
})();
