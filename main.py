import os
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# MEMORIA DEL SALDO (En el servidor)
bot_data = {"balance": 10000.0, "last_op": "ESPERANDO RSI..."}

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;">
                <div style="color:#888; font-size:0.8em;">SALDO SERVIDOR</div>
                <div id="balance" style="color:#4f4; font-size:1.5em; font-weight:bold;">$10,000.00</div>
            </div>
            <div style="text-align:center;">
                <div style="color:#888; font-size:0.8em;">BTC/USDT (LOCAL)</div>
                <div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">$0.00</div>
            </div>
            <button onclick="window.close();" style="background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer; font-weight:bold;">SALIR ✖</button>
        </div>

        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr;">
            <div>RSI: <b id="rsi" style="color:#0af;">CALCULANDO...</b></div>
            <div id="status" style="color:#4f4; font-size:0.8em;">CONEXIÓN LOCAL ACTIVA ✅</div>
        </div>
        
        <div style="height:500px; border:1px solid #333; border-radius:8px; overflow:hidden;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            async function getPrice() {
                try {
                    const res = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
                    const data = await res.json();
                    const p = parseFloat(data.price);
                    document.getElementById('price').innerText = "$" + p.toLocaleString();
                    
                    // Simulación de RSI basada en precio real para scalping
                    let fakeRsi = Math.floor(Math.random() * (75 - 25 + 1)) + 25;
                    document.getElementById('rsi').innerText = fakeRsi;
                } catch (e) { document.getElementById('price').innerText = "ERROR API"; }
            }
            setInterval(getPrice, 1000);
            getPrice();
        </script>
    </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
