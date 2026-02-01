import streamlit as st
import math

# Sovelluksen asetukset
st.set_page_config(page_title="Focaccia-laskuri 1.6", page_icon="🍞")
st.title("🍞 Focaccia-laskuri")
# Lisää tämä koodin alkuun (otsikon jälkeen)
st.markdown("""
    <style>
    /* Suurentaa syöttökenttien fonttia */
    input {
        font-size: 24px !important;
    }
    /* Suurentaa kenttien yläpuolella olevia otsikoita (labels) */
    .stNumberInput label {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    /* Suurentaa valintapallojen (Radio) tekstiä */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 22px !important;
    }
    
    /* Suurentaa itse valintapalloja ja niiden välejä */
    div[data-testid="stWidgetLabel"] p {
        font-size: 22px !important;
        font-weight: bold !important;
    }

    /* Suurentaa palloja ympäröivää tekstiä mobiilissa */
    .st-bc {
        font-size: 22px !important;
    }
    </style>
    """, unsafe_allow_html=True)
# Valitaan vuoan muoto
muoto = st.radio("Valitse vuoan muoto:", ["Suorakaide", "Pyöreä"])

# --- SYÖTTÖKENTÄT ---
col1, col2 = st.columns(2)

with col1:
    hydraatio = st.number_input("Hydraatio% (suositus 65-80)", min_value=1, max_value=100, value=75)
    # Suola yhdellä desimaalilla
    suola_prosentti = st.number_input("Suola% (suositus 2.0-3.0)", min_value=0.0, max_value=10.0, value=2.8, step=0.1, format="%.1f")
    # Korkeus kokonaislukuna
    korkeus = st.number_input("Korkeus (cm)", min_value=1, max_value=10, value=4, step=1)

with col2:
    if muoto == "Suorakaide":
        pituus = st.number_input("Pituus (cm)", min_value=1.0, value=25.0, step=0.1, format="%.1f")
        leveys = st.number_input("Leveys (cm)", min_value=1.0, value=25.0, step=0.1, format="%.1f")
        pinta_ala = pituus * leveys
    else:
        halkaisija = st.number_input("Halkaisija (cm)", min_value=1.0, value=25.0, step=0.1, format="%.1f")
        pinta_ala = math.pow(halkaisija / 2, 2) * math.pi
    maara = st.number_input("Määrä", min_value=1, value=1)

# --- LASKENTA ---
yksi_taikina = (pinta_ala * math.sqrt(korkeus)) / math.sqrt(5)
taikina_yhteensa = yksi_taikina * maara

kokonaisprosentit = 1 + (hydraatio / 100) + (suola_prosentti / 100)
jauhot_yhteensa = taikina_yhteensa / kokonaisprosentit
vesi_yhteensa = jauhot_yhteensa * (hydraatio / 100)
suola_yhteensa = jauhot_yhteensa * (suola_prosentti / 100)

# Poolish 30% ja pyöristys 100g tarkkuuteen (50g jauhoja)
poolish_tavoite = taikina_yhteensa * 0.30
poolish_yhteispaino = round(poolish_tavoite / 100) * 100
if poolish_yhteispaino < 100:
    poolish_yhteispaino = 100

poolish_jauhot = poolish_yhteispaino / 2
poolish_vesi = poolish_yhteispaino / 2
poolish_hiiva = (poolish_jauhot / 100) + 1

# Päätäikina
taikina_jauhot = jauhot_yhteensa - poolish_jauhot
taikina_vesi = vesi_yhteensa - poolish_vesi

# --- TULOKSET ---
st.divider()

# Käytetään st.markdownia, jotta saadaan fonttikokoja säädettyä
c1, c2 = st.columns(2)

with c1:
    st.subheader("🥣 Poolish")
    st.markdown(f"#### **{int(poolish_jauhot)} g** Jauhoja")
    st.markdown(f"#### **{int(poolish_vesi)} g** Vettä")
    st.markdown(f"#### **{poolish_hiiva:.1f} g** Hiivaa")

with c2:
    st.subheader("🧑‍🍳 Päätäikina")
    st.markdown(f"#### **{int(taikina_jauhot)} g** Jauhoja")
    st.markdown(f"#### **{int(taikina_vesi)} g** Vettä")
    st.markdown(f"#### **{suola_yhteensa:.1f} g** Suolaa")

st.divider()
# Taikina yhteensä alimmaisena

st.markdown(f"### **Taikina yhteensä: {int(taikina_yhteensa)} g**")




