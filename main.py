import requests
import pandas as pd
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# --- NUEVA CONFIGURACIÓN DEL ESCORPIANO ---
PRECIO_MIN = 68000
PRECIO_MAX = 78000
# ------------------------------------------

bot_data = {'position': 0, 'last_op': "ESPERANDO SEÑAL", 'balance': 100, 'precios': []}

def calcular_rsi(precios, periodo=14):
    if len(precios) < periodo + 1: return 50
    df = pd.DataFrame(precios, columns=['p'])
    delta = df['p'].diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    pérdida = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = ganancia / pérdida
    return 100 - (100 / (1 + rs)).iloc[-1]

@app.route('/')
def home():
    html = """
    <html>
        <head><meta http-equiv="refresh" content="30"></head>
        <body style="background:#131722; color:white; font-family:sans-serif; text-align:center;">
            <h1>🦂 ESCORPIANO V1 - RANGO $68k - $78k</h1>
            <div style="display:flex; justify-content:space-around; font-size:20px; background:#1e222d; padding:10px; border-bottom: 2px solid orange;">
                <p>Saldo: <b>$<span id="balance">{{balance}}</span></b></p>
                <p>RSI (14): <b><span id="rsi_val">--</span></b></p>
                <p>Precio BTC: <b>$<span id="precio">--</span></b></p>
            </div>
            <p style="color: #aaa;">Estado: <span id="op" style="color:orange;">{{last_op}}</span></p>
            
            <div id="chart" style="height:500px; width:100%;"></div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script>
                new TradingView.widget({"width": "100%", "height": 500, "symbol": "BINANCE:BTCUSDT", "interval": "1", "theme": "dark", "container_id": "chart"});
                
                setInterval(() => {
                    fetch('/status').then(r => r.json()).then(data => {
                        document.getElementById('precio').innerText = data.price;
                        document.getElementById('rsi_val').innerText = data.rsi ? data.rsi.toFixed(2) : "--";
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
        res = requests.get(url, timeout=5).json()
        precio = res['USD']
        
        bot_data['precios'].append(precio)
        if len(bot_data['precios']) > 50: bot_data['precios'].pop(0)
        
        rsi = calcular_rsi(bot_data['precios'])
        
        # LÓGICA DENTRO DE LA FRANJA 68k-78k
        if PRECIO_MIN <= precio <= PRECIO_MAX:
            if rsi <= 30 and bot_data['position'] == 0:
                bot_data['position'] = 1
                bot_data['last_op'] = f"COMPRADO A ${precio} (RSI BAJO)"
            elif rsi >= 70 and bot_data['position'] == 1:
                bot_data['position'] = 0
                bot_data['last_op'] = f"VENDIDO A ${precio} (RSI ALTO)"
                bot_data['balance'] += 3 # Ganancia simulada
        else:
            bot_data['last_op'] = "FUERA DE RANGO (PAUSA)"
        
        return jsonify({"price": precio, "rsi": rsi, "balance": bot_data['balance'], "last_op": bot_data['last_op']})
    except:
        return jsonify({"error": "Error de antena"})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
