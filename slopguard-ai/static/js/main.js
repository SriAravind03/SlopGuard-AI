const textEditor = document.querySelector('#text');
if (textEditor) {
  const count = document.querySelector('#char-count');
  const update = () => { count.textContent = `${textEditor.value.length.toLocaleString()} / 50,000`; };
  textEditor.addEventListener('input', update); update();
}
