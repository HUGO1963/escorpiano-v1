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
        <div id="status-box" style="background:#111; padding:15px; border-radius:8px; border:1px solid #444; margin-bottom:15px;">
            <div id="e" style="font-size:1.2em; font-weight:bold; color:#aaa;">CONECTANDO CON BINANCE...</div>
        </div>
        <button style="background:#f44; color:#fff; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; margin-bottom:15px;">🚨 BOTÓN DE PÁNICO</button>
        <div style="height:400px; border-radius:8px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            function update() {
                fetch('/status').then(r => r.json()).then(d => {
                    document.getElementById('p').innerText = "$" + d.p.toLocaleString();
                    document.getElementById('e').innerText = d.est;
                    document.getElementById('e').style.color = d.p > 0 ? '#4f4' : '#f44';
                }).catch(() => document.getElementById('e').innerText = "REINTENTANDO...");
            }
            setInterval(update, 4000); update();
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    try:
        # Intentamos con la URL alternativa de Binance que es más estable
        r = requests.get("https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=8).json()
        price = float(r['price'])
        return jsonify({"p": price, "est": "API CONECTADA ✅"})
    except Exception as e:
        return jsonify({"p": 0, "est": "ERROR DE CONEXIÓN API ❌"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
