import streamlit as st

# Configuración de página con estética de ALEMA Trading Academy
st.set_page_config(page_title="ALEMA Trading Academy - Calculadora de Lotes", page_icon="📊", layout="centered")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1E293B;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #64748B;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<div class="main-title">ALEMA TRADING ACADEMY</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calculadora de Lotes y Gestión de Riesgo</div>', unsafe_allow_html=True)

st.divider()

# --- SECCIÓN 1: PARÁMETROS DE LA OPERACIÓN ---
st.subheader("⚙️ Parámetros de la Cuenta y Riesgo")

par_activo = st.text_input("Par de Divisas / Activo (Opcional)", value="EUR/USD").strip().upper()

# Detección si es un par con JPY para ajustar el valor por defecto del pip
es_jpy = "JPY" in par_activo
valor_pip_defecto = 7.0 if es_jpy else 10.0

col1, col2 = st.columns(2)

with col1:
    balance = st.number_input("Balance de la Cuenta ($)", value=250.0, step=10.0)
    riesgo_pct = st.number_input("Porcentaje de Riesgo (%)", value=5.0, step=0.5)

with col2:
    sl_pips = st.number_input("Tamaño del Stop Loss (Pips)", value=10.0, step=1.0)
    valor_pip = st.number_input("Valor del Pip por Lote Estándar ($)", value=valor_pip_defecto, step=0.5)

if es_jpy:
    st.info("💡 **Par JPY Detectado:** Ajustado el valor de pip promedio sugerido a $7.0 USD.")

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
