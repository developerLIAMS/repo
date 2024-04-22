import requests
import streamlit as st

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
    tasa_compra = round(tasa_base * 0.995, 2)  # Compra a -0.5%, redondeado a dos decimales
    tasa_venta = round(tasa_base * 1.02, 2)    # Venta a +2%, redondeado a dos decimales
    return tasa_compra, tasa_venta

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

def obtener_tasas_de_cambio():
    tasas = []
    
    monedas_enviar_recibir = ['cop', 'brl', 'pen', 'clp']
    monedas_solo_enviar = ['mxn', 'pyg', 'uyu']

    # Mostrar tasas para enviar y recibir
    for moneda in monedas_enviar_recibir:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        tasa_recibir = obtener_tasa('usdt', moneda, "recibir")
        tasas.append((moneda.upper(), f"{tasa_enviar} / {tasa_recibir}"))

    # Mostrar tasas solo para enviar
    for moneda in monedas_solo_enviar:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        tasas.append((moneda.upper(), str(tasa_enviar)))

    # Mostrar tasa de cambio Euro a Dólar con compra y venta
    tasa_compra, tasa_venta = obtener_tasa_euro_usd()
    tasas.append(("EUR/USD", f"Compra: {tasa_compra}, Venta: {tasa_venta}"))

    # Obtener y mostrar tasas del dólar blue
    dolar_blue_ask, dolar_blue_compra, dolar_blue_venta = obtener_dolar_blue()
    if dolar_blue_ask is not None:
        tasas.append(("Dólar Blue", f"Tasa Dólar Blue: {dolar_blue_ask}, Compra: {dolar_blue_compra}, Venta: {dolar_blue_venta}"))
    else:
        tasas.append(("Dólar Blue", "No se pudo obtener la información del dólar blue."))
    
    return tasas

# Interfaz de usuario con Streamlit
st.title("Consulta de Tasas de Cambio")
tasas = obtener_tasas_de_cambio()
for tasa in tasas:
    st.write(f"{tasa[0]}: {tasa[1]}")
