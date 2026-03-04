import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# MEMORIA DEL BOT
bot_data = {"balance": 10192.28, "position": 0, "last_op": "SISTEMA ACTIVO 🟢"}

def rsi_simple(precios):
    if len(precios) < 14: return 50
    subidas = [max(0, precios[i] - precios[i-1]) for i in range(1, len(precios))]
    bajadas = [max(0, precios[i-1] - precios[i]) for i in range(1, len(precios))]
    prom_s = sum(subidas[-14:]) / 14
    prom_b = sum(bajadas[-14:]) / 14
    if prom_b == 0: return 100
    return round(100 - (100 / (1 + (prom_s / prom_b))), 2)

@app.route('/')
def home():
    return f"<h1>BOT ACTIVO - SALDO: ${bot_data['balance']}</h1>"

@app.route('/status')
def status():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
        res = requests.get(url).json()
        precios = [float(f[4]) for f in res]
        precio = precios[-1]
        rsi = rsi_simple(precios)
        
        # RANGO AMPLIADO A 85000
        if 60000 < precio < 85000:
            if rsi < 30 and bot_data['position'] == 0:
                bot_data['position'] = 1
                bot_data['last_op'] = f"COMPRADO A {precio}"
            elif rsi > 70 and bot_data['position'] == 1:
                bot_data['position'] = 0
                bot_data['last_op'] = f"VENDIDO A {precio}"
        
        return jsonify({"price": precio, "rsi": rsi, "last_op": bot_data['last_op']})
    except:
        return jsonify({"error": "Error de red"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
