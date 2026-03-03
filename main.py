import os
import requests
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# --- CONFIGURACIÓN OPTIMIZADA ---
bot = {
    "ars": 10000.0,
    "btc": 0.0,
    "estado": "BUSCANDO COMPRA",
    "rango_min": 40000.0,
    "rango_max": 100000.0,  # Subimos el techo a 100k
    "pausado_manual": False,
    "historial": []
}

def obtener_datos():
    try:
        r = requests.get("https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=30", timeout=5).json()
        precios = [float(v[4]) for v in r]
        p_act = precios[-1]
        subidas = [max(precios[i] - precios[i-1], 0) for i in range(1, len(precios))]
        bajadas = [abs(min(precios[i] - precios[i-1], 0)) for i in range(1, len(precios))]
        avg_s = sum(subidas[-14:]) / 14
        avg_b = sum(bajadas[-14:]) / 14
        rs = avg_s / avg_b if avg_b != 0 else 1
        rsi = 100 - (100 / (1 + rs))
        return p_act, rsi
    except:
        return 0.0, 50.0

@app.route('/')
def home():
    return render_template_string("""
    <body style="background:#050505; color:#eee; font-family:sans-serif; margin:0; padding:10px;">
        <div style="max-width:900px; margin:auto; border:2px solid #a0f; border-radius:15px; background:#111; overflow:hidden; box-shadow: 0 0 25px #a0f7;">
            <div style="background:#a0f; padding:15px; text-align:center; border-bottom:2px solid #333; position:relative;">
                <h1 style="margin:0; color:white; letter-spacing:3px; text-shadow: 2px 2px #000;">🦂 ESCORPIANO V1 PRO</h1>
                <button onclick="panico()" style="position:absolute; right:15px; top:15px; background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">⚠️ SALIR POR LAS DUDAS</button>
            </div>
            
            <div style="display:flex; justify-content:space-around; padding:20px; background:#1a1a1a;">
                <div style="text-align:center; flex:1; border-right:1px solid #333;">
                    <small style="color:#888;">PRECIO ACTUAL BTC</small><br>
                    <span id="p" style="color:#fa0; font-size:2.2em; font-weight:bold;">$0</span>
                </div>
                <div style="text-align:center; flex:1;">
                    <small style="color:#888;">RANGO OPERATIVO</small><br>
                    <span style="color:#aaa; font-size:1.2em;">Min: <b id="rmin">0</b> | Max: <b id="rmax">0</b></span>
                </div>
            </div>

            <div style="padding:20px; text-align:center; background:#001a00; border-top:1px solid #333; border-bottom:1px solid #333;">
                <small style="color:#aaa;">BILLETERA ESTIMADA (ARS)</small><br>
                <span id="ars" style="font-size:3em; font-weight:bold; color:#4f4;">$10,000</span>
                <p id="est" style="margin:10px 0; font-size:1.3em; font-weight:bold; text-transform:uppercase;"></p>
            </div>

            <div style="height:400px; background:#000;">
                <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
            </div>

            <div style="padding:20px; background:#111;">
                <h3 style="margin:0 0 10px 0; color:#a0f; border-bottom:1px solid #a0f4;">📜 REGISTRO OPERACIONES</h3>
                <div id="hist" style="font-family:monospace; font-size:1.1em; height:150px; overflow-y:auto; color:#ccc; background:#050505; padding:15px; border-radius:10px; border:1px solid #222;"></div>
            </div>
        </div>

        <script>
            function actualizar(){
                fetch('/api/status').then(res => res.json()).then(d => {
                    document.getElementById('p').innerText = "$" + d.precio.toLocaleString();
                    document.getElementById('rmin').innerText = "$" + d.r_min.toLocaleString();
                    document.getElementById('rmax').innerText = "$" + d.r_max.toLocaleString();
                    document.getElementById('ars').innerText = "$" + d.ars.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('est').innerText = d.estado;
                    document.getElementById('est').style.color = d.fuera ? "#ff4444" : "#44ff44";
                    let h = ""; 
                    d.hist.slice().reverse().forEach(t => h += "<div style='border-bottom:1px solid #222; padding:8px;'>"+t+"</div>");
                    document.getElementById('hist').innerHTML = h || "Radar activado...";
                });
            }
            function panico(){
                if(confirm("¿Seguro que querés vender todo y pausar el bot?")){
                    fetch('/api/panico', {method:'POST'}).then(() => actualizar());
                }
            }
            setInterval(actualizar, 2000);
            actualizar();
        </script>
    </body>
    """)

@app.route('/api/status')
def status():
    p, rsi = obtener_datos()
    fuera = p < bot["rango_min"] or p > bot["rango_max"]
    
    if not bot["pausado_manual"]:
        if not fuera:
            if bot["estado"] == "BUSCANDO COMPRA" and rsi <= 30:
                bot["btc"] = bot["ars"] / (p * 1200)
                bot["ars"] = 0
                bot["estado"] = "ESTADO: COMPRADO ✅"
                bot["historial"].append(f"🟢 COMPRÓ a ${p}")
            elif bot["estado"] == "ESTADO: COMPRADO ✅" and rsi >= 70:
                bot["ars"] = bot["btc"] * (p * 1200)
                bot["btc"] = 0
                bot["estado"] = "BUSCANDO COMPRA"
                bot["historial"].append(f"🔴 VENDIÓ a ${p} | Saldo: ${bot['ars']:.2f}")
        else:
            bot["estado"] = "PAUSADO (FUERA DE RANGO)"
    else:
        bot["estado"] = "DETENIDO POR EL USUARIO 🛑"

    return jsonify({
        "precio": p, "ars": bot["ars"] if bot["ars"] > 0 else (bot["btc"] * p * 1200), 
        "estado": bot["estado"], "fuera": fuera, "hist": bot["historial"],
        "r_min": bot["rango_min"], "r_max": bot["rango_max"]
    })

@app.route('/api/panico', methods=['POST'])
def panico():
    p, _ = obtener_datos()
    if bot["btc"] > 0:
        bot["ars"] = bot["btc"] * (p * 1200)
        bot["btc"] = 0
        bot["historial"].append(f"⚠️ PÁNICO: Venta manual a ${p}")
    bot["pausado_manual"] = True
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
