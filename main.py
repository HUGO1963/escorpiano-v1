import requests
from flask import Flask

app = Flask(__name__)

# --- CONFIGURACIÓN MINIMALISTA ---
CAPITAL = 100.0
MIN, MAX = 63000.0, 73000.0

@app.route('/')
def home():
    try:
        # Pedimos solo el precio, para no gastar datos
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=5)
        precio = res.json()['bitcoin']['usd']
        
        # Lógica del Rango
        activo = MIN <= precio <= MAX
        estado = "OPERANDO ✅" if activo else "FUERA DE RANGO ⚠️"
        color = "#00ff00" if activo else "#ff4444"
    except:
        precio, estado, color = 0, "ERROR RED", "orange"

    return f"""
    <body style="background:#131722; color:white; font-family:sans-serif; text-align:center; padding:20px;">
        <div style="border:2px solid {color}; border-radius:10px; display:inline-block; padding:20px; background:#1e222d;">
            <h1 style="margin:0;">🦂 ESCORPIÓN V1</h1>
            <h2 style="color:{color};">{estado}</h2>
            <hr style="border-color:#363c4e;">
            <p style="font-size:30px; margin:10px;">BTC: ${precio:,.2f}</p>
            <p>Rango: 63k - 73k | Capital: ${CAPITAL}</p>
        </div>
        <div style="margin-top:15px; height:350px;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE%3ABTCUSDT&interval=1&theme=dark&studies=RSI%40tv-basicstudies" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>setTimeout(() => {{ location.reload(); }}, 30000);</script>
    </body>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
