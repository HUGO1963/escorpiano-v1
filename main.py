import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

bot_data = {'position': 0, 'last_op': "NINGUNA", 'balance': 100}

@app.route('/')
def home():
    # Página principal para ver que el bot está vivo
    return f"<h1>ESCORPIANO V1 - SALDO: ${bot_data['balance']}</h1>"

@app.route('/status')
def status():
    try:
        # Usamos la API de Binance pero a través de una URL alternativa
        # que suele saltar los bloqueos de Render
        url = "https://api1.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        res = requests.get(url, timeout=10).json()
        precio = float(res['price'])
        
        return jsonify({
            "status": "online",
            "price": precio,
            "last_op": bot_data['last_op']
        })
    except Exception as e:
        # Si falla Binance, intentamos con una de respaldo automáticamente
        try:
            url_backup = "https://api.coindesk.com/v1/bpi/currentprice.json"
            res_b = requests.get(url_backup, timeout=10).json()
            precio_b = res_b['bpi']['USD']['rate_float']
            return jsonify({"status": "online (backup)", "price": precio_b})
        except:
            return jsonify({"error": "Falla total de antenas", "detalle": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
