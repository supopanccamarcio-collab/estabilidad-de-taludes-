"""
Modulo de Clasificacion GSI (Geological Strength Index)
Curso: Introduccion a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import numpy as np
import streamlit as st

# Tablas de valoracion para JCond89
PERSISTENCIA_VALS = {
    "< 1 m": 6,
    "1 - 3 m": 4,
    "3 - 10 m": 2,
    "10 - 20 m": 1,
    "> 20 m": 0
}

APERTURA_VALS = {
    "Nada": 6,
    "< 0.1 mm": 5,
    "0.1 - 1.0 mm": 4,
    "1 - 5 mm": 1,
    "> 5 mm": 0
}

RUGOSIDAD_VALS = {
    "Muy rugosa": 6,
    "Rugosa": 5,
    "Ligeramente rugosa": 3,
    "Ondulada": 1,
    "Suave": 0
}

RELLENO_VALS = {
    "Ninguno": 6,
    "Relleno duro < 5 mm": 4,
    "Relleno duro > 5 mm": 2,
    "Relleno blando < 5 mm": 2,
    "Relleno blando > 5 mm": 0
}

ALTERACION_VALS = {
    "Inalterado": 6,
    "Ligeramente alterado": 5,
    "Moderadamente alterado": 3,
    "Muy alterado": 1,
    "Descompuesto": 0
}

ESTRUCTURA_ROCA = {
    "Bloques muy grandes (VB)": {"rango_gsi": "75-90"},
    "Bloques grandes (B)": {"rango_gsi": "55-75"},
    "Bloques medianos (MB)": {"rango_gsi": "35-55"},
    "Bloques pequenos (S)": {"rango_gsi": "15-35"},
    "Fragmentos muy pequenos (VF)": {"rango_gsi": "3-15"}
}

SUPERFICIE_JUNTAS = {
    "Muy buena (VB)": {"rango_gsi": "75-90"},
    "Buena (B)": {"rango_gsi": "55-75"},
    "Regular (F)": {"rango_gsi": "35-55"},
    "Mala (P)": {"rango_gsi": "15-35"},
    "Muy mala (VP)": {"rango_gsi": "3-15"}
}

def calcular_jcond89(persistencia, apertura, rugosidad, relleno, alteracion):
    return persistencia + apertura + rugosidad + relleno + alteracion

def calcular_rqd_lambda(lambda_val):
    return 100 * np.exp(-0.1 * lambda_val) * (0.1 * lambda_val + 1)

def calcular_rqd_jv(jv):
    rqd = 115 - 3.3 * jv
    return max(0, min(100, rqd))

def calcular_gsi(jcond89, rqd):
    gsi = 1.5 * jcond89 + rqd / 2
    return max(10, min(90, gsi))

def gsi_a_clasificacion(gsi):
    if gsi > 65:
        return "Macizo rocoso competente, poco fracturado"
    elif gsi > 40:
        return "Macizo rocoso moderadamente fracturado"
    elif gsi > 25:
        return "Macizo rocoso muy fracturado / roca blanda"
    else:
        return "Suelo residual / Material coluvial / Roca muy alterada"

def gsi_a_metodo(gsi):
    if gsi > 65:
        return {
            "principal": "Hoek-Brown con Falla Planar o Falla por Cunias",
            "alternativo": "Bishop Simplificado (verificacion)",
            "tipo_falla": "Planar/Cunias"
        }
    elif gsi > 40:
        return {
            "principal": "Bishop Simplificado o Morgenstern-Price",
            "alternativo": "Fellenius",
            "tipo_falla": "Circular"
        }
    elif gsi > 25:
        return {
            "principal": "Fellenius o Bishop con parametros reducidos",
            "alternativo": "Taylor (Stability Number)",
            "tipo_falla": "Circular"
        }
    else:
        return {
            "principal": "Mohr-Coulomb, Talud Infinito o Culmann",
            "alternativo": "Taylor (phi=0)",
            "tipo_falla": "Superficial plana"
        }

def gsi_a_materiales(gsi):
    if gsi > 65:
        return ["Granito Sano", "Basalto", "Diorita"]
    elif gsi > 40:
        return ["Andesita", "Caliza Sana", "Arenisca", "Granito Fracturado"]
    elif gsi > 25:
        return ["Lutita", "Filita", "Esquisto", "Pizarra", "Caliza Fracturada"]
    else:
        return ["Suelo Residual Granitico", "Suelo Residual Andesitico", 
                "Material Coluvial", "Arcilla Blanda", "Arcilla Compacta",
                "Arena Suelta", "Arena Densa"]

def render_gsi_module():
    st.markdown("## 🏔️ Modulo GSI - Clasificacion Geomecanica")
    st.markdown("*Basado en Hoek, Carter & Diederichs (2013)*")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 Evaluacion Detallada", "🎯 GSI Directo", "📋 Tabla Cruzada"])

    with tab1:
        st.markdown("### Evaluacion de Condiciones de Juntas (JCond89)")

        col1, col2, col3 = st.columns(3)

        with col1:
            persistencia = st.selectbox("**Persistencia**", list(PERSISTENCIA_VALS.keys()))
            val_persistencia = PERSISTENCIA_VALS[persistencia]
            st.markdown(f"**Valor: {val_persistencia}**")

        with col2:
            apertura = st.selectbox("**Apertura**", list(APERTURA_VALS.keys()))
            val_apertura = APERTURA_VALS[apertura]
            st.markdown(f"**Valor: {val_apertura}**")

        with col3:
            rugosidad = st.selectbox("**Rugosidad**", list(RUGOSIDAD_VALS.keys()))
            val_rugosidad = RUGOSIDAD_VALS[rugosidad]
            st.markdown(f"**Valor: {val_rugosidad}**")

        col4, col5 = st.columns(2)

        with col4:
            relleno = st.selectbox("**Relleno**", list(RELLENO_VALS.keys()))
            val_relleno = RELLENO_VALS[relleno]
            st.markdown(f"**Valor: {val_relleno}**")

        with col5:
            alteracion = st.selectbox("**Alteracion**", list(ALTERACION_VALS.keys()))
            val_alteracion = ALTERACION_VALS[alteracion]
            st.markdown(f"**Valor: {val_alteracion}**")

        jcond89 = calcular_jcond89(val_persistencia, val_apertura, val_rugosidad, val_relleno, val_alteracion)

        st.markdown("---")
        st.markdown("### Calculo del RQD")

        metodo_rqd = st.radio("Metodo de calculo de RQD:", 
                               ["De mapeo de superficie (lambda)", "De conteo volumetrico (Jv)"],
                               horizontal=True)

        if metodo_rqd == "De mapeo de superficie (lambda)":
            lambda_val = st.slider("Frecuencia de juntas lambda (juntas/m)", 0.0, 50.0, 10.0, 0.5)
            rqd = calcular_rqd_lambda(lambda_val)
        else:
            jv = st.slider("Conteo volumetrico Jv (juntas/m3)", 0.0, 35.0, 10.0, 0.5)
            rqd = calcular_rqd_jv(jv)

        st.markdown(f"**RQD calculado: {rqd:.1f}%**")
        gsi = calcular_gsi(jcond89, rqd)

    with tab2:
        st.markdown("### Ingreso Directo de GSI")
        gsi_directo = st.slider("GSI", 10, 90, 50, 1)
        jcond89 = None
        rqd = None
        gsi = gsi_directo

    with tab3:
        st.markdown("### Tabla Cruzada: Estructura vs Superficie")
        estructura = st.selectbox("**Estructura de la Roca**", list(ESTRUCTURA_ROCA.keys()))
        superficie = st.selectbox("**Condicion de Superficie**", list(SUPERFICIE_JUNTAS.keys()))

        def promedio_rango(rango_str):
            parts = rango_str.split("-")
            return (int(parts[0]) + int(parts[1])) / 2

        gsi_est = promedio_rango(ESTRUCTURA_ROCA[estructura]["rango_gsi"])
        gsi_sup = promedio_rango(SUPERFICIE_JUNTAS[superficie]["rango_gsi"])
        gsi = (gsi_est + gsi_sup) / 2
        st.markdown(f"**GSI estimado: {gsi:.0f}**")
        jcond89 = None
        rqd = None

    # Resultados
    st.markdown("---")
    st.markdown("## 📊 Resultados de Clasificacion GSI")

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("GSI", f"{gsi:.1f}")
    with col_res2:
        clasificacion = gsi_a_clasificacion(gsi)
        st.metric("Clasificacion", clasificacion)
    with col_res3:
        recomendacion = gsi_a_metodo(gsi)
        st.metric("Metodo Principal", recomendacion["principal"])

    # Barra de progreso
    progress = (gsi - 10) / 80
    st.progress(progress, text=f"GSI = {gsi:.1f} / 90")

    # Recomendaciones
    st.markdown("---")
    st.markdown("### 🎯 Recomendaciones de Analisis")
    rec = gsi_a_metodo(gsi)

    col_rec1, col_rec2 = st.columns(2)
    with col_rec1:
        st.markdown("**Metodo Principal:**")
        st.success(f"📌 {rec['principal']}")
        st.markdown(f"**Tipo de Falla:** {rec['tipo_falla']}")
    with col_rec2:
        st.markdown("**Metodo Alternativo:**")
        st.info(f"📌 {rec['alternativo']}")

    st.markdown("### 🪨 Materiales Tipicos")
    materiales_sugeridos = gsi_a_materiales(gsi)
    st.write(", ".join([f"**{m}**" for m in materiales_sugeridos]))

    # Guardar en session state
    st.session_state["gsi_calculado"] = gsi
    st.session_state["jcond89"] = jcond89
    st.session_state["rqd"] = rqd
    st.session_state["clasificacion_gsi"] = clasificacion
    st.session_state["metodo_recomendado"] = rec["principal"]
    st.session_state["materiales_sugeridos"] = materiales_sugeridos

    return gsi
