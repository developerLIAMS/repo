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

def obtener_dolar_blue():
    url = 'https://criptoya.com/api/dolar'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        dolar_blue_ask = data['blue']['ask']
        tasa_compra = dolar_blue_ask - 25
        tasa_venta = dolar_blue_ask + 10
        return dolar_blue_ask, tasa_compra, tasa_venta
    else:
        return None, None, None

def mostrar_tasas():
    st.title("Consulta de Tasas de Cambio")
    monedas_enviar_recibir = ['cop', 'brl', 'pen', 'clp']
    monedas_solo_enviar = ['mxn', 'pyg', 'uyu']
    resultados = {}
    
    for moneda in monedas_enviar_recibir:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        tasa_recibir = obtener_tasa('usdt', moneda, "recibir")
        resultados[moneda] = f"{tasa_enviar} / {tasa_recibir}"

    for moneda in monedas_solo_enviar:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        resultados[moneda] = f"{tasa_enviar}"

    tasa_compra, tasa_venta = obtener_tasa_euro_usd()
    resultados["EUR/USD"] = f"Compra: {tasa_compra}, Venta: {tasa_venta}"

    dolar_blue_ask, dolar_blue_compra, dolar_blue_venta = obtener_dolar_blue()
    if dolar_blue_ask is not None:
        resultados["Dólar Blue"] = f"Tasa Dólar Blue: {dolar_blue_ask}, Compra: {dolar_blue_compra}, Venta: {dolar_blue_venta}"
    else:
        resultados["Dólar Blue"] = "No disponible"

    for key, value in resultados.items():
        st.write(f"{key}: {value}")

if __name__ == "__main__":
    if st.button('RUN'):
        mostrar_tasas()
