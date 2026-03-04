import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# MEMORIA DEL BOT - CAPITAL PROTEGIDO
bot_data = {
    "balance": 10192.28,
    "position": 0,
    "entry_price": 0.0,
    "last_op": "SISTEMA ACTIVO 🟢"
}

def get_data_real():
    try:
        # Pedimos el precio y el RSI en un solo paso
        p_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        k_res = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=15", timeout=5).json()
        
        precio = float(p_res['price'])
        cierres = [float(c[4]) for c in k_res]
        
        # Cálculo manual de RSI rápido
        subidas = sum([c - cierres[i] for i, c in enumerate(cierres[1:]) if c > cierres[i]])
        bajadas = sum([cierres[i] - c for i, c in enumerate(cierres[1:]) if c < cierres[i]])
        rsi = round(100 - (100 / (1 + (subidas/bajadas))), 2) if bajadas != 0 else 50.0
        
        return precio, rsi
    except:
        return 0, 50

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:20px; margin:0;">
        <div style="background:#111; padding:25px; border-radius:15px; border:1px solid #333; max-width:450px; margin:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
            <div style="color:#888; font-size:0.9em; letter-spacing:1px;">CAPITAL ESCORPIANO</div>
            <div style="font-size:2.8em; color:#4f4; font-weight:bold; margin:15px 0;">$ <span id="balance">0.00</span></div>
            
            <div style="display:grid; grid-template-columns:1fr 1fr; border-top:1px solid #333; border-bottom:1px solid #333; padding:15px 0; margin:15px 0;">
                <div><span style="color:#888; font-size:0.8em;">RSI REAL</span><br><b id="rsi" style="color:#0af; font-size:1.4em;">--</b></div>
                <div><span style="color:#888; font-size:0.8em;">PRECIO BTC</span><br><b id="price" style="color:#fa0; font-size:1.4em;">--</b></div>
            </div>
            <div id="last_op" style="font-size:0.9em; color:#aaa; background:#222; padding:10px; border-radius:5px;">Sincronizando...</div>
        </div>
        <div style="margin-top:20px; height:400px; max-width:800px; margin-left:auto; margin-right:auto; border-radius:10px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            async function actualizar(){
                try {
                    const res = await fetch('/status');
                    const d = await res.json();
                    document.getElementById('balance').innerText = d.balance.toLocaleString(undefined, {minimumFractionDigits:2});
                    document.getElementById('rsi').innerText = d.rsi;
                    document.getElementById('price').innerText = d.price.toLocaleString();
                    document.getElementById('last_op').innerText = d.last_op;
                } catch(e){}
            }
            setInterval(actualizar, 1000);
            actualizar();
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    p, rsi = get_data_real()
    if p > 0:
        if bot_data["position"] == 1:
            if rsi >= 70 or (p - bot_data["entry_price"]) < -300:
                bot_data["balance"] += (p - bot_data["entry_price"])
                bot_data["position"] = 0
                bot_data["last_op"] = f"VENTA EJECUTADA A ${p}"
        elif rsi <= 30:
            bot_data["position"] = 1
            bot_data["entry_price"] = p
            bot_data["last_op"] = f"COMPRA EJECUTADA A ${p}"
    
    return jsonify({"balance": round(bot_data["balance"], 2), "price": p, "rsi": rsi, "last_op": bot_data["last_op"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
