import requests
import time
from flask import Flask, jsonify, render_template_string
from threading import Thread

app = Flask(__name__)

# --- CONFIGURACIÓN DEL ESCORPIANO ---
PRECIO_MIN = 62000
PRECIO_MAX = 72000
bot_data = {'position': 0, 'last_op': "ESPERANDO DATOS", 'balance': 697, 'precios': [], 'rsi': 0}

def obtener_precio():
    try:
        # Usamos CoinGecko como Plan B infalible
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        res = requests.get(url, timeout=10)
        return float(res.json()['bitcoin']['usd'])
    except:
        return "Error de Red"

def actualizar_bot():
    while True:
        precio = obtener_precio()
        if precio and precio != "Error de Red":
            bot_data['precios'].append(precio)
            if len(bot_data['precios']) > 50:
                bot_data['precios'].pop(0)
            # Aquí iría tu lógica de RSI y trading...
        time.sleep(60) # Actualiza cada minuto

@app.route('/')
def home():
    # Aquí va tu diseño verde y negro que ya tenés
    return "Escorpiano V1 - BTC: $" + str(obtener_precio_binance())

@app.route('/data')
def data():
    return jsonify(bot_data)

if __name__ == "__main__":
    Thread(target=actualizar_bot).start()
    app.run(host='0.0.0.0', port=10000)
