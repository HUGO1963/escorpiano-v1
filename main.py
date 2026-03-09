import requests
from flask import Flask

app = Flask(__name__)

# --- CONFIGURACIÓN DEL BOT ---
CAPITAL_INICIAL = 100.0
PRECIO_COMPRA = 64500.0  # El precio base para calcular tu ganancia
MIN, MAX = 63000.0, 73000.0

def traer_datos_bot():
    try:
        # Antena Coinbase (más estable para Render)
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=10)
        p_actual = float(r.json()['data']['amount'])
        
        # Cálculo de Ganancia y Capital Total
        variacion = (p_actual - PRECIO_COMPRA) / PRECIO_COMPRA
        ganancia_usd = CAPITAL_INICIAL * variacion
        capital_total = CAPITAL_INICIAL + ganancia_usd
        
        # Estado del Rango
        activo = MIN <= p_actual <= MAX
        estado = "OPERANDO ✅" if activo else "FUERA DE RANGO ⚠️"
        color = "#00ff00" if activo else "#ff4444"
        
        return p_actual, capital_total, ganancia_usd, estado, color
    except:
        return 0.0, 100.0, 0.0, "RECONECTANDO...", "orange"

@app.route('/')
def home():
    p, cap, gan, est, col = traer_datos_bot()
    color_gan = "#00ff00" if gan >= 0 else "#ff4444"
    
    return f"""
    <body style="background:#131722; color:white; font-family:sans-serif; text-align:center; padding:15px;">
        <div style="border:3px solid {col}; border-radius:15px; display:inline-block; padding:15px; background:#1e222d; min-width:300px;">
            <h1 style="margin:0; font-size:20px;">🦂 ESCORPIÓN V1</h1>
            <h2 style="color:{col}; margin:5px; font-size:18px;">{est}</h2>
            <hr style="border-color:#363c4e;">
            <p style="font-size:32px; font-weight:bold; margin:5px;">BTC: ${p:,.2f}</p>
            
            <div style="background:#2a2e39; padding:10px; border-radius:10px; margin-top:10px;">
                <p style="margin:5px;">Capital Total: <b>${cap:,.2f}</b></p>
                <p style="margin:5px; color:{color_gan};">Ganancia: <b>${gan:,.2f}</b></p>
            </div>
            <p style="font-size:12px; color:#848e9c;">Rango: 63k - 73k</p>
        </div>

        <div style="margin-top:15px; height:400px; width:100%;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE%3ABTCUSDT&interval=1&theme=dark&studies=RSI%40tv-basicstudies" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        
        <script>setTimeout(() => {{ location.reload(); }}, 30000);</script>
    </body>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
