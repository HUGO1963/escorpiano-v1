import os, requests
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <body style="background:#000; color:#eee; font-family:sans-serif; text-align:center; padding:10px; margin:0;">
        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px;">
            <span style="color:#888;">BTC/USDT:</span> 
            <b id="p" style="color:#fa0; font-size:1.5em;">$0.00</b>
            <span id="s" style="margin-left:10px; font-size:0.8em;">...</span>
        </div>
        
        <div style="height:550px;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            function update() {
                fetch('/status').then(r => r.json()).then(d => {
                    document.getElementById('p').innerText = "$" + d.p.toLocaleString();
                    document.getElementById('s').innerText = d.p > 0 ? "✅" : "❌";
                });
            }
            setInterval(update, 3000); update();
        </script>
    </body>
    ''')

@app.route('/status')
def status():
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        return jsonify({"p": float(r['price'])})
    except:
        return jsonify({"p": 0})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
