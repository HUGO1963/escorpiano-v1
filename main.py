import os
import time
import requests
import pandas as pd
import pandas_ta as ta
from flask import Flask, jsonify

app = Flask(__name__)

# MEMORIA DEL BOT - CAPITAL PROTEGIDO
bot_data = {
    "balance": 10192.28,
    "position": 0,
    "entry_price": 0.0,
    "last_op": "SISTEMA ACTIVO 🟢"
}

def get_data():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=100"
        data = requests.get(url).json()
        df = pd.DataFrame(data, columns=['ts', 'o', 'h', 'l', 'c', 'v', 'ct', 'qv', 'n', 'tbb', 'tbq', 'i'])
        df['c'] = df['c'].astype(float)
        return df
    except:
        return None

@app.route('/')
def home():
    return f"""
    <html>
        <body style="background-color:black; color:white; font-family:sans-serif; text-align:center; padding-top:50px;">
            <h1>ESCORPIANO V1 - PANEL DE CONTROL</h1>
            <div style="border:2px solid green; display:inline-block; padding:20px; border-radius:15px;">
                <h2 style="color:lightgreen;">SALDO USDT: <span id="balance">{bot_data['balance']}</span></h2>
                <h3 style="color:orange;">PRECIO BTC: <span id="price">0</span></h3>
                <h3 style="color:cyan;">RSI REAL: <span id="rsi">50</span></h3>
                <hr>
                <h4 id="last_op" style="color:yellow;">{bot_data['last_op']}</h4>
            </div>
            <script>
                async function actualizar(){{
                    try {{
                        const res = await fetch('/status');
                        const d = await res.json();
                        document.getElementById('balance').innerText = d.balance.toLocaleString();
                        document.getElementById('rsi').innerText = d.rsi;
                        document.getElementById('price').innerText = d.price.toLocaleString();
                        document.getElementById('last_op').innerText = d.last_op;
                    }} catch(e){{}}
                }}
                setInterval(actualizar, 1000);
                actualizar();
            </script>
        </body>
    </html>
    """

@app.route('/status')
def status():
    df = get_data()
    price = 0
    rsi_val = 50
    
    if df is not None:
        price = df['c'].iloc[-1]
        rsi = ta.rsi(df['c'], length=14)
        rsi_val = round(rsi.iloc[-1], 2)
        
        # LÓGICA DE TRADING - RANGO AMPLIADO HASTA 85.000
        if 60000 < price < 85000:
            if rsi_val < 30 and bot_data['position'] == 0:
                bot_data['position'] = 1
                bot_data['entry_price'] = price
                bot_data['last_op'] = f"COMPRADO A {price} 🛒"
            elif rsi_val > 70 and bot_data['position'] == 1:
                bot_data['position'] = 0
                bot_data['last_op'] = f"VENDIDO A {price} 💰"
    
    return jsonify({{
        "balance": bot_data['balance'],
        "rsi": rsi_val,
        "price": price,
        "last_op": bot_data['last_op']
    }})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
