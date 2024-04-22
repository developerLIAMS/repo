import streamlit as st
import requests

def obtener_tasa(coin, fiat, tipo):
    url = f'https://criptoya.com/api/binancep2p/{coin}/{fiat}/0.1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ask = data['ask']
        if tipo == "enviar":
            return round(ask * 0.94, 1)  # Restar 6% y redondear a un decimal
        elif tipo == "recibir":
            return round(ask * 1.05, 1)  # Sumar 5% y redondear a un decimal
    else:
        return None

def obtener_tasa_euro_usd():
    tasa_base = 1.065  # Tasa EUR/USD
    tasa_compra = tasa_base * 0.995  # Compra a -0.5%
    tasa_venta = tasa_base * 1.02    # Venta a +2%
    return tasa_compra, tasa_venta  # Devuelve sin redondear

def main():
    monedas_enviar_recibir = ['cop', 'brl', 'pen', 'clp']
    monedas_solo_enviar = ['mxn', 'pyg', 'uyu']

    st.title("Consulta de Tasas de Cambio")
    selected_coin = st.selectbox("Elige la moneda", monedas_enviar_recibir + monedas_solo_enviar)
    tipo = st.selectbox("Elige el tipo de transacción", ["enviar", "recibir"])
    if st.button("Obtener Tasa"):
        tasa = obtener_tasa('usdt', selected_coin, tipo)
        if tasa:
            st.success(f"La tasa para {selected_coin} es {tasa}")
        else:
            st.error("Error al obtener la tasa.")

    # Mostrar tasa de cambio Euro a Dólar
    if st.button("Tasa de Cambio EUR/USD"):
        tasa_compra, tasa_venta = obtener_tasa_euro_usd()
        st.write(f"Tasa de cambio EUR/USD - Compra: {tasa_compra}, Venta: {tasa_venta}")

if __name__ == "__main__":
    main()