"""
Módulo de Materiales - Base de Datos Geotécnicas
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import json
import os
import streamlit as st
import numpy as np

# ============================================================
# RUTA ROBUSTA A materials.json
# Funciona tanto en local como en Streamlit Cloud
# ============================================================
def get_data_path():
    """Obtiene la ruta absoluta a materials.json de forma robusta"""
    # Opción 1: Desde el directorio de este archivo (modules/)
    module_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(module_dir, "..", "data", "materials.json")

    if os.path.exists(data_path):
        return os.path.abspath(data_path)

    # Opción 2: Desde el directorio de trabajo (Streamlit Cloud)
    cwd = os.getcwd()
    data_path = os.path.join(cwd, "data", "materials.json")

    if os.path.exists(data_path):
        return os.path.abspath(data_path)

    # Opción 3: Buscar en subdirectorios (por si app.py está en subcarpeta)
    for root, dirs, files in os.walk(cwd):
        if "materials.json" in files:
            return os.path.join(root, "materials.json")

    # Fallback: devolver la ruta esperada aunque no exista
    return os.path.abspath(data_path)

# Usar la ruta robusta
DATA_PATH = get_data_path()

def load_materials():
    """Carga la base de datos de materiales"""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error cargando materials.json: {e}")
        st.error(f"Ruta buscada: {DATA_PATH}")
        st.error(f"Directorio actual: {os.getcwd()}")
        return {}

def get_all_materials():
    """Obtiene todos los materiales en una lista plana"""
    data = load_materials()
    all_materials = []
    for category, materials in data.items():
        for name, props in materials.items():
            props["name"] = name
            props["category_key"] = category
            all_materials.append(props)
    return all_materials

def get_material_by_name(name):
    """Obtiene un material por su nombre"""
    all_materials = get_all_materials()
    for mat in all_materials:
        if mat["name"] == name:
            return mat
    return None

def get_materials_by_category(category_key):
    """Obtiene materiales por categoría"""
    data = load_materials()
    return data.get(category_key, {})

def render_materials_sidebar():
    """Renderiza el panel de materiales en la barra lateral"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🪨 Material Seleccionado")

    data = load_materials()

    if not data:
        st.sidebar.error("No se pudieron cargar los materiales")
        return None

    # Selector de categoría
    categories = {
        "rocas_igneas": "🔥 Rocas Ígneas",
        "rocas_sedimentarias": "🌊 Rocas Sedimentarias",
        "rocas_metamorficas": "⚡ Rocas Metamórficas",
        "suelos": "🌍 Suelos y Materiales Sueltos"
    }

    selected_category = st.sidebar.selectbox(
        "Categoría",
        list(categories.keys()),
        format_func=lambda x: categories[x]
    )

    # Selector de material
    materials_in_cat = data.get(selected_category, {})
    selected_material_name = st.sidebar.selectbox(
        "Material",
        list(materials_in_cat.keys())
    )

    material = materials_in_cat[selected_material_name]
    material["name"] = selected_material_name
    material["category_key"] = selected_category

    # Mostrar propiedades en sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{selected_material_name}**")
    st.sidebar.caption(material.get("description", ""))

    # Propiedades principales con sliders dinámicos
    st.sidebar.markdown("### ⚙️ Propiedades Principales")

    # Cohesión
    c_min = material["c_prime"]["min"]
    c_max = material["c_prime"]["max"]
    c_typ = material["c_prime"]["typical"]
    c_prime = st.sidebar.slider(
        "c' (kPa)", 
        float(c_min), float(c_max), float(c_typ), 
        step=1.0,
        help="Cohesión efectiva"
    )

    # Ángulo de fricción
    phi_min = material["phi_prime"]["min"]
    phi_max = material["phi_prime"]["max"]
    phi_typ = material["phi_prime"]["typical"]
    phi_prime = st.sidebar.slider(
        "φ' (°)", 
        float(phi_min), float(phi_max), float(phi_typ), 
        step=0.5,
        help="Ángulo de fricción interna efectiva"
    )

    # Peso unitario
    gamma_min = material["gamma"]["min"]
    gamma_max = material["gamma"]["max"]
    gamma_typ = material["gamma"]["typical"]
    gamma = st.sidebar.slider(
        "γ (kN/m³)", 
        float(gamma_min), float(gamma_max), float(gamma_typ), 
        step=0.1,
        help="Peso unitario del material"
    )

    # Peso unitario saturado (si aplica)
    gamma_sat = None
    if "gamma_sat" in material:
        gs_min = material["gamma_sat"]["min"]
        gs_max = material["gamma_sat"]["max"]
        gs_typ = material["gamma_sat"]["typical"]
        gamma_sat = st.sidebar.slider(
            "γ_sat (kN/m³)", 
            float(gs_min), float(gs_max), float(gs_typ), 
            step=0.1,
            help="Peso unitario saturado"
        )

    # Parámetros adicionales para rocas (Hoek-Brown)
    sigma_ci = None
    mi = None
    gsi = None

    if "sigma_ci" in material:
        st.sidebar.markdown("### 🪨 Parámetros Hoek-Brown")

        sc_min = material["sigma_ci"]["min"]
        sc_max = material["sigma_ci"]["max"]
        sc_typ = material["sigma_ci"]["typical"]
        sigma_ci = st.sidebar.slider(
            "σci (MPa)", 
            float(sc_min), float(sc_max), float(sc_typ), 
            step=1.0,
            help="Resistencia a compresión simple del intacto"
        )

        mi = material["mi"]["value"]
        st.sidebar.markdown(f"**mi:** {mi}")

        if "gsi_typical" in material:
            gsi_min = material["gsi_typical"]["min"]
            gsi_max = material["gsi_typical"]["max"]
            gsi_typ = material["gsi_typical"]["typical"]

            # Si hay GSI calculado, usarlo como default
            default_gsi = st.session_state.get("gsi_calculado", gsi_typ)
            default_gsi = max(gsi_min, min(gsi_max, default_gsi))

            gsi = st.sidebar.slider(
                "GSI", 
                float(gsi_min), float(gsi_max), float(default_gsi), 
                step=1.0,
                help="Geological Strength Index"
            )

    # Cohesión no drenada (para arcillas)
    cu = None
    if "cu" in material:
        cu_min = material["cu"]["min"]
        cu_max = material["cu"]["max"]
        cu_typ = material["cu"]["typical"]
        cu = st.sidebar.slider(
            "cu (kPa)", 
            float(cu_min), float(cu_max), float(cu_typ), 
            step=1.0,
            help="Cohesión no drenada (para φ=0)"
        )

    # Guardar en session state
    material_props = {
        "name": selected_material_name,
        "category": selected_category,
        "c_prime": c_prime,
        "phi_prime": phi_prime,
        "gamma": gamma,
        "gamma_sat": gamma_sat,
        "sigma_ci": sigma_ci,
        "mi": mi,
        "gsi": gsi,
        "cu": cu,
        "description": material.get("description", "")
    }

    st.session_state["material_props"] = material_props

    # Mostrar tabla de propiedades
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Resumen de Propiedades")

    import pandas as pd
    props_df = {
        "Parámetro": ["c'", "φ'", "γ"],
        "Valor": [f"{c_prime:.1f} kPa", f"{phi_prime:.1f}°", f"{gamma:.1f} kN/m³"],
        "Rango": [f"{c_min}-{c_max}", f"{phi_min}-{phi_max}", f"{gamma_min}-{gamma_max}"]
    }

    if gamma_sat is not None:
        props_df["Parámetro"].append("γ_sat")
        props_df["Valor"].append(f"{gamma_sat:.1f} kN/m³")
        props_df["Rango"].append(f"{gs_min}-{gs_max}")

    if sigma_ci is not None:
        props_df["Parámetro"].append("σci")
        props_df["Valor"].append(f"{sigma_ci:.1f} MPa")
        props_df["Rango"].append(f"{sc_min}-{sc_max}")

    if mi is not None:
        props_df["Parámetro"].append("mi")
        props_df["Valor"].append(f"{mi}")
        props_df["Rango"].append("-")

    if gsi is not None:
        props_df["Parámetro"].append("GSI")
        props_df["Valor"].append(f"{gsi:.0f}")
        props_df["Rango"].append(f"{gsi_min}-{gsi_max}")

    if cu is not None:
        props_df["Parámetro"].append("cu")
        props_df["Valor"].append(f"{cu:.1f} kPa")
        props_df["Rango"].append(f"{cu_min}-{cu_max}")

    df = pd.DataFrame(props_df)
    st.sidebar.dataframe(df, hide_index=True, use_container_width=True)

    return material_props

def render_materials_table():
    """Renderiza tabla completa de materiales en el panel principal"""
    st.markdown("## 📚 Base de Datos de Materiales")

    data = load_materials()

    tabs = st.tabs(["🔥 Rocas Ígneas", "🌊 Rocas Sedimentarias", "⚡ Rocas Metamórficas", "🌍 Suelos"])

    tab_names = ["rocas_igneas", "rocas_sedimentarias", "rocas_metamorficas", "suelos"]

    for tab, cat_key in zip(tabs, tab_names):
        with tab:
            materials = data.get(cat_key, {})

            rows = []
            for name, props in materials.items():
                row = {"Material": name}
                row["c' (kPa)"] = f"{props['c_prime']['min']}-{props['c_prime']['max']}"
                row["φ' (°)"] = f"{props['phi_prime']['min']}-{props['phi_prime']['max']}"
                row["γ (kN/m³)"] = f"{props['gamma']['min']}-{props['gamma']['max']}"
                if "sigma_ci" in props:
                    row["σci (MPa)"] = f"{props['sigma_ci']['min']}-{props['sigma_ci']['max']}"
                    row["mi"] = props["mi"]["value"]
                    row["GSI"] = f"{props['gsi_typical']['min']}-{props['gsi_typical']['max']}"
                if "gamma_sat" in props:
                    row["γ_sat (kN/m³)"] = f"{props['gamma_sat']['min']}-{props['gamma_sat']['max']}"
                if "cu" in props:
                    row["cu (kPa)"] = f"{props['cu']['min']}-{props['cu']['max']}"
                rows.append(row)

            import pandas as pd
            df = pd.DataFrame(rows)
            st.dataframe(df, hide_index=True, use_container_width=True)
