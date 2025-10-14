const extractBtn = document.getElementById('extract');
const firInput = document.getElementById('fir');
const output = document.getElementById('output');

extractBtn.onclick = async () => {
  const text = firInput.value.trim();
  if (!text) { alert('Please paste FIR text'); return; }
  output.textContent = 'Processing...';
  try {
    const resp = await fetch('/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!resp.ok) {
      const txt = await resp.text();
      output.textContent = 'Server error: ' + resp.status + '\n' + txt;
      return;
    }
    const data = await resp.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    output.textContent = 'Error: ' + e.message;
  }
};