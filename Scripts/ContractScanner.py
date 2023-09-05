import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ETHEREUM_SCAN_API = "https://api.etherscan.io/api"
API_KEY = "7UI59WUIDUBUDJRQDNUG45WQ5CY4R8SWX2"

def check_liquidity_pool_creation(contract_address):
    # ... existing code ...

    # Example code to check for specific logs
    payload = {
        "module": "logs",
        "action": "getLogs",
        "fromBlock": "0",
        "toBlock": "latest",
        "address": contract_address,
        # Include specific topic for the event or method indicative of liquidity pool creation
        "topic0": "TOPIC_SIGNATURE_HERE",
        "apikey": API_KEY
    }

    response = requests.get(ETHEREUM_SCAN_API, params=payload)
    if response.status_code == 200:
        logs = response.json().get('result', [])
        if logs:
            return "Liquidity Pool"

    return "Unknown"


def get_contracts_by_wallet(wallet_address):
    contract_details = []

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
            if tx['to'] == '':
                contract_address = tx['contractAddress']
                liquidity_status = check_liquidity_pool_creation(contract_address)
                contract_details.append({
                    'contractAddress': contract_address,
                    'liquidityStatus': liquidity_status
                })
                
    return contract_details

@app.route('/get_contracts', methods=['POST'])
def get_contracts():
    wallet_address = request.json.get('wallet_address')
    if not wallet_address:
        return jsonify({'error': 'Missing wallet_address parameter'}), 400

    contract_details = get_contracts_by_wallet(wallet_address)
    return jsonify({'contracts': contract_details}) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
