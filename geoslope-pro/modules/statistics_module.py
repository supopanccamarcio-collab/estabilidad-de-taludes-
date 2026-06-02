"""
Módulo de Análisis Estadístico
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy import stats
from modules.methods_module import (
    metodo_talud_infinito, metodo_culmann, metodo_fellenius,
    metodo_bishop, metodo_taylor
)

def monte_carlo_simulation(metodo, material, geometry, n_simulations=1000, 
                           std_c=0.15, std_phi=0.10, std_gamma=0.05):
    """
    Simulación Monte Carlo para análisis de probabilidad
    """
    c_mean = material.get("c_prime", 50)
    phi_mean = material.get("phi_prime", 20)
    gamma_mean = material.get("gamma", 19)

    # Generar muestras aleatorias
    c_samples = np.random.normal(c_mean, c_mean * std_c, n_simulations)
    c_samples = np.maximum(c_samples, 0)  # No negativos

    phi_samples = np.random.normal(phi_mean, phi_mean * std_phi, n_simulations)
    phi_samples = np.maximum(phi_samples, 0)
    phi_samples = np.minimum(phi_samples, 60)

    gamma_samples = np.random.normal(gamma_mean, gamma_mean * std_gamma, n_simulations)
    gamma_samples = np.maximum(gamma_samples, 10)

    FS_samples = []

    H = geometry.get("H", 10)
    beta = geometry.get("beta", 30)
    condicion = geometry.get("condicion", "seco")
    gamma_sat = material.get("gamma_sat", None)
    hw = geometry.get("hw", 0)
    ru = geometry.get("ru", 0)
    cu = material.get("cu", None)

    for i in range(n_simulations):
        mat_sim = material.copy()
        mat_sim["c_prime"] = c_samples[i]
        mat_sim["phi_prime"] = phi_samples[i]
        mat_sim["gamma"] = gamma_samples[i]

        if metodo == "Talud Infinito":
            res = metodo_talud_infinito(c_samples[i], phi_samples[i], gamma_samples[i], 
                                       H, beta, gamma_sat, hw, condicion)
        elif metodo == "Culmann":
            res = metodo_culmann(c_samples[i], phi_samples[i], gamma_samples[i], H, beta)
        elif metodo == "Fellenius":
            res = metodo_fellenius(c_samples[i], phi_samples[i], gamma_samples[i], H, beta, ru=ru)
        elif metodo == "Bishop Simplificado":
            res = metodo_bishop(c_samples[i], phi_samples[i], gamma_samples[i], H, beta, ru=ru)
        elif metodo == "Taylor":
            c_u = cu if cu is not None else c_samples[i]
            res = metodo_taylor(c_u, gamma_samples[i], H, beta)
        else:
            res = {"FS": None}

        fs = res.get("FS", None)
        if fs is not None and not np.isnan(fs) and not np.isinf(fs):
            FS_samples.append(fs)

    return np.array(FS_samples)

def render_statistics_module():
    """Renderiza el módulo de análisis estadístico"""
    st.markdown("## 📊 Análisis Estadístico y Probabilístico")
    st.markdown("*Simulación Monte Carlo y Análisis de Confiabilidad*")

    material = st.session_state.get("material_props", None)
    geometry = st.session_state.get("geometry", None)
    metodo = st.session_state.get("metodo_seleccionado", "Talud Infinito")

    if material is None or geometry is None:
        st.warning("⚠️ Primero seleccione material y defina geometría")
        return

    # Configuración de Monte Carlo
    st.markdown("### ⚙️ Configuración de Simulación")

    col1, col2, col3 = st.columns(3)

    with col1:
        n_simulations = st.selectbox("N° de simulaciones", [100, 500, 1000, 5000, 10000], index=2)

    with col2:
        std_c_pct = st.slider("Incertidumbre c' (±%)", 0, 50, 15, 5)
        std_phi_pct = st.slider("Incertidumbre φ' (±%)", 0, 50, 10, 5)

    with col3:
        std_gamma_pct = st.slider("Incertidumbre γ (±%)", 0, 50, 5, 5)
        FS_deseado = geometry.get("FS_deseado", 1.5)

    # Ejecutar simulación
    if st.button("🚀 Ejecutar Simulación Monte Carlo", type="primary"):
        with st.spinner("Ejecutando simulación..."):
            FS_samples = monte_carlo_simulation(
                metodo, material, geometry, n_simulations,
                std_c=std_c_pct/100, std_phi=std_phi_pct/100, std_gamma=std_gamma_pct/100
            )

        if len(FS_samples) == 0:
            st.error("No se generaron resultados válidos. Verifique los parámetros.")
            return

        # Estadísticas
        mu_FS = np.mean(FS_samples)
        sigma_FS = np.std(FS_samples)
        min_FS = np.min(FS_samples)
        max_FS = np.max(FS_samples)
        median_FS = np.median(FS_samples)

        # Probabilidad de falla
        P_falla = np.sum(FS_samples < 1.0) / len(FS_samples) * 100
        P_precario = np.sum((FS_samples >= 1.0) & (FS_samples < FS_deseado)) / len(FS_samples) * 100
        P_estable = np.sum(FS_samples >= FS_deseado) / len(FS_samples) * 100

        # Índice de confiabilidad
        beta_reliability = (mu_FS - 1.0) / sigma_FS if sigma_FS > 0 else 999

        # Mostrar resultados estadísticos
        st.markdown("---")
        st.markdown("### 📈 Resultados Estadísticos")

        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

        with col_stat1:
            st.metric("Media FS", f"{mu_FS:.3f}")
            st.metric("Mediana FS", f"{median_FS:.3f}")

        with col_stat2:
            st.metric("σ FS", f"{sigma_FS:.3f}")
            st.metric("Min/Max", f"{min_FS:.3f} / {max_FS:.3f}")

        with col_stat3:
            st.metric("P(Falla)", f"{P_falla:.1f}%", delta=f"FS < 1.0")
            st.metric("P(Precario)", f"{P_precario:.1f}%", delta=f"1.0 ≤ FS < {FS_deseado}")

        with col_stat4:
            st.metric("P(Estable)", f"{P_estable:.1f}%", delta=f"FS ≥ {FS_deseado}")

            # Color según confiabilidad
            if beta_reliability >= 2.5:
                conf_color = "green"
                conf_text = "ALTA"
            elif beta_reliability >= 1.5:
                conf_color = "orange"
                conf_text = "MEDIA"
            else:
                conf_color = "red"
                conf_text = "BAJA"

            st.markdown(f"**Índice de Confiabilidad β:**")
            st.markdown(f"<h2 style='color:{conf_color};'>{beta_reliability:.2f}</h2>", 
                       unsafe_allow_html=True)
            st.caption(f"Confiabilidad: {conf_text}")

        # Histograma
        st.markdown("---")
        st.markdown("### 📊 Histograma de Distribución de FS")

        fig, ax = plt.subplots(figsize=(12, 6))

        n, bins, patches = ax.hist(FS_samples, bins=50, density=True, alpha=0.7, color='steelblue', 
                                    edgecolor='black', linewidth=0.5)

        # Ajuste de distribución normal
        x_norm = np.linspace(min_FS, max_FS, 100)
        y_norm = stats.norm.pdf(x_norm, mu_FS, sigma_FS)
        ax.plot(x_norm, y_norm, 'r-', linewidth=2, label='Distribución Normal')

        # Líneas de referencia
        ax.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='FS = 1.0 (Crítico)')
        ax.axvline(x=FS_deseado, color='green', linestyle='--', linewidth=2, label=f'FS = {FS_deseado} (Deseado)')
        ax.axvline(x=mu_FS, color='blue', linestyle='-', linewidth=2, label=f'μ = {mu_FS:.3f}')

        # Zonas
        ax.axvspan(0, 1.0, alpha=0.2, color='red', label='Zona Inestable')
        ax.axvspan(1.0, FS_deseado, alpha=0.2, color='yellow', label='Zona Precaria')
        ax.axvspan(FS_deseado, max_FS * 1.2, alpha=0.2, color='green', label='Zona Estable')

        ax.set_xlabel("Factor de Seguridad FS", fontsize=12)
        ax.set_ylabel("Densidad de Probabilidad", fontsize=12)
        ax.set_title(f"Distribución de FS - {metodo} (n={n_simulations})", fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig)

        # CDF (Función de Distribución Acumulada)
        st.markdown("### 📈 Función de Distribución Acumulada (CDF)")

        fig2, ax2 = plt.subplots(figsize=(12, 6))

        sorted_FS = np.sort(FS_samples)
        cdf = np.arange(1, len(sorted_FS) + 1) / len(sorted_FS)

        ax2.plot(sorted_FS, cdf * 100, 'b-', linewidth=2)
        ax2.axvline(x=1.0, color='red', linestyle='--', linewidth=2)
        ax2.axvline(x=FS_deseado, color='green', linestyle='--', linewidth=2)
        ax2.axhline(y=P_falla, color='red', linestyle=':', linewidth=1, alpha=0.7)

        ax2.set_xlabel("Factor de Seguridad FS", fontsize=12)
        ax2.set_ylabel("Probabilidad Acumulada (%)", fontsize=12)
        ax2.set_title("CDF - Probabilidad de que FS ≤ valor", fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig2)

        # Boxplot
        st.markdown("### 📦 Boxplot de FS")

        fig3, ax3 = plt.subplots(figsize=(8, 6))

        bp = ax3.boxplot([FS_samples], labels=[metodo], patch_artist=True,
                         boxprops=dict(facecolor='lightblue', color='black'),
                         medianprops=dict(color='red', linewidth=2),
                         whiskerprops=dict(color='black', linewidth=1.5),
                         capprops=dict(color='black', linewidth=1.5))

        ax3.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='FS = 1.0')
        ax3.axhline(y=FS_deseado, color='green', linestyle='--', linewidth=2, label=f'FS = {FS_deseado}')
        ax3.set_ylabel("Factor de Seguridad FS", fontsize=12)
        ax3.set_title("Diagrama de Caja - FS", fontsize=14, fontweight='bold')
        ax3.legend(loc='best')
        ax3.grid(True, alpha=0.3, axis='y')

        st.pyplot(fig3)

        # Guardar resultados
        st.session_state["mc_results"] = {
            "FS_samples": FS_samples,
            "mu": mu_FS,
            "sigma": sigma_FS,
            "P_falla": P_falla,
            "P_precario": P_precario,
            "P_estable": P_estable,
            "beta": beta_reliability
        }

def render_tornado_diagram():
    """Renderiza diagrama de tornado (análisis de sensibilidad paramétrica)"""
    st.markdown("## 🌪️ Diagrama de Tornado")
    st.markdown("*Impacto de la variación ±20% de cada parámetro sobre el FS*")

    material = st.session_state.get("material_props", None)
    geometry = st.session_state.get("geometry", None)
    metodo = st.session_state.get("metodo_seleccionado", "Talud Infinito")

    if material is None or geometry is None:
        st.warning("⚠️ Primero seleccione material y defina geometría")
        return

    # Parámetros a evaluar
    params = ["c_prime", "phi_prime", "gamma", "beta"]
    param_labels = {"c_prime": "c'", "phi_prime": "φ'", "gamma": "γ", "beta": "β"}

    base_FS = None
    # Calcular FS base
    if metodo == "Talud Infinito":
        res = metodo_talud_infinito(material["c_prime"], material["phi_prime"], 
                                     material["gamma"], geometry["H"], geometry["beta"])
        base_FS = res.get("FS", 1.0)

    if base_FS is None:
        st.error("No se pudo calcular el FS base")
        return

    results = []

    for param in params:
        if param in material:
            base_val = material[param]
        elif param in geometry:
            base_val = geometry[param]
        else:
            continue

        # -20%
        val_low = base_val * 0.8
        res_low = ejecutar_metodo_sensibilidad(metodo, material, geometry, param, val_low)
        fs_low = res_low.get("FS", base_FS)

        # +20%
        val_high = base_val * 1.2
        res_high = ejecutar_metodo_sensibilidad(metodo, material, geometry, param, val_high)
        fs_high = res_high.get("FS", base_FS)

        impact = max(abs(fs_low - base_FS), abs(fs_high - base_FS))

        results.append({
            "parametro": param_labels[param],
            "fs_low": fs_low,
            "fs_base": base_FS,
            "fs_high": fs_high,
            "impacto": impact
        })

    # Ordenar por impacto
    results.sort(key=lambda x: x["impacto"], reverse=True)

    # Gráfico de tornado
    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = np.arange(len(results))

    # Barras horizontales
    for i, r in enumerate(results):
        # Barra desde fs_low a fs_high
        ax.barh(i, r["fs_high"] - r["fs_low"], left=r["fs_low"], 
                height=0.6, color='steelblue', alpha=0.7, edgecolor='black')

        # Línea del valor base
        ax.plot([r["fs_base"], r["fs_base"]], [i-0.3, i+0.3], 'r-', linewidth=3)

        # Etiquetas
        ax.text(r["fs_low"], i, f'{r["fs_low"]:.2f}', ha='right', va='center', fontsize=9)
        ax.text(r["fs_high"], i, f'{r["fs_high"]:.2f}', ha='left', va='center', fontsize=9)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([r["parametro"] for r in results])
    ax.set_xlabel("Factor de Seguridad FS", fontsize=12)
    ax.set_title("Diagrama de Tornado - Impacto ±20%", fontsize=14, fontweight='bold')
    ax.axvline(x=base_FS, color='red', linestyle='--', linewidth=1, alpha=0.5, label=f'FS base = {base_FS:.2f}')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='x')

    st.pyplot(fig)

    # Tabla
    st.markdown("### 📋 Tabla de Impacto")

    import pandas as pd
    df = pd.DataFrame([{
        "Parámetro": r["parametro"],
        "FS (-20%)": f"{r['fs_low']:.3f}",
        "FS (Base)": f"{r['fs_base']:.3f}",
        "FS (+20%)": f"{r['fs_high']:.3f}",
        "Impacto": f"{r['impacto']:.3f}",
        "Clasificación": "ALTO" if r["impacto"] > 0.3 else "MEDIO" if r["impacto"] > 0.15 else "BAJO"
    } for r in results])

    st.dataframe(df, hide_index=True, use_container_width=True)

def ejecutar_metodo_sensibilidad(metodo, material, geometry, parametro, valor):
    """Ejecuta método con un parámetro modificado"""
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
    H = geo_copy.get("H", 10)
    beta = geo_copy.get("beta", 30)
    condicion = geo_copy.get("condicion", "seco")
    hw = geo_copy.get("hw", 0)
    ru = geo_copy.get("ru", 0)
    cu = mat_copy.get("cu", None)

    if metodo == "Talud Infinito":
        return metodo_talud_infinito(c_prime, phi_prime, gamma, H, beta, gamma_sat, hw, condicion)
    elif metodo == "Culmann":
        return metodo_culmann(c_prime, phi_prime, gamma, H, beta)
    elif metodo == "Fellenius":
        return metodo_fellenius(c_prime, phi_prime, gamma, H, beta, ru=ru)
    elif metodo == "Bishop Simplificado":
        return metodo_bishop(c_prime, phi_prime, gamma, H, beta, ru=ru)
    elif metodo == "Taylor":
        c_u = cu if cu is not None else c_prime
        return metodo_taylor(c_u, gamma, H, beta)
    else:
        return {"FS": None}
