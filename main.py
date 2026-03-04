import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# CONFIGURACIÓN MINIMALISTA PARA 512MB
bot = {"ars": 10000.0, "btc": 0.0, "est": "ESPERANDO", "hist": []}

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#fff; font-family:sans-serif; text-align:center; padding:20px;">
        <h2 style="color:#a0f;">🦂 ESCORPIANO V1 PRO</h2>
        <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333;">
            <p>PRECIO BTC: <span id="p" style="color:#fa0; font-size:1.5em;">$0</span></p>
            <p id="e" style="font-weight:bold; font-size:1.2em;">CONECTANDO...</p>
        </div>
        <div style="height:400px; margin-top:20px;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            setInterval(() => {
                fetch('/status').then(r => r.json()).then(d => {
                    document.getElementById('p').innerText = "$" + d.p.toLocaleString();
                    document.getElementById('e').innerText = d.est;
                    document.getElementById('e').style.color = d.p > 100000 ? "#f44" : "#4f4";
                });
            }, 3000);
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        p = float(r['price'])
        # Lógica simple de rango
        est = "BUSCANDO COMPRA" if p < 100000 else "PAUSADO (PRECIO ALTO)"
        return jsonify({"p": p, "est": est})
    except:
        return jsonify({"p": 0, "est": "ERROR DE CONEXIÓN"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
