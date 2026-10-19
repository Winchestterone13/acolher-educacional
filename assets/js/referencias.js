document.getElementById('copy-references').addEventListener('click', async () => {
  const field = document.getElementById('reference-text');
  const status = document.getElementById('copy-status');
  try {
    await navigator.clipboard.writeText(field.value);
    status.textContent = 'Referências copiadas!';
  } catch (_) {
    field.focus(); field.select();
    status.textContent = 'Lista selecionada. Use Ctrl+C ou a opção Copiar do seu dispositivo.';
  }
});
