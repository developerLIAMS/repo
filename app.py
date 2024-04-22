import streamlit as st
import requests

# Función para obtener las tasas de cambio
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

# Función para mostrar las tasas de cambio en la aplicación
def mostrar_tasas():
    st.title("Consulta de Tasas de Cambio")

    # Obtener las tasas de cambio
    tasas = {
        'COP': obtener_tasa('usdt', 'cop', "enviar"),
        'BRL': obtener_tasa('usdt', 'brl', "enviar"),
        'PEN': obtener_tasa('usdt', 'pen', "enviar"),
        'CLP': obtener_tasa('usdt', 'clp', "enviar"),
        'MXN': obtener_tasa('usdt', 'mxn', "enviar"),
        'PYG': obtener_tasa('usdt', 'pyg', "enviar"),
        'UYU': obtener_tasa('usdt', 'uyu', "enviar"),
    }
    
    # Mostrar las tasas de cambio
    for moneda, tasa in tasas.items():
        if tasa is not None:
            st.write(f"{moneda}: {tasa}")
        else:
            st.write(f"No se pudo obtener la tasa de {moneda}")

    # Mostrar la tasa de cambio EUR/USD
    tasa_compra, tasa_venta = obtener_tasa_euro_usd()
    st.write(f"EUR/USD - Compra: {tasa_compra}, Venta: {tasa_venta}")

    # Mostrar la tasa del dólar blue
    dolar_blue_ask, dolar_blue_compra, dolar_blue_venta = obtener_dolar_blue()
    if dolar_blue_ask is not None:
        st.write(f"Dólar Blue - Tasa Dólar Blue: {dolar_blue_ask}, Compra: {dolar_blue_compra}, Venta: {dolar_blue_venta}")
    else:
        st.write("No se pudo obtener la información del Dólar Blue")

# Configurar la apariencia de la aplicación
st.set_page_config(page_title="Tasas de Cambio", page_icon=":money_with_wings:")
st.markdown(
    """
    <style>
    .stApp {
        max-width: 900px;
        padding: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin-top: 20px;
    }
    .stMarkdown {
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar la aplicación
mostrar_tasas()
