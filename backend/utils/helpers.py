def format_wallet_address(address):
    return address.lower()

def calculate_transaction_fee(gas_price, gas_used):
    return gas_price * gas_used

def is_valid_wallet_address(address):
    return len(address) == 42 and address.startswith('0x')

def parse_transaction_data(txn_data):
    return {
        'from': txn_data.get('from'),
        'to': txn_data.get('to'),
        'value': txn_data.get('value'),
        'timestamp': txn_data.get('timestamp'),
        'hash': txn_data.get('hash')
    }

def extract_relevant_features(wallet_data):
    return {
        'transaction_count': len(wallet_data.get('transactions', [])),
        'total_value_sent': sum(txn['value'] for txn in wallet_data.get('transactions', [])),
        'unique_receivers': len(set(txn['to'] for txn in wallet_data.get('transactions', [])))
    }