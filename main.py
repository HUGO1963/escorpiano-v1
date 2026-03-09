import requests
from flask import Flask

app = Flask(__name__)

def obtener_precio():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        res = requests.get(url, timeout=10)
        data = res.json()
        return float(data['bitcoin']['usd'])
    except Exception as e:
        return "Error de Red"

@app.route('/')
def home():
    precio = obtener_precio()
    if precio != "Error de Red":
        return f"<h1>Escorpión V1</h1><p>BTC: ${precio:,.2f}</p><p>Estado: Operativo 🦂</p>"
    else:
        return "<h1>Escorpión V1</h1><p>Estado: Error de Conexión</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
