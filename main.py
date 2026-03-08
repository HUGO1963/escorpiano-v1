import requests
import time
from flask import Flask, jsonify, render_template_string
from threading import Thread

app = Flask(__name__)

# --- CONFIGURACIÓN DEL ESCORPIANO ---
PRECIO_MIN = 62000
PRECIO_MAX = 72000
bot_data = {'position': 0, 'last_op': "ESPERANDO DATOS", 'balance': 697, 'precios': [], 'rsi': 0}

def obtener_precio_binance():
    # Probamos con dos caminos distintos por si uno está bloqueado
    urls = [
        "https://api.binance.com/api/3/ticker/price?symbol=BTCUSDT",
        "https://api1.binance.com/api/3/ticker/price?symbol=BTCUSDT"
    ]
    for url in urls:
        try:
            res = requests.get(url, timeout=5)
            return float(res.json()['price'])
        except:
            continue
    return "Error de Conexión"

def actualizar_bot():
    while True:
        precio = obtener_precio_binance()
        if precio:
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
