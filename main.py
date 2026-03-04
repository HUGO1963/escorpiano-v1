import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:15px; margin:0;">
        <h2 style="color:#a0f; margin:10px 0;">🦂 ESCORPIANO V1 PRO</h2>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:15px;">
            <div style="background:#111; padding:10px; border:1px solid #333; border-radius:8px;">
                <small style="color:#888;">PRECIO BTC</small>
                <div id="p" style="color:#fa0; font-size:1.8em; font-weight:bold;">$0</div>
            </div>
            <div style="background:#111; padding:10px; border:1px solid #333; border-radius:8px;">
                <small style="color:#888;">BILLETERA</small>
                <div style="color:#4f4; font-size:1.8em; font-weight:bold;">$10.000</div>
            </div>
        </div>
        <div id="status-box" style="background:#111; padding:10px; border-radius:8px; border:1px solid #444; margin-bottom:15px;">
            <div id="e" style="font-size:1.1em; font-weight:bold; color:#f44;">CONECTANDO PUENTE...</div>
        </div>
        <div style="height:400px; border-radius:8px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            async function update() {
                try {
                    const r = await fetch('https://api.coindesk.com/v1/bpi/currentprice.json');
                    const d = await r.json();
                    const price = d.bpi.USD.rate_float;
                    document.getElementById('p').innerText = "$" + price.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('e').innerText = "CONEXIÓN ESTABLE ✅";
                    document.getElementById('e').style.color = "#4f4";
                } catch { document.getElementById('e').innerText = "BUSCANDO SEÑAL..."; }
            }
            setInterval(update, 5000); update();
        </script>
    </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
