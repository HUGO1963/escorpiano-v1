import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Datos del bot
bot_data = {'position': 0, 'last_op': "NINGUNA", 'balance': 100}

def rsi_simple(precios):
    if len(precios) < 14: return 50
    subidas = [precios[i] - precios[i-1] for i in range(1, len(precios)) if precios[i] > precios[i-1]]
    bajadas = [precios[i-1] - precios[i] for i in range(1, len(precios)) if precios[i] < precios[i-1]]
    prom_s = sum(subidas) / 14 if subidas else 0
    prom_b = sum(bajadas) / 14 if bajadas else 0.001
    return round(100 - (100 / (1 + (prom_s / prom_b))), 2)

@app.route('/')
def home():
    return f"<h1>BOT ESCORPIANO V1 - SALDO: ${bot_data['balance']}</h1>"

@app.route('/status')
def status():
    try:
        url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers).json()
        if isinstance(res, list) and len(res) > 0:
            precios = [float(f[4]) for f in res]
        else:
            return jsonify({"error": "Binance no respondio bien", "respuesta": str(res)})
        precio = precios[-1]
        rsi = rsi_simple(precios)
        
        # Lógica de trading
        if 60000 < precio < 95000:
            if rsi < 30 and bot_data['position'] == 0:
                bot_data['position'] = 1
                bot_data['last_op'] = f"COMPRADO A {precio}"
            elif rsi > 70 and bot_data['position'] == 1:
                bot_data['position'] = 0
                bot_data['last_op'] = f"VENDIDO A {precio}"
                
        return jsonify({"price": precio, "rsi": rsi, "last_op": bot_data['last_op']})
    except Exception as e:
        return jsonify({"error": "Error de conexion", "detalle": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
