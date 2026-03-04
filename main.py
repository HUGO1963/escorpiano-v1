import os, requests, time
from flask import Flask, render_template_string, jsonify
from threading import Thread

app = Flask(__name__)

bot_data = {
    "balance": 10000.0,
    "position": 0,
    "last_op": "INICIANDO...",
    "current_price": 0.0,
    "current_rsi": 50.0
}

def loop_del_bot():
    while True:
        try:
            # Pedimos precio a Binance
            r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
            price = float(r['price'])
            bot_data["current_price"] = price
            
            # Lógica de RSI simplificada para que NO falle el servidor
            # Si el precio baja de 64k, simulamos RSI bajo. Si sube de 70k, RSI alto.
            if price < 64000: bot_data["current_rsi"] = 28
            elif price > 71000: bot_data["current_rsi"] = 72
            else: bot_data["current_rsi"] = 50

            # Operación Automática (Rango 63k-73k)
            if 63000 <= price <= 73000:
                if bot_data["current_rsi"] <= 30 and bot_data["position"] == 0:
                    bot_data["position"] = 1
                    bot_data["last_op"] = f"COMPRA AUTO A ${price}"
                elif bot_data["current_rsi"] >= 70 and bot_data["position"] == 1:
                    bot_data["position"] = 0
                    bot_data["balance"] += 100 # Ganancia fija de prueba
                    bot_data["last_op"] = f"VENTA AUTO A ${price}"
        except: pass
        time.sleep(2)

Thread(target=loop_del_bot, daemon=True).start()

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;"><div style="color:#888; font-size:0.8em;">SALDO SERVIDOR</div><div id="balance" style="color:#4f4; font-size:1.5em; font-weight:bold;">$10,000.00</div></div>
            <div style="text-align:center;"><div style="color:#888; font-size:0.8em;">BTC/USDT</div><div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">0.00</div></div>
            <button onclick="window.close();" style="background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">SALIR ✖</button>
        </div>
        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr;">
            <div>RSI: <b id="rsi" style="color:#0af;">--</b></div>
            <div id="last_op" style="font-size:0.8em; color:#aaa;">ESPERANDO...</div>
        </div>
        <div style="height:500px; border:1px solid #333;"><iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe></div>
        <script>
            async function update() {
                const r = await fetch('/status'); const d = await r.json();
                document.getElementById('balance').innerText = "$" + d.balance.toLocaleString();
                document.getElementById('price').innerText = "$" + d.current_price.toLocaleString();
                document.getElementById('rsi').innerText = d.current_rsi;
                document.getElementById('last_op').innerText = d.last_op;
            }
            setInterval(update, 1000);
        </script>
    </body>
    ''')

@app.route('/status')
def status(): return jsonify(bot_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
