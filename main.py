import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# CONFIGURACIÓN ULTRA-LIVIANA PARA 512MB
@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#fff; font-family:sans-serif; text-align:center; padding:20px;">
        <h2 style="color:#a0f;">🦂 ESCORPIANO V1 PRO</h2>
        <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #333; margin-bottom:20px;">
            <p style="margin:0; font-size:0.9em; color:#888;">PRECIO BTC (BINANCE)</p>
            <p id="p" style="color:#fa0; font-size:2.5em; font-weight:bold; margin:10px 0;">$0.00</p>
            <p id="e" style="font-weight:bold; font-size:1.1em; color:#4f4;">CONECTANDO...</p>
        </div>
        <div style="height:450px; border-radius:10px; overflow:hidden;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            function update() {
                fetch('/status').then(r => r.json()).then(d => {
                    document.getElementById('p').innerText = "$" + d.p.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('e').innerText = d.est;
                }).catch(() => {
                    document.getElementById('e').innerText = "RECONECTANDO...";
                });
            }
            setInterval(update, 3000);
            update();
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    try:
        # Pedimos el precio real a Binance
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        price = float(r['price'])
        # Estado simple según tu rango de 100k
        estado = "BUSCANDO COMPRA" if price < 100000 else "PAUSADO (PRECIO ALTO)"
        return jsonify({"p": price, "est": estado})
    except:
        return jsonify({"p": 0, "est": "ERROR DE SEÑAL"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
