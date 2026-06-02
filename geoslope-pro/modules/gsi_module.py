"""
Módulo de Clasificación GSI (Geological Strength Index)
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import numpy as np
import streamlit as st

# Tablas de valoración para JCond89 (según Bieniawski 1989)
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

# Estructura de la roca para GSI (Hoek, Carter & Diederichs 2013)
ESTRUCTURA_ROCA = {
    "Bloques muy grandes (VB)": {"descripcion": "Bloques muy grandes, interbloques muy escasos", "rango_gsi": "75-90"},
    "Bloques grandes (B)": {"descripcion": "Bloques grandes, interbloques escasos", "rango_gsi": "55-75"},
    "Bloques medianos (MB)": {"descripcion": "Bloques medianos, interbloques moderados", "rango_gsi": "35-55"},
    "Bloques pequeños (S)": {"descripcion": "Bloques pequeños, interbloques frecuentes", "rango_gsi": "15-35"},
    "Fragmentos muy pequeños (VF)": {"descripcion": "Fragmentos muy pequeños, interbloques muy frecuentes", "rango_gsi": "3-15"}
}

SUPERFICIE_JUNTAS = {
    "Muy buena (VB)": {"descripcion": "Muy rugosa, sin alteración, sin relleno, estrecha", "rango_gsi": "75-90"},
    "Buena (B)": {"descripcion": "Rugosa, ligeramente alterada, sin relleno, estrecha", "rango_gsi": "55-75"},
    "Regular (F)": {"descripcion": "Ligeramente rugosa, moderadamente alterada, relleno duro", "rango_gsi": "35-55"},
    "Mala (P)": {"descripcion": "Suave, muy alterada, relleno blando", "rango_gsi": "15-35"},
    "Muy mala (VP)": {"descripcion": "Descompuesta, relleno blando, muy ancha", "rango_gsi": "3-15"}
}

def calcular_jcond89(persistencia, apertura, rugosidad, relleno, alteracion):
    """Calcula JCond89 sumando las 5 valoraciones"""
    return persistencia + apertura + rugosidad + relleno + alteracion

def calcular_rqd_lambda(lambda_val):
    """RQD desde frecuencia de juntas (Priest & Hudson, 1976)"""
    return 100 * np.exp(-0.1 * lambda_val) * (0.1 * lambda_val + 1)

def calcular_rqd_jv(jv):
    """RQD desde conteo volumétrico (Palmström, 1982)"""
    rqd = 115 - 3.3 * jv
    return max(0, min(100, rqd))

def calcular_gsi(jcond89, rqd):
    """GSI según Hoek, Carter & Diederichs (2013)"""
    gsi = 1.5 * jcond89 + rqd / 2
    return max(10, min(90, gsi))

def gsi_a_clasificacion(gsi):
    """Clasificación del macizo rocoso según GSI"""
    if gsi > 65:
        return "Macizo rocoso competente, poco fracturado"
    elif gsi > 40:
        return "Macizo rocoso moderadamente fracturado"
    elif gsi > 25:
        return "Macizo rocoso muy fracturado / roca blanda"
    else:
        return "Suelo residual / Material coluvial / Roca muy alterada"

def gsi_a_metodo(gsi):
    """Recomendación de método según GSI"""
    if gsi > 65:
        return {
            "principal": "Hoek-Brown con Falla Planar o Falla por Cuñas",
            "alternativo": "Bishop Simplificado (verificación)",
            "tipo_falla": "Planar/Cuñas"
        }
    elif gsi > 40:
        return {
            "principal": "Bishop Simplificado o Morgenstern-Price",
            "alternativo": "Fellenius",
            "tipo_falla": "Circular"
        }
    elif gsi > 25:
        return {
            "principal": "Fellenius o Bishop con parámetros reducidos",
            "alternativo": "Taylor (Stability Number)",
            "tipo_falla": "Circular"
        }
    else:
        return {
            "principal": "Mohr-Coulomb, Talud Infinito o Culmann",
            "alternativo": "Taylor (φ=0)",
            "tipo_falla": "Superficial plana"
        }

def gsi_a_materiales(gsi):
    """Materiales típicos según rango GSI"""
    if gsi > 65:
        return ["Granito Sano", "Basalto", "Diorita"]
    elif gsi > 40:
        return ["Andesita", "Caliza Sana", "Arenisca", "Granito Fracturado"]
    elif gsi > 25:
        return ["Lutita", "Filita", "Esquisto", "Pizarra", "Caliza Fracturada"]
    else:
        return ["Suelo Residual Granítico", "Suelo Residual Andesítico", 
                "Material Coluvial", "Arcilla Blanda", "Arcilla Compacta",
                "Arena Suelta", "Arena Densa"]

def render_gsi_module():
    """Renderiza el módulo GSI en Streamlit"""
    st.markdown("## 🏔️ Módulo GSI - Clasificación Geomecánica")
    st.markdown("*Basado en Hoek, Carter & Diederichs (2013)*")

    st.markdown("---")

    # Tabs para diferentes formas de calcular GSI
    tab1, tab2, tab3 = st.tabs(["📊 Evaluación Detallada (JCond89 + RQD)", 
                                 "🎯 GSI Directo", 
                                 "📋 Tabla Cruzada Estructura/Superficie"])

    with tab1:
        st.markdown("### Evaluación de Condiciones de Juntas (JCond89)")

        col1, col2, col3 = st.columns(3)

        with col1:
            persistencia = st.selectbox(
                "**Persistencia**", 
                list(PERSISTENCIA_VALS.keys()),
                help="Longitud de las discontinuidades"
            )
            val_persistencia = PERSISTENCIA_VALS[persistencia]
            st.markdown(f"<span style='color:#1f77b4; font-size:24px; font-weight:bold;'>{val_persistencia}</span>", 
                       unsafe_allow_html=True)

        with col2:
            apertura = st.selectbox(
                "**Apertura**", 
                list(APERTURA_VALS.keys()),
                help="Ancho de la apertura de las juntas"
            )
            val_apertura = APERTURA_VALS[apertura]
            st.markdown(f"<span style='color:#1f77b4; font-size:24px; font-weight:bold;'>{val_apertura}</span>", 
                       unsafe_allow_html=True)

        with col3:
            rugosidad = st.selectbox(
                "**Rugosidad**", 
                list(RUGOSIDAD_VALS.keys()),
                help="Rugosidad de la superficie de las juntas"
            )
            val_rugosidad = RUGOSIDAD_VALS[rugosidad]
            st.markdown(f"<span style='color:#1f77b4; font-size:24px; font-weight:bold;'>{val_rugosidad}</span>", 
                       unsafe_allow_html=True)

        col4, col5 = st.columns(2)

        with col4:
            relleno = st.selectbox(
                "**Relleno**", 
                list(RELLENO_VALS.keys()),
                help="Material de relleno en las juntas"
            )
            val_relleno = RELLENO_VALS[relleno]
            st.markdown(f"<span style='color:#1f77b4; font-size:24px; font-weight:bold;'>{val_relleno}</span>", 
                       unsafe_allow_html=True)

        with col5:
            alteracion = st.selectbox(
                "**Alteración**", 
                list(ALTERACION_VALS.keys()),
                help="Grado de alteración de las paredes de las juntas"
            )
            val_alteracion = ALTERACION_VALS[alteracion]
            st.markdown(f"<span style='color:#1f77b4; font-size:24px; font-weight:bold;'>{val_alteracion}</span>", 
                       unsafe_allow_html=True)

        jcond89 = calcular_jcond89(val_persistencia, val_apertura, val_rugosidad, val_relleno, val_alteracion)

        st.markdown("---")
        st.markdown("### Cálculo del RQD (Rock Quality Designation)")

        metodo_rqd = st.radio("Método de cálculo de RQD:", 
                               ["De mapeo de superficie (λ)", "De conteo volumétrico (Jv)"],
                               horizontal=True)

        if metodo_rqd == "De mapeo de superficie (λ)":
            lambda_val = st.slider("Frecuencia de juntas λ (juntas/m)", 0.0, 50.0, 10.0, 0.5)
            rqd = calcular_rqd_lambda(lambda_val)
            st.info(f"**Fórmula:** RQD = 100·e^(-0.1λ)·(0.1λ + 1)")
        else:
            jv = st.slider("Conteo volumétrico Jv (juntas/m³)", 0.0, 35.0, 10.0, 0.5)
            rqd = calcular_rqd_jv(jv)
            st.info(f"**Fórmula:** RQD = 115 - 3.3·Jv")

        st.markdown(f"**RQD calculado:** <span style='color:#2ca02c; font-size:28px; font-weight:bold;'>{rqd:.1f}%</span>", 
                   unsafe_allow_html=True)

        gsi = calcular_gsi(jcond89, rqd)

    with tab2:
        st.markdown("### Ingreso Directo de GSI")
        st.info("Use esta opción si ya conoce el valor de GSI o desea probar diferentes escenarios.")

        gsi_directo = st.slider("GSI", 10, 90, 50, 1)
        jcond89 = None
        rqd = None
        gsi = gsi_directo

    with tab3:
        st.markdown("### Tabla Cruzada: Estructura de la Roca vs Superficie de Juntas")
        st.info("Seleccione la combinación que mejor describa su macizo rocoso.")

        estructura = st.selectbox("**Estructura de la Roca**", list(ESTRUCTURA_ROCA.keys()))
        superficie = st.selectbox("**Condición de Superficie de Juntas**", list(SUPERFICIE_JUNTAS.keys()))

        # Extraer rangos y promediar
        rango_est = ESTRUCTURA_ROCA[estructura]["rango_gsi"]
        rango_sup = SUPERFICIE_JUNTAS[superficie]["rango_gsi"]

        # Calcular promedio de los rangos
        def promedio_rango(rango_str):
            parts = rango_str.split("-")
            return (int(parts[0]) + int(parts[1])) / 2

        gsi_est = promedio_rango(rango_est)
        gsi_sup = promedio_rango(rango_sup)
        gsi = (gsi_est + gsi_sup) / 2

        st.markdown(f"**GSI estimado:** <span style='color:#2ca02c; font-size:28px; font-weight:bold;'>{gsi:.0f}</span>", 
                   unsafe_allow_html=True)

        jcond89 = None
        rqd = None

    # Resultados GSI
    st.markdown("---")
    st.markdown("## 📊 Resultados de Clasificación GSI")

    col_res1, col_res2, col_res3 = st.columns(3)

    with col_res1:
        st.metric("GSI", f"{gsi:.1f}")

    with col_res2:
        clasificacion = gsi_a_clasificacion(gsi)
        st.metric("Clasificación", clasificacion)

    with col_res3:
        recomendacion = gsi_a_metodo(gsi)
        st.metric("Método Principal", recomendacion["principal"])

    # Barra de color para GSI
    st.markdown("### Indicador Visual de GSI")

    # Crear barra de progreso con color según rango
    if gsi > 65:
        color = "🟢"
        bar_color = "green"
    elif gsi > 40:
        color = "🟡"
        bar_color = "orange"
    elif gsi > 25:
        color = "🟠"
        bar_color = "darkorange"
    else:
        color = "🔴"
        bar_color = "red"

    progress = (gsi - 10) / 80
    st.progress(progress, text=f"{color} GSI = {gsi:.1f} / 90")

    # Recomendaciones detalladas
    st.markdown("---")
    st.markdown("### 🎯 Recomendaciones de Análisis")

    rec = gsi_a_metodo(gsi)

    col_rec1, col_rec2 = st.columns(2)

    with col_rec1:
        st.markdown("**Método Principal Recomendado:**")
        st.success(f"📌 {rec['principal']}")
        st.markdown(f"**Tipo de Falla:** {rec['tipo_falla']}")

    with col_rec2:
        st.markdown("**Método Alternativo:**")
        st.info(f"📌 {rec['alternativo']}")

    # Materiales sugeridos
    st.markdown("### 🪨 Materiales Típicos para este Rango GSI")
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
