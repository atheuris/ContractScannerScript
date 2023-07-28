import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ETHEREUM_SCAN_API = "https://api.etherscan.io/api"
API_KEY = "7UI59WUIDUBUDJRQDNUG45WQ5CY4R8SWX2"

def get_contracts_by_wallet(wallet_address):
    contract_addresses = []

    # API params
    payload = {
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": API_KEY
    }

    # Send request to Etherscan API
    response = requests.get(ETHEREUM_SCAN_API, params=payload)

    if response.status_code == 200:
        transactions = response.json().get('result', [])
        
        for tx in transactions:
            # Check if the transaction is a contract creation
            if tx['to'] == '':
                contract_addresses.append(tx['contractAddress'])
                
    return contract_addresses

@app.route('/get_contracts', methods=['POST'])
def get_contracts():
    wallet_address = request.json.get('wallet_address')
    if not wallet_address:
        return jsonify({'error': 'Missing wallet_address parameter'}), 400

    contract_addresses = get_contracts_by_wallet(wallet_address)
    return jsonify({'contract_addresses': contract_addresses}) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
