import requests
from flask import Flask, jsonify

app = Flask(__name__)

# --- CONFIGURACIÓN ---
CAPITAL_INICIAL = 100.0
PRECIO_ENTRADA = 64500.0 
R_MIN, R_MAX = 63000.0, 73000.0

def traer_datos():
    try:
        # Antena Coinbase ultra-rápida
        r = requests.get("https://api.coinbase.com/v2/prices/BTC-USD/spot", timeout=2)
        p = float(r.json()['data']['amount'])
        gan = ((p - PRECIO_ENTRADA) / PRECIO_ENTRADA) * CAPITAL_INICIAL
        cap = CAPITAL_INICIAL + gan
        est = "OPERANDO ✅" if R_MIN <= p <= R_MAX else "SISTEMA APAGADO ⚠️"
        col = "#00ff00" if R_MIN <= p <= R_MAX else "#ff4444"
        return {"p": f"{p:,.2f}", "cap": f"{cap:,.2f}", "gan": f"{gan:,.2f}", "est": est, "col": col}
    except:
        return {"p": "---", "cap": "---", "gan": "---", "est": "RECONECTANDO...", "col": "orange"}

@app.route('/datos')
def datos():
    return jsonify(traer_datos())

@app.route('/')
def home():
    d = traer_datos()
    return f"""
    <body style="background:#131722; color:white; font-family:sans-serif; text-align:center; padding:10px;">
        <div id="borde" style="border:4px solid {d['col']}; border-radius:15px; display:inline-block; padding:15px; background:#1e222d; min-width:320px;">
            <h1 style="margin:0; font-size:22px;">🦂 ESCORPIÓN V1</h1>
            <h2 id="estado" style="color:{d['col']}; margin:5px; font-size:16px;">{d['est']}</h2>
            <hr style="border-color:#363c4e;">
            <div style="margin:10px 0;">
                <span style="font-size:14px; color:#848e9c;">PRECIO BTC ACTUAL</span>
                <div id="precio" style="font-size:40px; font-weight:bold;">${d['p']}</div>
            </div>
            <div style="background:#2a2e39; padding:15px; border-radius:12px; border:1px solid #444;">
                <span style="font-size:14px; color:#848e9c;">CAPITAL TOTAL</span>
                <div id="capital" style="font-size:28px; font-weight:bold;">${d['cap']}</div>
                <div id="ganancia" style="font-size:16px;">Ganancia: ${d['gan']}</div>
            </div>
        </div>
        <div style="margin-top:15px; height:450px;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE%3ABTCUSDT&interval=1&theme=dark&studies=RSI%40tv-basicstudies" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <script>
            async function actualizar() {{
                try {{
                    const res = await fetch('/datos');
                    const d = await res.json();
                    document.getElementById('precio').innerText = '$' + d.p;
                    document.getElementById('capital').innerText = '$' + d.cap;
                    document.getElementById('ganancia').innerText = 'Ganancia: $' + d.gan;
                    document.getElementById('estado').innerText = d.est;
                    document.getElementById('estado').style.color = d.col;
                    document.getElementById('borde').style.borderColor = d.col;
                }} catch (e) {{ console.log("Error de lectura"); }}
            }}
            setInterval(actualizar, 1000); // ACTUALIZACIÓN CADA 1 SEGUNDO
        </script>
    </body>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
