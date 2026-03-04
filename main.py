import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# MEMORIA DEL BOT (Se resetea solo si Render reinicia el servidor)
bot_data = {
    "balance": 10000.0,
    "position": 0,  # 0: nada, 1: comprado
    "entry_price": 0.0,
    "last_op": "ESPERANDO..."
}

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;">
                <div style="color:#888; font-size:0.8em;">SALDO EN SERVIDOR</div>
                <div id="balance" style="color:#4f4; font-size:1.5em; font-weight:bold;">$10,000.00</div>
            </div>
            <button onclick="window.close();" style="background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">SALIR ✖</button>
        </div>

        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr;">
            <div><span style="color:#888;">ESTADO:</span> <b id="bot_status">--</b></div>
            <div><span style="color:#888;">ULT. OP:</span> <b id="last_op" style="color:#0af;">--</b></div>
        </div>
        
        <div style="height:500px; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            async function refresh() {
                const res = await fetch('/get_data');
                const d = await res.json();
                document.getElementById('balance').innerText = "$" + d.balance.toLocaleString();
                document.getElementById('bot_status').innerText = d.position === 1 ? "COMPRADO ✅" : "BUSCANDO...";
                document.getElementById('last_op').innerText = d.last_op;
            }
            setInterval(refresh, 2000);
        </script>
    </body>
    ''')

@app.route('/get_data')
def get_data():
    # Aquí es donde el BOT TRABAJA SOLO en el servidor
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=2).json()
        price = float(r['price'])
        
        # Simulación de RSI (Necesitaríamos 14 velas para el real, por ahora lógica de rango)
        # Rango: 63000 - 73000
        if 63000 <= price <= 73000:
            # Lógica simple para testear persistencia
            if price < 64000 and bot_data["position"] == 0:
                bot_data["position"] = 1
                bot_data["entry_price"] = price
                bot_data["last_op"] = f"COMPRA A {price}"
            elif price > 70000 and bot_data["position"] == 1:
                profit = price - bot_data["entry_price"]
                bot_data["balance"] += profit
                bot_data["position"] = 0
                bot_data["last_op"] = f"VENTA GANANCIA: {profit:.2f}"
    except:
        pass
    return jsonify(bot_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
