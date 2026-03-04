import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# MEMORIA DEL BOT (Mantenemos tu capital ganado)
bot_data = {
    "balance": 10192.28,
    "position": 0,
    "entry_price": 0.0,
    "last_op": "SISTEMA LIVIANO CONECTADO 🟢"
}

def get_rsi_simple():
    try:
        # Traemos velas de 1 minuto de Binance
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=15"
        data = requests.get(url).json()
        precios = [float(c[4]) for c in data]
        
        subidas = 0
        bajadas = 0
        for i in range(1, len(precios)):
            dif = precios[i] - precios[i-1]
            if dif > 0: subidas += dif
            else: bajadas -= dif
        
        if bajadas == 0: return 100.0
        rs = subidas / bajadas
        return round(100 - (100 / (1 + rs)), 2)
    except:
        return 50.0

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="background:#111; padding:20px; border-radius:10px; border:1px solid #333; max-width:500px; margin:auto; margin-top:20px;">
            <div style="color:#888; font-size:0.9em;">SALDO EN LA NUBE</div>
            <div style="font-size:2.5em; color:#4f4; font-weight:bold; margin:10px 0;">$ <span id="balance">0.00</span></div>
            <div style="display:grid; grid-template-columns:1fr 1fr; border-top:1px solid #333; padding-top:15px;">
                <div>RSI REAL: <b id="rsi" style="color:#0af;">--</b></div>
                <div>BTC: <b id="price" style="color:#fa0;">--</b></div>
            </div>
            <div id="last_op" style="margin-top:15px; font-size:0.8em; color:#aaa; font-style:italic;">Sincronizando...</div>
        </div>
        <div style="margin-top:20px; height:450px; border-radius:10px; overflow:hidden; border:1px solid #333; max-width:800px; margin-left:auto; margin-right:auto;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            async function update(){
                try {
                    const res = await fetch('/status');
                    const d = await res.json();
                    document.getElementById('balance').innerText = d.balance.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('rsi').innerText = d.rsi;
                    document.getElementById('price').innerText = d.price.toLocaleString();
                    document.getElementById('last_op').innerText = d.last_op;
                } catch(e){}
            }
            setInterval(update, 3000);
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    try:
        p_req = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        p = float(p_req['price'])
        rsi = get_rsi_simple()
        
        # Lógica del Bot
        if bot_data["position"] == 1:
            pnl = p - bot_data["entry_price"]
            if rsi >= 70 or pnl < -300:
                bot_data["balance"] += pnl
                bot_data["position"] = 0
                bot_data["last_op"] = f"VENTA EJECUTADA A ${p}"
        else:
            if rsi <= 30:
                bot_data["position"] = 1
                bot_data["entry_price"] = p
                bot_data["last_op"] = f"COMPRA EJECUTADA A ${p}"
                
        return jsonify({"balance": round(bot_data["balance"], 2), "price": p, "rsi": rsi, "last_op": bot_data["last_op"]})
    except:
        return jsonify({"balance": bot_data["balance"], "price": 0, "rsi": 50, "last_op": "Error de conexión con Binance"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
