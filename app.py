import streamlit as st
import streamlit.components.v1 as components

# Configuración de página
st.set_page_config(page_title="ALEMA Trading Academy - Calculadora de Lotes", page_icon="📊", layout="centered")

# Estilos CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #FF6B00; /* Color Naranja Institucional */
        margin-top: 10px;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #64748B;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARRUSEL SUPERIOR TIPO TICKER (Fondo Naranja / Letras Blancas) ---
ticker_html = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
  "symbols": [
    {"proName": "FX_IDC:EURUSD", "title": "EUR/USD"},
    {"proName": "FX_IDC:GBPUSD", "title": "GBP/USD"},
    {"proName": "FX_IDC:USDJPY", "title": "USD/JPY"},
    {"proName": "FX_IDC:AUDUSD", "title": "AUD/USD"},
    {"proName": "FX_IDC:USDCAD", "title": "USD/CAD"},
    {"proName": "FX_IDC:USDCHF", "title": "USD/CHF"},
    {"proName": "BITSTAMP:BTCUSD", "title": "BTC/USD"}
  ],
  "showSymbolLogo": true,
  "isTransparent": false,
  "displayMode": "adaptive",
  "colorTheme": "dark",
  "locale": "es"
}
  </script>
</div>
<style>
  /* Personalización del carrusel a Naranja ALEMA */
  .tradingview-widget-container {
    background-color: #FF6B00 !important;
    border-radius: 8px;
    overflow: hidden;
  }
</style>
<!-- TradingView Widget END -->
"""

# Renderizado de la franja carrusel ajustado a altura 78px para celulares
components.html(ticker_html, height=78)

# Encabezado principal
st.markdown('<div class="main-title">ALEMA TRADING ACADEMY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calculadora de Lotes y Gestión de Riesgo</div>', unsafe_allow_html=True)

st.divider()

# --- SECCIÓN 1: PARÁMETROS DE LA OPERACIÓN ---
st.subheader("⚙️ Parámetros de la Cuenta y Riesgo")

par_activo = st.text_input("Par de Divisas / Activo (Opcional)", value="EUR/USD").strip().upper()

# Limpiar el nombre del par para el enlace de TradingView
symbol_tv = par_activo.replace("/", "").replace("-", "").replace(" ", "")
tv_url = f"https://es.tradingview.com/chart/?symbol=FX:{symbol_tv}"
investing_url = "https://es.investing.com/economic-calendar/"

# Botones de herramientas externas
st.link_button("📈 Ver Gráfico en TradingView", tv_url)
st.link_button("📅 Ver Calendario Económico (Investing)", investing_url)

es_jpy = "JPY" in par_activo
valor_pip_sugerido = 7.0 if es_jpy else 10.0

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("Balance de la Cuenta ($)", value=250.0, step=10.0)
    riesgo_pct = st.number_input("Porcentaje de Riesgo (%)", value=1.0, step=0.5)

with col2:
    sl_pips = st.number_input("Tamaño del Stop Loss (Pips)", value=15.0, step=1.0)
    valor_pip = st.number_input("Valor del Pip por Lote Estándar ($)", value=valor_pip_sugerido, step=0.5)

if es_jpy:
    st.info("💡 **Par JPY Detectado:** Valor del pip ajustado automáticamente a **$7.00 USD**.")
else:
    st.info("💡 **Par Estándar Detectado:** Valor del pip ajustado automáticamente a **$10.00 USD**.")

# --- SECCIÓN 2: CÁLCULOS MATEMÁTICOS ---
dinero_arriesgar = balance * (riesgo_pct / 100.0)
lotaje = dinero_arriesgar / (sl_pips * valor_pip) if (sl_pips > 0 and valor_pip > 0) else 0.0

st.divider()

# --- SECCIÓN 3: RESULTADOS ---
st.subheader("📊 Resultados de Posición")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="Dinero Máximo a Arriesgar ($)", value=f"${dinero_arriesgar:.2f}")

with res_col2:
    st.metric(label="Lotaje Exacto a Colocar", value=f"{lotaje:.2f}")

st.caption("© ALEMA Trading Academy. Reservados todos los derechos.")
