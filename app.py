import streamlit as st
import requests

# Función para obtener las tasas de cambio
def obtener_tasas_de_cambio():
    tasas = {}
    monedas_enviar_recibir = ['cop', 'brl', 'pen', 'clp']
    monedas_solo_enviar = ['mxn', 'pyg', 'uyu']
    for moneda in monedas_enviar_recibir:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        tasa_recibir = obtener_tasa('usdt', moneda, "recibir")
        tasas[moneda.upper()] = (tasa_enviar, tasa_recibir)
    for moneda in monedas_solo_enviar:
        tasa_enviar = obtener_tasa('usdt', moneda, "enviar")
        tasas[moneda.upper()] = tasa_enviar
    return tasas

# Función para obtener la tasa de cambio EUR/USD
def obtener_tasa_euro_usd():
    tasa_base = 1.065  # Tasa EUR/USD
    tasa_compra = tasa_base * 0.995  # Compra a -0.5%
    tasa_venta = tasa_base * 1.02    # Venta a +2%
    return tasa_compra, tasa_venta  # Devuelve sin redondear

# Función para obtener la tasa del dólar blue
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

# Configuración de la apariencia de la aplicación
st.set_page_config(page_title="Consulta de Tasas de Cambio", page_icon=":money_with_wings:")
st.title("Tasas de Cambio")

# Obtener y mostrar las tasas de cambio
tasas = obtener_tasas_de_cambio()
for moneda, tasa in tasas.items():
    if isinstance(tasa, tuple):
        st.write(f"{moneda}: {tasa[0]} / {tasa[1]}")
    else:
        st.write(f"{moneda}: {tasa}")

# Mostrar la tasa de cambio EUR/USD
tasa_compra, tasa_venta = obtener_tasa_euro_usd()
st.write(f"EUR/USD: Compra: {tasa_compra}, Venta: {tasa_venta}")

# Mostrar la tasa del dólar blue
dolar_blue_ask, dolar_blue_compra, dolar_blue_venta = obtener_dolar_blue()
if dolar_blue_ask is not None:
    st.write(f"Dólar Blue: Tasa Dólar Blue: {dolar_blue_ask}, Compra: {dolar_blue_compra}, Venta: {dolar_blue_venta}")
else:
    st.write("No se pudo obtener la información del Dólar Blue")

