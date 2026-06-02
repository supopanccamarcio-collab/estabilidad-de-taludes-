"""
Módulo de Análisis de Sensibilidad
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from modules.methods_module import (
    metodo_talud_infinito, metodo_culmann, metodo_fellenius, 
    metodo_bishop, metodo_taylor, metodo_hoek_brown
)

def ejecutar_metodo_sensibilidad(metodo, material, geometry, parametro, valor):
    """Ejecuta método con un parámetro modificado para sensibilidad"""
    mat_copy = material.copy()
    geo_copy = geometry.copy()

    if parametro in mat_copy:
        mat_copy[parametro] = valor
    elif parametro in geo_copy:
        geo_copy[parametro] = valor

    c_prime = mat_copy.get("c_prime", 0)
    phi_prime = mat_copy.get("phi_prime", 0)
    gamma = mat_copy.get("gamma", 19)
    gamma_sat = mat_copy.get("gamma_sat", None)
    sigma_ci = mat_copy.get("sigma_ci", None)
    mi = mat_copy.get("mi", None)
    gsi = mat_copy.get("gsi", None)
    cu = mat_copy.get("cu", None)

    H = geo_copy.get("H", 10)
    beta = geo_copy.get("beta", 30)
    condicion = geo_copy.get("condicion", "seco")
    hw = geo_copy.get("hw", 0)
    ru = geo_copy.get("ru", 0)

    if metodo == "Talud Infinito":
        return metodo_talud_infinito(c_prime, phi_prime, gamma, H, beta, gamma_sat, hw, condicion)
    elif metodo == "Culmann":
        return metodo_culmann(c_prime, phi_prime, gamma, H, beta)
    elif metodo == "Fellenius":
        return metodo_fellenius(c_prime, phi_prime, gamma, H, beta, ru=ru)
    elif metodo == "Bishop Simplificado":
        return metodo_bishop(c_prime, phi_prime, gamma, H, beta, ru=ru)
    elif metodo == "Taylor":
        if cu is None:
            cu = c_prime
        return metodo_taylor(cu, gamma, H, beta)
    elif metodo == "Hoek-Brown":
        if sigma_ci is None or mi is None or gsi is None:
            return {"FS": None}
        return metodo_hoek_brown(sigma_ci, mi, gsi, H=H, beta=beta)
    else:
        return {"FS": None}

def render_sensitivity_module():
    """Renderiza el módulo de análisis de sensibilidad"""
    st.markdown("## 📈 Análisis de Sensibilidad")
    st.markdown("*Evaluación paramétrica del Factor de Seguridad*")

    material = st.session_state.get("material_props", None)
    geometry = st.session_state.get("geometry", None)
    metodo = st.session_state.get("metodo_seleccionado", "Talud Infinito")

    if material is None or geometry is None:
        st.warning("⚠️ Primero seleccione material y defina geometría")
        return

    # Parámetros para sensibilidad
    st.markdown("### ⚙️ Configuración del Análisis")

    col1, col2 = st.columns(2)

    with col1:
        parametro_x = st.selectbox(
            "Parámetro a variar (Eje X):",
            ["H", "beta", "c_prime", "phi_prime", "gamma"],
            format_func=lambda x: {
                "H": "Altura del talud H",
                "beta": "Ángulo del talud β",
                "c_prime": "Cohesión c'",
                "phi_prime": "Ángulo de fricción φ'",
                "gamma": "Peso unitario γ"
            }[x]
        )

    with col2:
        # Rango y frecuencia
        if parametro_x == "H":
            rango_min = st.number_input("Valor mínimo", 1.0, 100.0, 5.0, 0.5)
            rango_max = st.number_input("Valor máximo", 1.0, 100.0, 20.0, 0.5)
            frecuencia = st.selectbox("Frecuencia", [0.1, 0.5, 1.0, 2.0], format_func=lambda x: f"Cada {x} m")
        elif parametro_x == "beta":
            rango_min = st.number_input("Valor mínimo", 5.0, 85.0, 15.0, 0.5)
            rango_max = st.number_input("Valor máximo", 5.0, 85.0, 60.0, 0.5)
            frecuencia = st.selectbox("Frecuencia", [0.5, 1.0, 2.0, 5.0], format_func=lambda x: f"Cada {x}°")
        elif parametro_x == "c_prime":
            rango_min = st.number_input("Valor mínimo", 0.0, 5000.0, 10.0, 1.0)
            rango_max = st.number_input("Valor máximo", 0.0, 5000.0, 200.0, 1.0)
            frecuencia = st.number_input("Frecuencia", 1.0, 100.0, 5.0, 1.0)
        elif parametro_x == "phi_prime":
            rango_min = st.number_input("Valor mínimo", 0.0, 60.0, 10.0, 0.5)
            rango_max = st.number_input("Valor máximo", 0.0, 60.0, 40.0, 0.5)
            frecuencia = st.selectbox("Frecuencia", [0.5, 1.0, 2.0], format_func=lambda x: f"Cada {x}°")
        else:  # gamma
            rango_min = st.number_input("Valor mínimo", 10.0, 30.0, 15.0, 0.1)
            rango_max = st.number_input("Valor máximo", 10.0, 30.0, 25.0, 0.1)
            frecuencia = st.selectbox("Frecuencia", [0.1, 0.5, 1.0], format_func=lambda x: f"Cada {x} kN/m³")

    # Generar vector de valores
    valores = np.arange(rango_min, rango_max + frecuencia/2, frecuencia)

    # Calcular FS para cada valor
    FS_vals = []
    for val in valores:
        res = ejecutar_metodo_sensibilidad(metodo, material, geometry, parametro_x, val)
        FS_vals.append(res.get("FS", None))

    # Filtrar valores None
    valid_pairs = [(v, fs) for v, fs in zip(valores, FS_vals) if fs is not None]

    if not valid_pairs:
        st.error("No se pudieron calcular valores de FS para el rango seleccionado")
        return

    valores_validos, FS_validos = zip(*valid_pairs)

    # Gráfico de sensibilidad
    st.markdown("---")
    st.markdown("### 📊 Gráfico de Sensibilidad")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Línea de FS
    ax.plot(valores_validos, FS_validos, 'b-', linewidth=2.5, marker='o', markersize=6, label=f'FS - {metodo}')

    # Líneas de referencia
    FS_deseado = geometry.get("FS_deseado", 1.5)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='FS = 1.0 (Crítico)')
    ax.axhline(y=FS_deseado, color='green', linestyle='--', linewidth=2, label=f'FS = {FS_deseado} (Deseado)')

    # Zonas de color
    ax.fill_between(valores_validos, 0, 1.0, alpha=0.2, color='red', label='Zona Inestable')
    ax.fill_between(valores_validos, 1.0, FS_deseado, alpha=0.2, color='yellow', label='Zona Precaria')
    ax.fill_between(valores_validos, FS_deseado, max(FS_validos) * 1.2, alpha=0.2, color='green', label='Zona Estable')

    # Etiquetas
    param_labels = {
        "H": "Altura H (m)",
        "beta": "Ángulo β (°)",
        "c_prime": "Cohesión c' (kPa)",
        "phi_prime": "Ángulo de fricción φ' (°)",
        "gamma": "Peso unitario γ (kN/m³)"
    }

    ax.set_xlabel(param_labels[parametro_x], fontsize=12)
    ax.set_ylabel("Factor de Seguridad FS", fontsize=12)
    ax.set_title(f"Análisis de Sensibilidad - FS vs {param_labels[parametro_x]}", fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(FS_validos) * 1.2)

    st.pyplot(fig)

    # Tabla de resultados
    st.markdown("### 📋 Tabla de Resultados")

    import pandas as pd
    df_data = {
        param_labels[parametro_x]: [f"{v:.2f}" for v in valores_validos],
        "FS": [f"{fs:.3f}" for fs in FS_validos],
        "Estado": ["ESTABLE" if fs >= 1.5 else "PRECARIO" if fs >= 1.0 else "INESTABLE" for fs in FS_validos]
    }
    df = pd.DataFrame(df_data)
    st.dataframe(df, hide_index=True, use_container_width=True)

    # Análisis adicional: múltiples métodos comparados
    st.markdown("---")
    st.markdown("### 🔬 Comparación entre Métodos")

    metodos_comparar = st.multiselect(
        "Métodos a comparar:",
        ["Talud Infinito", "Culmann", "Fellenius", "Bishop Simplificado", "Taylor"],
        default=["Talud Infinito", "Bishop Simplificado"]
    )

    if metodos_comparar and len(metodos_comparar) > 1:
        fig2, ax2 = plt.subplots(figsize=(12, 6))

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for i, met in enumerate(metodos_comparar):
            FS_met = []
            for val in valores_validos:
                res = ejecutar_metodo_sensibilidad(met, material, geometry, parametro_x, val)
                FS_met.append(res.get("FS", None))

            valid_met = [(v, fs) for v, fs in zip(valores_validos, FS_met) if fs is not None]
            if valid_met:
                v_met, fs_met = zip(*valid_met)
                ax2.plot(v_met, fs_met, color=colors[i % len(colors)], 
                        linewidth=2, marker='o', markersize=4, label=met)

        ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax2.axhline(y=FS_deseado, color='green', linestyle='--', linewidth=2, alpha=0.7)
        ax2.set_xlabel(param_labels[parametro_x], fontsize=12)
        ax2.set_ylabel("Factor de Seguridad FS", fontsize=12)
        ax2.set_title("Comparación de Métodos", fontsize=14, fontweight='bold')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig2)
