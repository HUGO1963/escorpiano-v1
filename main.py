import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Datos del bot (Se reinician si Render se duerme)
bot_data = {'position': 0, 'last_op': "NINGUNA", 'balance': 100}

@app.route('/')
def home():
    return f"<h1>ESCORPIANO V1 - SISTEMA ACTIVO</h1><p>Saldo: {bot_data['balance']}</p>"

@app.route('/status')
def status():
    # Usamos Cryptocompare: es mas estable para servidores gratuitos
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
    
    try:
        res = requests.get(url, timeout=10)
        
        # Verificamos que la respuesta sea exitosa (200)
        if res.status_code == 200:
            datos = res.json()
            # Cryptocompare devuelve directamente {"USD": precio}
            precio = datos.get('USD')
            
            if precio:
                return jsonify({
                    "status": "online",
                    "price": precio,
                    "source": "Cryptocompare",
                    "last_op": bot_data['last_op'],
                    "balance": bot_data['balance']
                })
        
        return jsonify({"error": "Respuesta API invalida", "code": res.status_code})

    except Exception as e:
        return jsonify({"error": "Fallo de conexion total", "detalle": str(e)})

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=10000)
