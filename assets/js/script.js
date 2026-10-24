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
