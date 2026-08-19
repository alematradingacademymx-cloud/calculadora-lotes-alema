import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="ALEMA Trading Academy - Calculadora de Lotes", page_icon="📊", layout="centered")

# Estilos CSS personalizados con Fondo Azul Oscuro Elegante
st.markdown("""
    <style>
    /* Fondo General Azul Oscuro */
    .stApp {
        background-color: #0E1726;
        color: #F1F5F9;
    }
    
    /* Encabezados y Textos */
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: 800;
        color: #FF6B00; /* Naranja Institucional */
        margin-top: 10px;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }
    .sub-title {
        text-align: center;
        font-size: 17px;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    
    /* Contenedor de Copia Rápida */
    .copy-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 15px;
        color: #38BDF8;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARRUSEL SUPERIOR TIPO TICKER ---
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
  .tradingview-widget-container {
    background-color: #FF6B00 !important;
    border-radius: 8px;
    overflow: hidden;
  }
</style>
<!-- TradingView Widget END -->
"""

components.html(ticker_html, height=78)

# Encabezado principal
st.markdown('<div class="main-title">ALEMA TRADING ACADEMY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calculadora de Lotes y Gestión de Riesgo</div>', unsafe_allow_html=True)

# --- GUÍA RÁPIDA PLEGABLE ---
with st.expander("📖 Guía Rápida de Uso para Alumnos"):
    st.markdown("""
    1. **Par de Divisas:** Coloca el activo a operar para ajustar el valor por pip automáticamente.
    2. **Gestiona tu Capital:** Establece tu porcentaje de riesgo por operación (Recomendado: **1% a 2%**).
    3. **Stop Loss:** Ingrese la distancia en pips medida en el gráfico.
    4. **Resultado:** Copia el lotaje exacto para tu terminal de trading.
    """)

st.divider()

# --- SECCIÓN 1: PARÁMETROS DE LA OPERACIÓN ---
st.subheader("⚙️ Parámetros de la Cuenta y Riesgo")

par_activo = st.text_input("Par de Divisas / Activo (Opcional)", value="EUR/USD").strip().upper()

symbol_tv = par_activo.replace("/", "").replace("-", "").replace(" ", "")
tv_url = f"https://es.tradingview.com/chart/?symbol=FX:{symbol_tv}"
investing_url = "https://es.investing.com/economic-calendar/"

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

# --- SECCIÓN 2: CÁLCULOS MATEMÁTICOS ---
dinero_arriesgar = balance * (riesgo_pct / 100.0)
lotaje = dinero_arriesgar / (sl_pips * valor_pip) if (sl_pips > 0 and valor_pip > 0) else 0.0

st.divider()

# --- SEMÁFORO DE GESTIÓN DE RIESGO (PSICOTRADING) ---
if riesgo_pct <= 2.0:
    st.success(f"🟢 **Riesgo Institucional Saludable ({riesgo_pct}%):** Operación en rangos de conservación de capital.")
elif riesgo_pct <= 5.0:
    st.warning(f"🟠 **Riesgo Moderado ({riesgo_pct}%):** Evalúa la confluencia técnica de la entrada.")
else:
    st.error(f"🔴 **Alerta de Sobrerriesgo ({riesgo_pct}%):** Considera bajar el porcentaje para proteger la cuenta.")

# --- SECCIÓN 3: RESULTADOS ---
st.subheader("📊 Resultados de Posición")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.metric(label="Dinero Máximo a Arriesgar ($)", value=f"${dinero_arriesgar:.2f}")

with res_col2:
    st.metric(label="Lotaje Exacto a Colocar", value=f"{lotaje:.2f}")

# --- COPIA RÁPIDA ---
st.subheader("📋 Lote para la Posición")
st.markdown(f"""
<div class="copy-box">
<b>{par_activo}</b><br>
🔹 Lotaje Exacto: <b>{lotaje:.2f}</b><br>
🛑 Riesgo: <b>${dinero_arriesgar:.2f} ({riesgo_pct}%)</b>
</div>
""", unsafe_allow_html=True)

# --- GRÁFICO VISUAL DE DONA ---
st.subheader("📉 Distribución del Balance")
capital_seguro = max(0.0, balance - dinero_arriesgar)

fig = go.Figure(data=[go.Pie(
    labels=['Capital Seguro', 'Capital en Riesgo'],
    values=[capital_seguro, dinero_arriesgar],
    hole=.5,
    marker_colors=['#10B981', '#FF6B00']
)])

fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    height=220,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#F1F5F9'),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

st.caption("© ALEMA Trading Academy. Reservados todos los derechos.")
