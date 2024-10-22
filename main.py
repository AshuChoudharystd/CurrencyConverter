from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Function to get the exchange rate from the API
def get_exchange_rate(from_currency, to_currency):
    api_key = "9d4a0b086fe881fad6dfd2af"  # Replace with your actual API key
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['result'] == 'success':
        return data['conversion_rate']
    else:
        return None

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    exchange_rate = get_exchange_rate(from_currency, to_currency)

    if exchange_rate:
        return amount * exchange_rate
    else:
        return None

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    amount = data.get('amount')
    from_currency = data.get('from_currency').upper()
    to_currency = data.get('to_currency').upper()

    if not amount or not from_currency or not to_currency:
        return jsonify({"error": "Missing required parameters"}), 400

    result = convert_currency(amount, from_currency, to_currency)

    if result:
        return jsonify({
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "converted_amount": round(result, 2)
        })
    else:
        return jsonify({"error": "Conversion failed. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
