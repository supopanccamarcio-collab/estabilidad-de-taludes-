"""
Módulo de Métodos de Análisis de Estabilidad
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar, brentq

def metodo_talud_infinito(c_prime, phi_prime, gamma, H, beta, gamma_sat=None, hw=0, condicion="seco"):
    """
    Método del Talud Infinito (Infinite Slope Method)

    Fórmula seca: FS = c'/(γ·H·sinβ·cosβ) + tanφ'/tanβ
    Fórmula saturada: FS = c'/(γsat·H·cos²β·tanβ) + (γ'/γsat)·tanφ'/tanβ
    """
    beta_rad = np.radians(beta)
    phi_rad = np.radians(phi_prime)

    if condicion == "seco":
        # Condición seca
        term1 = c_prime / (gamma * H * np.sin(beta_rad) * np.cos(beta_rad))
        term2 = np.tan(phi_rad) / np.tan(beta_rad)
        FS = term1 + term2
    elif condicion in ["saturado", "parcial"]:
        # Condición con agua
        gamma_w = 9.81  # kN/m³
        if gamma_sat is None:
            gamma_sat = gamma + 2  # aproximación
        gamma_prime = gamma_sat - gamma_w

        term1 = c_prime / (gamma_sat * H * np.cos(beta_rad)**2 * np.tan(beta_rad))
        term2 = (gamma_prime / gamma_sat) * (np.tan(phi_rad) / np.tan(beta_rad))
        FS = term1 + term2
    else:
        # Default a seco
        term1 = c_prime / (gamma * H * np.sin(beta_rad) * np.cos(beta_rad))
        term2 = np.tan(phi_rad) / np.tan(beta_rad)
        FS = term1 + term2

    # Altura crítica
    if beta > phi_prime:
        H_cr = c_prime / (gamma * np.cos(beta_rad)**2 * (np.tan(beta_rad) - np.tan(phi_rad)))
    else:
        H_cr = float('inf')

    return {
        "FS": FS,
        "H_cr": H_cr,
        "term1": term1,
        "term2": term2,
        "metodo": "Talud Infinito",
        "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE"
    }

def metodo_culmann(c_prime, phi_prime, gamma, H, beta):
    """
    Método de Culmann (Talud Finito con Plano de Falla)

    FS = [2c'·sinβ] / [γ·H·sin(β-θ)·sinθ] + tanφ'/tanθ
    Ángulo crítico: θcr = (β + φ')/2
    """
    beta_rad = np.radians(beta)
    phi_rad = np.radians(phi_prime)

    # Ángulo crítico del plano de falla
    theta_cr_rad = (beta_rad + phi_rad) / 2
    theta_cr = np.degrees(theta_cr_rad)

    # Factor de seguridad en el ángulo crítico
    denom = gamma * H * np.sin(beta_rad - theta_cr_rad) * np.sin(theta_cr_rad)
    if denom == 0:
        denom = 1e-10

    term1 = (2 * c_prime * np.sin(beta_rad)) / denom
    term2 = np.tan(phi_rad) / np.tan(theta_cr_rad)
    FS = term1 + term2

    # Altura crítica (FS=1)
    if beta > phi_prime:
        H_cr = (4 * c_prime / gamma) * ((1 - np.cos(beta_rad - phi_rad)) / 
                                          (np.sin(beta_rad) * np.cos(phi_rad)))
    else:
        H_cr = float('inf')

    return {
        "FS": FS,
        "H_cr": H_cr,
        "theta_cr": theta_cr,
        "term1": term1,
        "term2": term2,
        "metodo": "Culmann",
        "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE"
    }

def metodo_fellenius(c_prime, phi_prime, gamma, H, beta, n_slices=10, ru=0):
    """
    Método de Fellenius (Método Ordinario de Dovelas)

    FS = Σ(Wi·sinαi) / Σ[c'·ΔLi + Wi·cosαi·tanφ']
    """
    beta_rad = np.radians(beta)
    phi_rad = np.radians(phi_prime)

    # Asumir superficie de falla circular aproximada
    # Centro del círculo: aproximadamente en la mitad de la base
    base_length = H / np.tan(beta_rad)
    R = np.sqrt((base_length/2)**2 + H**2) * 1.5  # Radio estimado

    # Centro del círculo
    xc = base_length / 2
    yc = R

    # Dividir en dovelas
    x_start = 0
    x_end = base_length
    dx = (x_end - x_start) / n_slices

    sum_num = 0
    sum_den = 0

    for i in range(n_slices):
        x_i = x_start + (i + 0.5) * dx

        # Altura de la dovela en la superficie del talud
        if x_i <= base_length:
            h_surface = H * (x_i / base_length)
        else:
            h_surface = 0

        # Altura de la dovela en la superficie de falla circular
        # Ecuación del círculo: (x-xc)² + (y-yc)² = R²
        # y = yc - sqrt(R² - (x-xc)²)
        dx_circle = x_i - xc
        if R**2 - dx_circle**2 > 0:
            y_circle = yc - np.sqrt(R**2 - dx_circle**2)
        else:
            y_circle = 0

        h_i = max(0, h_surface - y_circle)

        # Peso de la dovela
        W_i = gamma * dx * h_i

        # Ángulo de la base de la dovela
        # dy/dx del círculo
        if abs(dx_circle) > 1e-6 and R**2 - dx_circle**2 > 0:
            dy_dx = dx_circle / np.sqrt(R**2 - dx_circle**2)
            alpha_i = np.arctan(dy_dx)
        else:
            alpha_i = 0

        # Longitud del arco
        dL_i = dx / np.cos(alpha_i) if abs(alpha_i) < np.pi/2 - 0.01 else dx

        # Presión de poros
        u_i = ru * gamma * h_i if ru > 0 else 0

        # Sumar
        sum_num += W_i * np.sin(alpha_i)
        sum_den += c_prime * dL_i + (W_i * np.cos(alpha_i) - u_i * dL_i) * np.tan(phi_rad)

    if sum_den == 0:
        sum_den = 1e-10

    FS = sum_num / sum_den

    return {
        "FS": FS,
        "metodo": "Fellenius",
        "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE",
        "n_slices": n_slices,
        "R": R
    }

def metodo_bishop(c_prime, phi_prime, gamma, H, beta, n_slices=10, ru=0, tol=0.001, max_iter=50):
    """
    Método de Bishop Simplificado (Simplified Bishop Method)

    FS iterativo: FS = Σ(Wi·sinαi) / Σ{[c'·bi + (Wi - ui·bi)·tanφ'] / mαi}
    mαi = cosαi + (sinαi·tanφ')/FS
    """
    beta_rad = np.radians(beta)
    phi_rad = np.radians(phi_prime)

    # Geometría similar a Fellenius
    base_length = H / np.tan(beta_rad)
    R = np.sqrt((base_length/2)**2 + H**2) * 1.5

    xc = base_length / 2
    yc = R

    x_start = 0
    x_end = base_length
    dx = (x_end - x_start) / n_slices

    # Iteración
    FS = 1.5  # Valor inicial

    for iteration in range(max_iter):
        sum_num = 0
        sum_den = 0

        for i in range(n_slices):
            x_i = x_start + (i + 0.5) * dx

            if x_i <= base_length:
                h_surface = H * (x_i / base_length)
            else:
                h_surface = 0

            dx_circle = x_i - xc
            if R**2 - dx_circle**2 > 0:
                y_circle = yc - np.sqrt(R**2 - dx_circle**2)
            else:
                y_circle = 0

            h_i = max(0, h_surface - y_circle)
            W_i = gamma * dx * h_i

            if abs(dx_circle) > 1e-6 and R**2 - dx_circle**2 > 0:
                dy_dx = dx_circle / np.sqrt(R**2 - dx_circle**2)
                alpha_i = np.arctan(dy_dx)
            else:
                alpha_i = 0

            u_i = ru * gamma * h_i if ru > 0 else 0

            # Factor m_alpha
            m_alpha = np.cos(alpha_i) + (np.sin(alpha_i) * np.tan(phi_rad)) / FS
            if m_alpha < 0.1:
                m_alpha = 0.1  # Evitar división por cero

            sum_num += W_i * np.sin(alpha_i)
            sum_den += (c_prime * dx + (W_i - u_i * dx) * np.tan(phi_rad)) / m_alpha

        if sum_den == 0:
            sum_den = 1e-10

        FS_new = sum_num / sum_den

        if abs(FS_new - FS) < tol:
            FS = FS_new
            break

        FS = FS_new

    return {
        "FS": FS,
        "metodo": "Bishop Simplificado",
        "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE",
        "n_slices": n_slices,
        "iterations": iteration + 1,
        "R": R
    }

def metodo_taylor(cu, gamma, H, beta, D=1.0, phi=0):
    """
    Método de Taylor (Stability Number)

    Para φ=0: FS = cu / (γ·H·m)
    m = f(β, D) de tablas de Taylor
    """
    beta_rad = np.radians(beta)

    if phi == 0:
        # Tabla simplificada de Taylor para φ=0
        # Interpolación lineal de valores típicos
        beta_vals = [0, 15, 30, 45, 60, 75, 90]
        m_vals_D1 = [0.146, 0.149, 0.156, 0.172, 0.195, 0.219, 0.261]
        m_vals_Dinf = [0.130, 0.130, 0.132, 0.138, 0.150, 0.165, 0.187]

        # Interpolar según D
        if D <= 1.0:
            m = np.interp(beta, beta_vals, m_vals_D1)
        elif D >= 4.0:
            m = np.interp(beta, beta_vals, m_vals_Dinf)
        else:
            m_D1 = np.interp(beta, beta_vals, m_vals_D1)
            m_Dinf = np.interp(beta, beta_vals, m_vals_Dinf)
            m = m_D1 + (m_Dinf - m_D1) * (D - 1.0) / 3.0

        FS = cu / (gamma * H * m)
        H_cr = cu / (gamma * m)

        return {
            "FS": FS,
            "H_cr": H_cr,
            "m": m,
            "metodo": "Taylor (φ=0)",
            "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE"
        }
    else:
        # Para φ>0, requiere iteración más compleja
        # Simplificación: usar aproximación
        phi_rad = np.radians(phi)
        m_approx = 0.15  # Valor aproximado
        FS = cu / (gamma * H * m_approx)

        return {
            "FS": FS,
            "m": m_approx,
            "metodo": "Taylor (φ>0) - Aproximado",
            "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE",
            "nota": "Para φ>0 se recomienda usar método de Bishop"
        }

def metodo_hoek_brown(sigma_ci, mi, gsi, D=0, H=10, beta=30):
    """
    Criterio de Rotura de Hoek-Brown (2002)

    σ1 = σ3 + σci·(mb·σ3/σci + s)^a
    """
    # Parámetros Hoek-Brown
    mb = mi * np.exp((gsi - 100) / (28 - 14 * D))
    s = np.exp((gsi - 100) / (9 - 3 * D))
    a = 0.5 + (1/6) * (np.exp(-gsi/15) - np.exp(-20/3))

    # Resistencia del macizo (aproximación para taludes)
    # σcm = σci · (mb/4 + s)^(a-1) / [2(1+a)(2+a)] · [mb + 4s - a(mb - 8s)]
    term1 = (mb / 4 + s)**(a - 1)
    term2 = 2 * (1 + a) * (2 + a)
    term3 = mb + 4 * s - a * (mb - 8 * s)

    sigma_cm = sigma_ci * (term1 / term2) * term3

    # Factor de seguridad simplificado
    # FS = σcm / σ1_actuante (aproximado)
    # Para taludes, σ1_actuante ≈ γ·H·sinβ
    beta_rad = np.radians(beta)
    gamma_rock = 25  # kN/m³ aproximado para roca
    sigma1_act = gamma_rock * H * np.sin(beta_rad) / 1000  # Convertir a MPa

    if sigma1_act > 0:
        FS = sigma_cm / sigma1_act
    else:
        FS = 999.0

    return {
        "FS": FS,
        "sigma_cm": sigma_cm,
        "mb": mb,
        "s": s,
        "a": a,
        "metodo": "Hoek-Brown",
        "estado": "ESTABLE" if FS >= 1.5 else "PRECARIO" if FS >= 1.0 else "INESTABLE"
    }

def ejecutar_metodo(metodo, material, geometry):
    """Ejecuta el método de análisis seleccionado"""
    c_prime = material.get("c_prime", 0)
    phi_prime = material.get("phi_prime", 0)
    gamma = material.get("gamma", 19)
    gamma_sat = material.get("gamma_sat", None)
    sigma_ci = material.get("sigma_ci", None)
    mi = material.get("mi", None)
    gsi = material.get("gsi", None)
    cu = material.get("cu", None)

    H = geometry.get("H", 10)
    beta = geometry.get("beta", 30)
    condicion = geometry.get("condicion", "seco")
    hw = geometry.get("hw", 0)
    ru = geometry.get("ru", 0)

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
            cu = c_prime  # Usar c' como aproximación si no hay cu
        return metodo_taylor(cu, gamma, H, beta)

    elif metodo == "Hoek-Brown":
        if sigma_ci is None or mi is None or gsi is None:
            return {
                "FS": None,
                "metodo": "Hoek-Brown",
                "estado": "ERROR",
                "error": "Se requieren parámetros Hoek-Brown (σci, mi, GSI)"
            }
        return metodo_hoek_brown(sigma_ci, mi, gsi, H=H, beta=beta)

    else:
        return {
            "FS": None,
            "metodo": metodo,
            "estado": "ERROR",
            "error": "Método no reconocido"
        }

def render_methods_selector():
    """Renderiza el selector de métodos"""
    st.markdown("## 🔬 Selección del Método de Análisis")

    # Recomendación basada en GSI
    gsi = st.session_state.get("gsi_calculado", 50)
    metodo_recomendado = st.session_state.get("metodo_recomendado", "Bishop Simplificado")

    st.info(f"📌 **Recomendación según GSI = {gsi:.1f}:** {metodo_recomendado}")

    # Lista de métodos disponibles
    metodos_disponibles = [
        "Talud Infinito",
        "Culmann", 
        "Fellenius",
        "Bishop Simplificado",
        "Taylor",
        "Hoek-Brown"
    ]

    # Filtrar según GSI
    if gsi > 65:
        metodos_sugeridos = ["Hoek-Brown", "Bishop Simplificado", "Talud Infinito"]
    elif gsi > 40:
        metodos_sugeridos = ["Bishop Simplificado", "Fellenius", "Talud Infinito"]
    elif gsi > 25:
        metodos_sugeridos = ["Fellenius", "Bishop Simplificado", "Taylor"]
    else:
        metodos_sugeridos = ["Talud Infinito", "Culmann", "Taylor"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Métodos Recomendados")
        for metodo in metodos_sugeridos:
            if st.button(f"🔹 {metodo}", key=f"btn_{metodo}"):
                st.session_state["metodo_seleccionado"] = metodo
                st.rerun()

    with col2:
        st.markdown("### 📋 Todos los Métodos")
        metodo_seleccionado = st.selectbox(
            "Seleccionar método:",
            metodos_disponibles,
            index=metodos_disponibles.index(metodo_recomendado.split(" ")[0]) if any(m in metodo_recomendado for m in metodos_disponibles) else 0
        )

    # Verificar si hay material seleccionado
    material = st.session_state.get("material_props", None)
    geometry = st.session_state.get("geometry", None)

    if material is None:
        st.warning("⚠️ Primero seleccione un material en el panel lateral")
        return None

    if geometry is None:
        st.warning("⚠️ Primero defina la geometría del talud")
        return None

    # Ejecutar análisis
    st.markdown("---")
    st.markdown(f"## 📊 Resultados - {metodo_seleccionado}")

    resultado = ejecutar_metodo(metodo_seleccionado, material, geometry)

    # Mostrar resultados
    col_res1, col_res2, col_res3 = st.columns(3)

    with col_res1:
        if resultado["FS"] is not None:
            fs_color = "green" if resultado["FS"] >= 1.5 else "orange" if resultado["FS"] >= 1.0 else "red"
            st.markdown(f"### Factor de Seguridad")
            st.markdown(f"<h1 style='color:{fs_color}; font-size:48px;'>{resultado['FS']:.3f}</h1>", 
                       unsafe_allow_html=True)
        else:
            st.error("No se pudo calcular el FS")

    with col_res2:
        st.markdown("### Estado")
        estado = resultado.get("estado", "DESCONOCIDO")
        if estado == "ESTABLE":
            st.success(f"🟢 {estado}")
        elif estado == "PRECARIO":
            st.warning(f"🟡 {estado}")
        else:
            st.error(f"🔴 {estado}")

    with col_res3:
        if "H_cr" in resultado and resultado["H_cr"] != float('inf'):
            st.markdown("### Altura Crítica")
            st.markdown(f"<h2 style='font-size:32px;'>{resultado['H_cr']:.2f} m</h2>", 
                       unsafe_allow_html=True)

    # Detalles del cálculo
    with st.expander("📐 Detalles del Cálculo"):
        st.json(resultado)

    # Guardar resultado
    st.session_state["ultimo_resultado"] = resultado
    st.session_state["metodo_seleccionado"] = metodo_seleccionado

    return resultado
