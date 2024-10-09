import requests
import time

def get_latest_transaction(address):
    url = f"https://blockstream.info/api/address/{address}/txs"
    response = requests.get(url)
    if response.status_code == 200:
        transactions = response.json()
        if len(transactions) > 0:
            return transactions[0]
    return None

def check_confirmations(txid):
    url = f"https://blockstream.info/api/tx/{txid}"
    response = requests.get(url)
    if response.status_code == 200:
        tx_data = response.json()
        block_height = tx_data.get("status", {}).get("block_height", None)
        confirmations = tx_data.get("status", {}).get("confirmations", 0)
        return block_height is not None, confirmations
    return False, 0

def monitor_address(address, custom_msg):
    print(f"Monitoring Bitcoin address: {address}")
    while True:
        latest_transaction = get_latest_transaction(address)
        if latest_transaction:
            txid = latest_transaction.get("txid")
            print(f"Transaction detected: {txid}")
            
            while True:
                confirmed, confirmations = check_confirmations(txid)
                if confirmed and confirmations >= 10:
                    print(custom_msg)
                    return
                print(f"Confirmations: {confirmations} (waiting for 10)")
                time.sleep(60)
        else:
            print("No transactions found. Retrying in 60 seconds...")
        time.sleep(60)

bitcoin_address = ""
custom_message = "Your transaction is fully confirmed!"
monitor_address(bitcoin_address, custom_message)
