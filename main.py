import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;">
                <div style="color:#888; font-size:0.8em;">SALDO VIRTUAL</div>
                <div id="balance" style="color:#4f4; font-size:1.5em; font-weight:bold;">$10,000.00</div>
            </div>
            <div style="text-align:center;">
                <div style="color:#888; font-size:0.8em;">BTC/USDT</div>
                <div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">0.00</div>
            </div>
            <button onclick="window.close();" style="background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">SALIR ✖</button>
        </div>

        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px;">
            <div><span style="color:#888;">RSI:</span> <b id="rsi_val">--</b></div>
            <div><span style="color:#888;">RANGO:</span> <b style="color:#0af;">63k-73k</b></div>
            <div><span style="color:#888;">ESTADO:</span> <b id="bot_status" style="color:#aaa;">ESPERANDO...</b></div>
        </div>
        
        <div style="height:500px; border-radius:8px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            let balance = 10000;
            let position = 0; // 0 = nada, 1 = comprado

            async function botLogic() {
                try {
                    // Pedimos precio y RSI (usando una API que calcula RSI para no complicar el server)
                    const res = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
                    const data = await res.json();
                    const p = parseFloat(data.price);
                    
                    // Simulación de RSI (para scalping de 1s, el RSI fluctúa rápido)
                    // En un bot real, acá conectaríamos a un indicador técnico
                    let rsi = Math.floor(Math.random() * (80 - 20 + 1)) + 20; 

                    document.getElementById('price').innerText = "$" + p.toLocaleString();
                    document.getElementById('rsi_val').innerText = rsi;

                    // LÓGICA AUTOMÁTICA
                    if (p >= 63000 && p <= 73000) {
                        if (rsi <= 30 && position === 0) {
                            position = 1;
                            document.getElementById('bot_status').innerText = "COMPRADO ✅";
                            document.getElementById('bot_status').style.color = "#4f4";
                        } else if (rsi >= 70 && position === 1) {
                            position = 0;
                            balance += 50; // Simulación de ganancia fija
                            document.getElementById('balance').innerText = "$" + balance.toLocaleString();
                            document.getElementById('bot_status').innerText = "VENDIDO (GANANCIA) 💰";
                            document.getElementById('bot_status').style.color = "#fa0";
                        } else if (position === 0) {
                            document.getElementById('bot_status').innerText = "BUSCANDO ENTRADA...";
                        }
                    } else {
                        document.getElementById('bot_status').innerText = "FUERA DE RANGO ⚠️";
                        document.getElementById('bot_status').style.color = "#f44";
                    }
                } catch (e) { console.log("Error de conexión"); }
            }

            setInterval(botLogic, 1000);
        </script>
    </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
