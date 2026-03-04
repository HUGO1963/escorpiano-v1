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
        # Usamos una URL de CoinGecko que devuelve el dato mas simple
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        res_json = response.json()
        
        # Verificamos si el dato existe antes de mostrarlo
        if 'bitcoin' in res_json:
            precio = res_json['bitcoin']['usd']
            return jsonify({
                "status": "online",
                "price": precio,
                "last_op": bot_data['last_op']
            })
        else:
            return jsonify({"error": "No se encontro el precio", "respuesta_api": res_json})
            
    except Exception as e:
        return jsonify({"error": "Fallo la conexion", "detalle": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
