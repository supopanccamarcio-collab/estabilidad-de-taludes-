"""
================================================================================
GeoSlope Pro - Análisis de Estabilidad de Taludes
================================================================================
Curso: Introducción a las Aplicaciones Digitales
Autor: Ing. Marcio Supo Pancca
Versión: 1.0.0
Fecha: 2026
================================================================================
Aplicativo web profesional para el análisis de estabilidad de taludes en 
ingeniería geotecnica. Implementa 6 métodos de análisis, clasificación GSI,
análisis estadístico y generación de informes técnicos.
================================================================================
"""
import sys
import os

# Agregar el directorio actual al path para que encuentre los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(
    page_title="GeoSlope Pro - Estabilidad de Taludes",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para estilo profesional
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f4e79;
        text-align: center;
        padding: 20px 0;
    }
    .sub-header {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-bottom: 30px;
    }
    .author-info {
        font-size: 14px;
        color: #888;
        text-align: center;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        gap: 4px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f4e79 !important;
        color: white !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
    }
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f4e79;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f8e8;
        border-left: 4px solid #2ca02c;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff8e8;
        border-left: 4px solid #ff7f0e;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    .danger-box {
        background-color: #ffe8e8;
        border-left: 4px solid #d62728;
        padding: 15px;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
    div[data-testid="stSidebarUserContent"] {
        background-color: #f8f9fa;
    }
    .sidebar-title {
        font-size: 20px;
        font-weight: bold;
        color: #1f4e79;
        padding: 10px 0;
        border-bottom: 2px solid #1f4e79;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Importar módulos
import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.gsi_module import render_gsi_module
from modules.materials_module import render_materials_sidebar, render_materials_table
from modules.geometry_module import render_geometry_module
from modules.methods_module import render_methods_selector
from modules.sensitivity_module import render_sensitivity_module
from modules.statistics_module import render_statistics_module, render_tornado_diagram
from modules.report_module import render_report_module

# ============================================================
# HEADER PRINCIPAL
# ============================================================
st.markdown('<div class="main-header">🏔️ GeoSlope Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema Avanzado de Análisis de Estabilidad de Taludes</div>', unsafe_allow_html=True)
st.markdown('<div class="author-info">📚 Curso: Introducción a las Aplicaciones Digitales | 👨‍💻 Autor: Ing. Marcio Supo Pancca</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SIDEBAR - PANEL DE CONTROL
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎛️ Panel de Control</div>', unsafe_allow_html=True)

    # Renderizar selector de materiales
    material_props = render_materials_sidebar()

    st.markdown("---")

    # Información del sistema
    st.markdown("### ℹ️ Información")
    st.info("""
    **GeoSlope Pro v1.0**

    Sistema integral para el análisis de estabilidad de taludes basado en la memoria de cálculo técnica de ingeniería geotécnica.

    **Métodos implementados:**
    - Talud Infinito
    - Culmann
    - Fellenius
    - Bishop Simplificado
    - Taylor
    - Hoek-Brown

    **Autor:** Marcio Supo Pancca
    """)

    st.markdown("---")
    st.caption("© 2026 - Todos los derechos reservados")

# ============================================================
# TABS PRINCIPALES
# ============================================================
tabs = st.tabs([
    "🏔️ GSI",
    "📐 Geometría", 
    "🔬 Métodos",
    "📈 Sensibilidad",
    "📊 Estadística",
    "📄 Informe",
    "📚 Materiales"
])

# Tab 1: GSI
with tabs[0]:
    render_gsi_module()

# Tab 2: Geometría
with tabs[1]:
    render_geometry_module()

# Tab 3: Métodos
with tabs[2]:
    render_methods_selector()

# Tab 4: Sensibilidad
with tabs[3]:
    render_sensitivity_module()

# Tab 5: Estadística
with tabs[4]:
    st.markdown("### 📊 Simulación Monte Carlo")
    render_statistics_module()

    st.markdown("---")
    st.markdown("### 🌪️ Análisis de Tornado")
    render_tornado_diagram()

# Tab 6: Informe
with tabs[5]:
    render_report_module()

# Tab 7: Materiales
with tabs[6]:
    render_materials_table()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px; padding: 20px;">
    <b>GeoSlope Pro v1.0</b> | Curso: Introducción a las Aplicaciones Digitales | Autor: Ing. Marcio Supo Pancca<br>
    Basado en la memoria de cálculo técnica de estabilidad de taludes | © 2026
</div>
""", unsafe_allow_html=True)
