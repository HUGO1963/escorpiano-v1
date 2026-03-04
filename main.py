import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

bot_data = {'position': 0, 'last_op': "NINGUNA", 'balance': 100}

@app.route('/')
def home():
    return f"<h1>ESCORPIANO V1 - SALDO: ${bot_data['balance']}</h1>"

@app.route('/status')
def status():
    try:
        # Usamos CoinDesk que es libre y no tiene limites estrictos
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        res = requests.get(url).json()
        precio = res['bpi']['USD']['rate_float']
        
        return jsonify({
            "status": "online",
            "price": precio,
            "last_op": bot_data['last_op']
        })
    except Exception as e:
        return jsonify({"error": "Fallo la antena de precio", "detalle": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
