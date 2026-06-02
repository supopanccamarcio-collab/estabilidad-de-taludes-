"""
Módulo de Geometría del Talud
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon

def render_geometry_module():
    """Renderiza el módulo de geometría del talud"""
    st.markdown("## 📐 Geometría del Talud")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Parámetros del Talud")

        # Altura del talud
        H = st.slider(
            "Altura del talud H (m)", 
            1.0, 100.0, 
            st.session_state.get("H_default", 10.0), 
            0.5,
            help="Altura vertical del talud"
        )

        # Ángulo del talud
        beta = st.slider(
            "Ángulo del talud β (°)", 
            5.0, 85.0, 
            st.session_state.get("beta_default", 30.0), 
            0.5,
            help="Inclinación del talud respecto a horizontal"
        )

        # Nivel freático
        st.markdown("### 💧 Condiciones Hídricas")

        tiene_agua = st.checkbox("Incluir nivel freático", value=False)

        hw = 0.0
        ru = 0.0
        condicion = "seco"

        if tiene_agua:
            condicion = st.radio(
                "Condición:",
                ["Nivel freático en superficie", "Nivel freático parcial", "Coeficiente de poros ru"],
                horizontal=True
            )

            if condicion == "Nivel freático en superficie":
                hw = H
                condicion = "saturado"
            elif condicion == "Nivel freático parcial":
                hw = st.slider("Altura de agua hw (m)", 0.0, H, H/2, 0.1)
                condicion = "parcial"
            else:
                ru = st.slider("Coeficiente de poros ru", 0.0, 0.7, 0.3, 0.01)
                condicion = "ru"

        # Factor de seguridad deseado
        st.markdown("### 🎯 Diseño")
        FS_deseado = st.slider(
            "FS deseado", 
            1.0, 3.0, 1.5, 0.05,
            help="Factor de seguridad mínimo requerido"
        )

        # Tipo de análisis sísmico
        st.markdown("### 🌋 Condiciones Especiales")

        analisis_sismico = st.checkbox("Incluir análisis sísmico", value=False)
        kh = 0.0
        if analisis_sismico:
            kh = st.slider("Coeficiente sísmico kh", 0.0, 0.5, 0.15, 0.01)

    with col2:
        st.markdown("### 🎨 Visualización del Talud")

        fig, ax = plt.subplots(figsize=(10, 8))

        # Dibujar talud
        beta_rad = np.radians(beta)

        # Base del talud
        base_length = H / np.tan(beta_rad)

        # Puntos del talud
        x_talud = [0, base_length, base_length, 0]
        y_talud = [0, 0, H, H]

        # Crear polígono del talud
        talud = Polygon(list(zip(x_talud, y_talud)), 
                       facecolor='#D2691E', edgecolor='black', linewidth=2, alpha=0.7)
        ax.add_patch(talud)

        # Dibujar nivel freático si aplica
        if tiene_agua and hw > 0:
            # Nivel freático como línea
            hw_ratio = hw / H
            x_agua = [0, base_length * hw_ratio]
            y_agua = [hw, hw]
            ax.plot(x_agua, y_agua, 'b--', linewidth=2, label=f'Nivel freático (hw={hw:.1f}m)')

            # Zona saturada
            if condicion == "saturado":
                x_sat = [0, base_length, base_length, 0]
                y_sat = [0, 0, H, H]
            else:
                x_sat = [0, base_length * hw_ratio, base_length * hw_ratio, 0]
                y_sat = [0, 0, hw, hw]

            sat_poly = Polygon(list(zip(x_sat, y_sat)), 
                              facecolor='blue', edgecolor='blue', 
                              linewidth=1, alpha=0.2)
            ax.add_patch(sat_poly)

        # Dibujar ángulo
        from matplotlib.patches import Arc
        arc = Arc((base_length, 0), 3, 3, angle=0, 
                 theta1=180-beta, theta2=180, color='red', linewidth=2)
        ax.add_patch(arc)
        ax.annotate(f'β = {beta}°', xy=(base_length-1.5, 0.5), 
                   fontsize=12, color='red', fontweight='bold')

        # Dimensiones
        ax.annotate(f'H = {H}m', xy=(base_length/2, H+0.5), 
                   fontsize=12, ha='center', fontweight='bold')
        ax.annotate(f'L = {base_length:.1f}m', xy=(base_length/2, -0.8), 
                   fontsize=12, ha='center', fontweight='bold')

        # Configuración del gráfico
        ax.set_xlim(-1, base_length + 2)
        ax.set_ylim(-1.5, H + 2)
        ax.set_aspect('equal')
        ax.set_xlabel('Distancia (m)', fontsize=12)
        ax.set_ylabel('Altura (m)', fontsize=12)
        ax.set_title('Geometría del Talud', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')

        st.pyplot(fig)

        # Información geométrica
        st.markdown("### 📊 Información Geométrica")

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:
            st.metric("Altura H", f"{H:.1f} m")

        with info_col2:
            st.metric("Ángulo β", f"{beta:.1f}°")

        with info_col3:
            st.metric("Base L", f"{base_length:.1f} m")

    # Guardar en session state
    geometry = {
        "H": H,
        "beta": beta,
        "beta_rad": beta_rad,
        "base_length": base_length,
        "tiene_agua": tiene_agua,
        "hw": hw,
        "ru": ru,
        "condicion": condicion,
        "FS_deseado": FS_deseado,
        "analisis_sismico": analisis_sismico,
        "kh": kh
    }

    st.session_state["geometry"] = geometry

    return geometry

def render_multi_layer_geometry():
    """Renderiza geometría con múltiples capas de materiales"""
    st.markdown("## 📐 Geometría Multicapa del Talud")

    st.info("🚧 Esta función permite definir taludes con múltiples materiales en capas. "
            "Actualmente en desarrollo avanzado.")

    # Por ahora, usar la geometría simple
    return render_geometry_module()
