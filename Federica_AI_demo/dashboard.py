import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Federica AI – HR Control Room")

# lettura dati demo da CSV
recruiting = pd.read_csv("Federica_AI_demo/data/vw_recruiting_hr.csv")
onboarding = pd.read_csv("Federica_AI_demo/data/onboarding_hr.csv")

# filtro ruolo
ruoli = ["Tutti"] + sorted(recruiting["ruolo"].dropna().unique().tolist())
ruolo_selezionato = st.sidebar.selectbox("Seleziona ruolo", ruoli)

if ruolo_selezionato != "Tutti":
    recruiting = recruiting[recruiting["ruolo"] == ruolo_selezionato]

# KPI recruiting
totale_candidati = len(recruiting)
totale_assunti = len(recruiting[recruiting["stato"] == "Assunto"])
media_colloqui = recruiting["valutazione"].mean()

# KPI onboarding
totale_onboarding = len(onboarding)

# titolo
st.title("📊 Federica AI – HR Control Room")
st.caption("Demo portfolio HR Data Analytics con Python, Pandas e Streamlit")

# layout a 2 colonne
col_left, col_right = st.columns(2)

with col_left:
    st.header("📊 Recruiting")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("👥 Candidati totali", totale_candidati)

    with col2:
        st.metric("✅ Assunti", totale_assunti)

    with col3:
        st.metric("🗓️ Media colloqui", round(media_colloqui, 2))

    st.subheader("📊 Candidati per fonte")
    fonte = recruiting.groupby("fonte").size().reset_index(name="candidati")
    st.bar_chart(fonte.set_index("fonte"))

    st.subheader("🎯 Funnel recruiting")
    funnel = recruiting.groupby("stato").size().reset_index(name="totale")
    st.bar_chart(funnel.set_index("stato"))

    st.subheader("🎯 Assunzioni per fonte")
    assunti_df = recruiting[recruiting["stato"] == "Assunto"]
    st.metric("Totale assunti", len(assunti_df))

    if not assunti_df.empty:
        assunti_per_fonte = assunti_df["fonte"].value_counts()
        st.bar_chart(assunti_per_fonte)
    else:
        st.info("Nessuna assunzione registrata")

    st.subheader("📅 Distribuzione colloqui")
    st.bar_chart(recruiting["valutazione"])

    st.subheader("📌 Stato recruiting")
    in_selezione = len(recruiting[recruiting["stato"] == "In selezione"])
    rifiutati = len(recruiting[recruiting["stato"] == "Rifiutato"])
    assunti = len(recruiting[recruiting["stato"] == "Assunto"])
    totale = len(recruiting)

    if totale > 0:
        tasso_assunzione = round((assunti / totale) * 100, 1)
        tasso_rifiuto = round((rifiutati / totale) * 100, 1)
    else:
        tasso_assunzione = 0
        tasso_rifiuto = 0

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("🟡 In selezione", in_selezione)

    with col5:
        st.metric("🔴 Tasso rifiuto", f"{tasso_rifiuto}%")

    with col6:
        st.metric("🟢 Tasso assunzione", f"{tasso_assunzione}%")

with col_right:
    st.header("🚀 Onboarding")
    st.metric("Nuovi onboarding", totale_onboarding)

    st.subheader("Stato onboarding")
    stato_onboarding = onboarding["stato_onboarding"].value_counts()
    st.bar_chart(stato_onboarding)

    st.header("📈 Performance")
    st.info("Sezione performance in sviluppo")

    st.header("🤖 HR Assistant")
    domanda = st.text_input("Fai una domanda sui dati HR")

    if domanda:
        domanda = domanda.lower()

        onboarding_completati = 0
        if "stato_onboarding" in onboarding.columns:
            onboarding_completati = len(
                onboarding[onboarding["stato_onboarding"].astype(str).str.lower() == "completato"]
            )

        if "candidati" in domanda:
            st.write(f"👥 Il numero totale di candidati è {totale_candidati}")

        elif "assunti" in domanda:
            st.write(f"✅ Il numero totale di assunti è {totale_assunti}")

        elif "onboarding" in domanda and "completati" in domanda:
            st.write(f"🚀 Gli onboarding completati sono {onboarding_completati}")

        elif "onboarding" in domanda:
            st.write(f"🚀 Ci sono {totale_onboarding} onboarding registrati")

        elif "rifiutati" in domanda or "rifiuti" in domanda:
            st.write(f"❌ I candidati rifiutati sono {rifiutati}")

        elif "in selezione" in domanda:
            st.write(f"🟡 I candidati in selezione sono {in_selezione}")

        elif "tasso di assunzione" in domanda:
            st.write(f"📈 Il tasso di assunzione è {tasso_assunzione}%")

        elif "fonti" in domanda or "fonte" in domanda:
            fonte_top = recruiting["fonte"].value_counts().idxmax()
            num_fonte_top = recruiting["fonte"].value_counts().max()
            st.write(f"📊 La fonte con più candidati è {fonte_top} con {num_fonte_top} candidati")

        else:
            st.write("Posso rispondere su candidati, assunti, rifiutati, onboarding, tasso di assunzione e fonti.")