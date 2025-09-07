from flask import Flask, request, jsonify
import yfinance as yf
import json

app = Flask(__name__)

def normalize_exchange(exchange: str) -> str:
    """Normalize exchange names for Yahoo Finance compatibility."""
    if not exchange:
        return None
    exchange = exchange.upper()
    if exchange in ["NSE", "NS"]:
        return "NS"   # Yahoo Finance NSE suffix
    elif exchange in ["BSE", "BO"]:
        return "BO"   # Yahoo Finance BSE suffix
    return exchange   # fallback (e.g., NYSE, NASDAQ)


@app.route('/api/stock', methods=['GET'])
def get_stock_data():
    """
    Fetch stock or index data using yfinance and return relevant details.
    """
    try:
        symbol = request.args.get('symbol')
        exchange = request.args.get('exchange')

        if not symbol:
            return jsonify({'error': 'Missing required parameter "symbol"'}), 400
        if not exchange:
            return jsonify({'error': 'Missing required parameter "exchange"'}), 400

        exchange = normalize_exchange(exchange)

        # Special case: NIFTY 50
        if symbol.upper() == "NIFTY" and exchange == "NS":
            symbol = "^NSEI"
            stock = yf.Ticker(symbol)
        else:
            stock = yf.Ticker(f"{symbol}.{exchange}")

        data = stock.info
        if not data:
            return jsonify({'error': f"No data found for {symbol}.{exchange}"}), 404

        name = data.get("shortName", "N/A")
        price = data.get("currentPrice", "N/A")
        currency = data.get("currency", "N/A")
        previous_close = data.get("regularMarketPreviousClose", "N/A")

        if isinstance(price, (int, float)) and isinstance(previous_close, (int, float)):
            day_change = price - previous_close
            day_change_percent = (day_change / previous_close) * 100
        else:
            day_change = "N/A"
            day_change_percent = "N/A"

        response = {
            "stock_name": name,
            "current_price": str(price),
            "daily_change": f"{day_change:.2f}" if day_change != "N/A" else "N/A",
            "daily_change_percent": f"{day_change_percent:.2f}%" if day_change != "N/A" else "N/A",
            "currency": currency,
            "exchange": data.get("exchange", exchange),
            "data": data
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500


@app.route('/api/historical_nifty', methods=['GET'])
def get_historical_nifty():
    """Fetch historical Nifty 50 data."""
    try:
        period = request.args.get('period', '1mo')
        interval = request.args.get('interval', '1d')

        nifty = yf.Ticker("^NSEI")
        hist = nifty.history(period=period, interval=interval)

        if hist.empty:
            return jsonify({'error': 'Could not retrieve historical data'}), 404

        historical_data = hist.to_dict(orient='records')
        return jsonify(historical_data)

    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500


@app.route('/api/stock/news', methods=['GET'])
def get_stock_news():
    """Fetch the latest news for a given stock symbol."""
    try:
        symbol = request.args.get('symbol')
        if not symbol:
            return jsonify({"error": "Missing required parameter 'symbol'"}), 400

        ticker = yf.Ticker(symbol)
        news = ticker.news

        if not news or not isinstance(news, list):
            return jsonify({"message": f"No news found for ticker '{symbol}'"}), 404

        formatted_news = [
            {
                "title": item.get("title", "N/A"),
                "link": item.get("link", "N/A"),
                "publisher": item.get("publisher", "N/A"),
                "providerPublishTime": item.get("providerPublishTime", "N/A")
            }
            for item in news
        ]

        return jsonify({"symbol": symbol, "news": formatted_news})

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid response from Yahoo Finance: {str(e)}"}), 502
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
