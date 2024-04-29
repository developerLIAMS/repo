import streamlit as st
import requests

st.set_page_config(page_title="Crypto Balance Tracker", layout="wide")

# Función para obtener el saldo de BTC
def get_btc_balance():
    wallet_addresses = [
        "bc1qzkncn5wmxwkxzjxzk3drnjpwc9p5rx8dgkw8z9",
        "bc1qs3j6ggfjjhhsduv4zdupdgvwd2gsanjp2qcqjw",
        "bc1qwwjawfzawapd0udncqxvpfyuq6cw9je036rpms",
    ]
    total_balance = 0
    st.write("Escaneando direcciones BTC:")
    for address in wallet_addresses:
        st.write(f"  - {address}")
        url = f"https://blockchain.info/balance?active={address}"
        response = requests.get(url)
        response_data = response.json()
        balance = response_data[address]['final_balance'] / 100000000
        total_balance += balance
    escrow_amount = total_balance - 2
    return total_balance, escrow_amount

# Función para obtener el saldo de ETH, USDT y USDC ERC20
def get_eth_usdt_usdc_balances(addresses, api_key):
    usdt_contract_address = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    usdc_contract_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    total_eth_balance = 0
    total_usdt_balance = 0
    total_usdc_balance = 0
    st.write("Escaneando direcciones ETH, USDT, USDC:")
    for address in addresses:
        st.write(f"  - {address}")
        url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        eth_balance = int(response.json()['result']) / 1e18
        total_eth_balance += eth_balance

        url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={usdt_contract_address}&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        usdt_balance = int(response.json()['result']) / 1e6
        total_usdt_balance += usdt_balance

        url = f"https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={usdc_contract_address}&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        usdc_balance = int(response.json()['result']) / 1e6
        total_usdc_balance += usdc_balance

    return total_eth_balance, total_usdt_balance, total_usdc_balance

# Función para obtener el saldo de USDT y USDC en Tron y BSC
def get_tron_usdt_balance():
    wallet_addresses = [
        "TJWBGNKDq4mM4kv3rmHQ56Jfd8kyAkhKdG", 
        "TQcC1DXYgBXpwBniqvj48ktjMrkLNv3uFv",
        "TT6GB73KTwsYNvG9EFgkSKGKTxY6efdQwN",
        "TEMDWHe6yVYvLQ9r3xyAcPV3gLQqXQDUy4",
        "TJrL55qNikyEgiTisU4z2o6nJXCJs3ZJRy",
        "TJeXUgYMVBsm4eKtTB52wT9HWQiKK7XXfW"
    ]
    total_balance = 0
    api_key = "1bd19576-d12e-4fdc-9584-af2373780f93"
    st.write("Escaneando direcciones Tron USDT:")
    for address in wallet_addresses:
        st.write(f"  - {address}")
        url = f"https://apilist.tronscan.org/api/account?address={address}"
        response = requests.get(url)
        response_data = response.json()
        if 'trc20token_balances' in response_data:
            balance = next((int(token['balance']) for token in response_data['trc20token_balances'] if token['tokenId'] == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"), 0)
            total_balance += balance / 1e6
    return total_balance

# Función para obtener el saldo de USDT, USDC y BUSD en BSC
def get_bep20_balances(addresses, api_key):
    usdt_contract_address = "0x55d398326f99059ff775485246999027b3197955"
    usdc_contract_address = "0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
    busd_contract_address = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
    total_usdt_balance = 0
    total_usdc_balance = 0
    total_busd_balance = 0
    st.write("Escaneando direcciones BSC (USDT, USDC, BUSD):")
    for address in addresses:
        st.write(f"  - {address}")
        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={usdt_contract_address}&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        usdt_balance = int(response.json()['result']) / 1e18
        total_usdt_balance += usdt_balance

        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={usdc_contract_address}&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        usdc_balance = int(response.json()['result']) / 1e18
        total_usdc_balance += usdc_balance

        url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={busd_contract_address}&address={address}&tag=latest&apikey={api_key}"
        response = requests.get(url)
        busd_balance = int(response.json()['result']) / 1e18
        total_busd_balance += busd_balance

    return total_usdt_balance, total_usdc_balance, total_busd_balance

# Ejecución de funciones y visualización de resultados
if st.button('Obtener saldos'):
    with st.spinner('Obteniendo saldos...'):
        addresses = ["0x5F30A6e8f15F6c0aF4F1FB99a418EB12e0365dE3", "0x2B810C240eDFFA6D97188838F8D3feA546495Af5", "0xa09051AeB68dE249F49aE64100cb1be63D726fE6"]
        api_key_eth = "3I28J7YR6D183MR7UEQ8YY2U8UCJIT7ZX5"
        api_key_bsc = "CHNW397RZW2GT148SSHHRSQN1BVC4YR9CD"
        
        btc_balance, btc_escrow = get_btc_balance()
        eth_balance, eth_usdt_balance, eth_usdc_balance = get_eth_usdt_usdc_balances(addresses, api_key_eth)
        tron_usdt_balance = get_tron_usdt_balance()
        bep20_usdt_balance, bep20_usdc_balance, bep20_busd_balance = get_bep20_balances(addresses, api_key_bsc)

        st.write(f"SALDO BTC: {btc_balance} BTC ... DEBERÍAS TENER EN ESCROW {btc_escrow} BTC")
        if eth_balance > 5.86:
            eth_to_sell = eth_balance - 5.86
            st.write(f"SALDO ETH: {eth_balance} ETH ... DEBERÍAS VENDER {eth_to_sell:.2f} ETH PARA LLEGAR AL ESCROW DESEADO")
        else:
            st.write(f"SALDO ETH: {eth_balance} ETH ... DEBERÍAS TENER EN ESCROW {eth_balance - 5.86:.2f} ETH")
        st.write(f"SALDO ETH USDT: {eth_usdt_balance} USDT")
        st.write(f"SALDO ETH USDC: {eth_usdc_balance} USDC")
        st.write(f"SALDO TRON USDT: {tron_usdt_balance} USDT")
        st.write(f"SALDO BSC USDT: {bep20_usdt_balance} USDT")
        st.write(f"SALDO BSC USDC: {bep20_usdc_balance} USDC")
        st.write(f"SALDO BSC BUSD: {bep20_busd_balance} BUSD")

        # Sumar todos los saldos de stablecoins (USDT, USDC y BUSD en diferentes redes)
        total_stablecoins = eth_usdt_balance + tron_usdt_balance + bep20_usdt_balance + eth_usdc_balance + bep20_usdc_balance + bep20_busd_balance
        st.write(f"Total en stablecoins (USDT, USDC y BUSD en diferentes redes): {total_stablecoins} USDT/USDC/BUSD")
