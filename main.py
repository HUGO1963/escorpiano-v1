import os
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# MEMORIA DEL BOT EN EL SERVIDOR
bot_data = {
    "balance": 10000.0,
    "position": 0,  # 0: nada, 1: comprado
    "entry_price": 0.0,
    "last_op": "ESPERANDO OPORTUNIDAD..."
}

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
                <div style="color:#888; font-size:0.8em;">BTC/USDT</div>
                <div id="price" style="color:#fa0; font-size:1.8em; font-weight:bold;">$0.00</div>
            </div>
            <button onclick="window.close();" style="background:#f44; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">SALIR ✖</button>
        </div>

        <div style="background:#111; padding:10px; border:1px solid #333; margin-bottom:10px; border-radius:8px; display:grid; grid-template-columns: 1fr 1fr;">
            <div>RSI: <b id="rsi" style="color:#0af;">--</b></div>
            <div id="last_op" style="font-size:0.8em; color:#aaa;">ESPERANDO...</div>
        </div>
        
        <div style="height:500px; border:1px solid #333; border-radius:8px; overflow:hidden;">
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=1&theme=dark" width="100%" height="100%" frameborder="0"></iframe>
        </div>

        <script>
            let local_position = 0;

            async function loop() {
                try {
                    // 1. Obtener precio real desde tu navegador
                    const res = await fetch('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT');
                    const data = await res.json();
                    const p = parseFloat(data.price);
                    document.getElementById('price').innerText = "$" + p.toLocaleString();

                    // 2. Simular RSI y avisar al servidor para que procese
                    let rsi = Math.floor(Math.random() * (80 - 20 + 1)) + 20;
                    document.getElementById('rsi').innerText = rsi;

                    // 3. Enviar datos al servidor para que el BOT ejecute
                    const response = await fetch('/trade', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({price: p, rsi: rsi})
                    });
                    const bot = await response.json();
                    
                    // 4. Actualizar visualmente el saldo y operaciones
                    document.getElementById('balance').innerText = "$" + bot.balance.toLocaleString(undefined, {minimumFractionDigits: 2});
                    document.getElementById('last_op').innerText = bot.last_op;
                    if(bot.position == 1) document.getElementById('last_op').style.color = "#4f4";
                    else document.getElementById('last_op').style.color = "#aaa";

                } catch (e) { console.log("Error en loop"); }
            }
            setInterval(loop, 2000); // Cada 2 segundos para no saturar
        </script>
    </body>
    ''')

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    price = data['price']
    rsi = data['rsi']
    
    # LÓGICA DE COMPRA/VENTA (63k - 73k)
    if 63000 <= price <= 73000:
        if rsi <= 30 and bot_data["position"] == 0:
            bot_data["position"] = 1
            bot_data["entry_price"] = price
            bot_data["last_op"] = f"COMPRADO A ${price}"
        elif rsi >= 70 and bot_data["position"] == 1:
            profit = price - bot_data["entry_price"]
            bot_data["balance"] += profit
            bot_data["position"] = 0
            bot_data["last_op"] = f"VENDIDO! GANANCIA: ${profit:.2f}"
    else:
        bot_data["last_op"] = "FUERA DE RANGO (63k-73k)"

    return jsonify(bot_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
