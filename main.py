import requests
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# --- CONFIGURACIÓN DEL ESCORPIANO ---
PRECIO_MIN = 68000
PRECIO_MAX = 78000
bot_data = {'position': 0, 'last_op': "ESPERANDO RSI", 'balance': 100, 'precios': []}

def calcular_rsi_simple(precios, periodo=14):
    if len(precios) < periodo + 1: return 50
    subidas = 0
    bajadas = 0
    for i in range(1, periodo + 1):
        dif = precios[-i] - precios[-i-1]
        if dif > 0: subidas += dif
        else: bajadas -= dif
    if bajadas == 0: return 100
    rs = (subidas / periodo) / (bajadas / periodo)
    return 100 - (100 / (1 + rs))

@app.route('/')
def home():
    html = """
    <html>
        <body style="background:#131722; color:white; font-family:sans-serif; text-align:center;">
            <h1 style="color:orange;">🦂 ESCORPIANO V1 - RANGO 68k-78k</h1>
            <div style="display:flex; justify-content:space-around; font-size:22px; background:#1e222d; padding:15px; border-radius:10px;">
                <p>Saldo: <b>$<span id="balance">{{balance}}</span></b></p>
                <p>RSI: <b><span id="rsi_val">--</span></b></p>
                <p>BTC: <b>$<span id="precio">--</span></b></p>
            </div>
            <h2 id="op" style="color:#00ff00;">{{last_op}}</h2>
            <div id="chart" style="height:500px; width:100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script>
                new TradingView.widget({"width": "100%", "height": 500, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "container_id": "chart"});
                setInterval(() => {
                    fetch('/status').then(r => r.json()).then(data => {
                        document.getElementById('precio').innerText = data.price;
                        document.getElementById('rsi_val').innerText = data.rsi.toFixed(2);
                        document.getElementById('balance').innerText = data.balance;
                        document.getElementById('op').innerText = data.last_op;
                    });
                }, 5000);
            </script>
        </body>
    </html>
    """
    return render_template_string(html, balance=bot_data['balance'], last_op=bot_data['last_op'])

@app.route('/status')
def status():
    try:
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
        precio = requests.get(url).json()['USD']
        bot_data['precios'].append(precio)
        if len(bot_data['precios']) > 30: bot_data['precios'].pop(0)
        
        rsi = calcular_rsi_simple(bot_data['precios'])
        
        if PRECIO_MIN <= precio <= PRECIO_MAX:
            if rsi <= 30 and bot_data['position'] == 0:
                bot_data['position'] = 1
                bot_data['last_op'] = f"COMPRADO A ${precio}"
            elif rsi >= 70 and bot_data['position'] == 1:
                bot_data['position'] = 0
                bot_data['last_op'] = f"VENDIDO A ${precio}"
                bot_data['balance'] += 3
        else:
            bot_data['last_op'] = "FUERA DE RANGO"
            
        return jsonify({"price": precio, "rsi": rsi, "balance": bot_data['balance'], "last_op": bot_data['last_op']})
    except: return jsonify({"error": "Error"})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
