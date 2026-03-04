import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="display:flex; justify-content: space-between; align-items: center; background:#111; padding:10px 20px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="text-align:left;">
                <div style="color:#888; font-size:0.8em;">BTC/USDT (1s)</div>
                <div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">Cargando...</div>
            </div>
            
            <button onclick="window.close(); window.location.href='about:blank';" 
                style="background:#f44; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer;">
                SALIR ✖
            </button>
        </div>

        <div id="status" style="color:#4f4; font-size:0.7em; margin-bottom:10px;">VELOCIDAD: 1 SEGUNDO ✅</div>
        
        <div style="height:550px; border-radius:8px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            function getPrice() {
                fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
                    .then(r => r.json())
                    .then(data => {
                        const p = parseFloat(data.price);
                        document.getElementById('price').innerText = "$" + p.toLocaleString(undefined, {minimumFractionDigits: 2});
                    })
                    .catch(() => {
                        document.getElementById('price').innerText = "ERROR";
                    });
            }
            // Cambiado a 1000ms (1 segundo)
            setInterval(getPrice, 1000); 
            getPrice();
        </script>
    </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
