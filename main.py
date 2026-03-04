import os, requests
import pandas as pd
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Memoria del bot (Vive en el servidor)
bot_data = {
    "balance": 10192.28, # Empezamos desde donde dejaste
    "position": 0,
    "entry_price": 0.0,
    "last_op": "BOT CONECTADO AL RSI REAL 🟢",
    "pnl": 0.0
}

def calcular_rsi_real():
    try:
        # Traemos las últimas 100 velas de 1 minuto
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
        r = requests.get(url).json()
        precios = pd.Series([float(vela[4]) for vela in r]) # Precio de cierre
        
        # Fórmula RSI con EMA (Igual a TradingView)
        delta = precios.diff()
        subidas = delta.clip(lower=0)
        bajadas = -delta.clip(upper=0)
        ema_subida = subidas.ewm(com=13, adjust=False).mean()
        ema_bajada = bajadas.ewm(com=13, adjust=False).mean()
        rs = ema_subida / ema_bajada
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2)
    except:
        return 50.0

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;">
                <div style="color:#888; font-size:0.8em;">SALDO EN SERVIDOR</div>
                <div id="balance" style="color:#4f4; font-size:1.5em; font-weight:bold;">$0.00</div>
            </div>
            <div style="text-align:center;">
                <div style="color:#888; font-size:0.8em;">BTC REAL-TIME</div>
                <div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">$0.00</div>
            </div>
        </div>

        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
            <div>RSI ACTUAL: <b id="rsi" style="color:#0af;">--</b></div>
            <div id="last_op" style="font-size:0.8em; color:#aaa;">SINCRONIZANDO...</div>
        </div>
        
        <div style="height:450px; border:1px solid #333; border-radius:8px; overflow:hidden;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            async function actualizar() {
                try {
                    const res = await fetch('/status');
                    const d = await res.json();
                    document.getElementById('balance').innerText = "$" + d.balance.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('price').innerText = "$" + d.price.toLocaleString();
                    document.getElementById('rsi').innerText = d.rsi;
                    document.getElementById('last_op').innerText = d.last_op;
                } catch (e) {}
            }
            setInterval(actualizar, 2000);
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    # El bot pide el precio y el RSI a Binance de verdad
    p_req = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
    p_actual = float(p_req['price'])
    rsi_actual = calcular_rsi_real()
    
    # Lógica de Trading Real
    if bot_data["position"] == 1:
        bot_data["pnl"] = p_actual - bot_data["entry_price"]
        # Venta: RSI > 70 o pérdida de $300 (Stop Loss)
        if rsi_actual >= 70 or bot_data["pnl"] < -300:
            bot_data["balance"] += bot_data["pnl"]
            bot_data["position"] = 0
            bot_data["last_op"] = f"VENTA CERRADA A ${p_actual}"
            bot_data["pnl"] = 0.0
    else:
        # Compra: RSI < 30 y precio en tu rango
        if rsi_actual <= 30 and 63000 <= p_actual <= 75000:
            bot_data["position"] = 1
            bot_data["entry_price"] = p_actual
            bot_data["last_op"] = f"COMPRA REALIZADA A ${p_actual}"

    return jsonify({"balance": bot_data["balance"], "price": p_actual, "rsi": rsi_actual, "last_op": bot_data["last_op"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
