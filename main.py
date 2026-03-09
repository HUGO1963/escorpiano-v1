from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Escorpión Pro V2</title>
            <style>
                body { background-color: #131722; color: white; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
                h1 { color: #2962ff; }
                .container { max-width: 1000px; margin: auto; background: #1e222d; padding: 20px; border-radius: 10px; border: 1px solid #363c4e; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🦂 Escorpión Pro V2</h1>
                <p>BTC/USD - Gráfica, RSI y Análisis Técnico</p>
                
                <div class="tradingview-widget-container" style="height:500px;width:100%">
                    <div id="tradingview_btc"></div>
                    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                    <script type="text/javascript">
                    new TradingView.widget({
                      "autosize": true,
                      "symbol": "BINANCE:BTCUSDT",
                      "interval": "60",
                      "timezone": "Etc/UTC",
                      "theme": "dark",
                      "style": "1",
                      "locale": "es",
                      "toolbar_bg": "#f1f3f6",
                      "enable_publishing": false,
                      "hide_side_toolbar": false,
                      "allow_symbol_change": true,
                      "details": true,
                      "hotlist": true,
                      "calendar": true,
                      "container_id": "tradingview_btc"
                    });
                    </script>
                </div>
                <div style="margin-top: 20px;">
                    <p><i>El RSI y las ganancias se calculan automáticamente en el panel de la derecha de la gráfica.</i></p>
                </div>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
