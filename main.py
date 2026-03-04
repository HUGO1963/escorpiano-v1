import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="background:#111; padding:15px; border:1px solid #333; margin-bottom:10px; border-radius:8px;">
            <div style="color:#888; font-size:0.9em;">PRECIO BTC (DIRECTO BINANCE)</div>
            <div id="price" style="color:#fa0; font-size:2.5em; font-weight:bold; margin:5px 0;">Cargando...</div>
            <div id="status" style="color:#4f4; font-size:0.8em;">CONECTANDO DESDE TU NAVEGADOR...</div>
        </div>
        
        <div style="height:550px; border-radius:8px; overflow:hidden; border:1px solid #333;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            // Este script conecta directamente desde TU PC a Binance, saltando el bloqueo de Render
            function getPrice() {
                fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
                    .then(response => response.json())
                    .then(data => {
                        const p = parseFloat(data.price);
                        document.getElementById('price').innerText = "$" + p.toLocaleString(undefined, {minimumFractionDigits: 2});
                        document.getElementById('status').innerText = "CONEXIÓN LOCAL EXITOSA ✅";
                    })
                    .catch(err => {
                        document.getElementById('status').innerText = "ERROR DE SEÑAL LOCAL ❌";
                        document.getElementById('price').innerText = "$0,00";
                    });
            }
            setInterval(getPrice, 3000); 
            getPrice();
        </script>
    </body>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
