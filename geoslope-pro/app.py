"""
================================================================================
GeoSlope Pro - Analisis de Estabilidad de Taludes
================================================================================
Curso: Introduccion a las Aplicaciones Digitales
Autor: Ing. Marcio Supo Pancca
Version: 1.0.0
Fecha: 2026
================================================================================
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONFIGURACION DE IMPORTS - ROBUSTO PARA LOCAL Y STREAMLIT CLOUD
# ============================================================
import sys
import os

# Obtener el directorio donde esta app.py
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Anadir al path para encontrar modules/ y data/
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

# Imports de modulos
from modules.gsi_module import render_gsi_module
from modules.materials_module import render_materials_sidebar, render_materials_table
from modules.geometry_module import render_geometry_module
from modules.methods_module import render_methods_selector
from modules.sensitivity_module import render_sensitivity_module
from modules.statistics_module import render_statistics_module, render_tornado_diagram
from modules.report_module import render_report_module

# Configuracion de pagina
st.set_page_config(
    page_title="GeoSlope Pro - Estabilidad de Taludes",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
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

# ============================================================
# HEADER PRINCIPAL
# ============================================================
st.markdown('<div class="main-header">🏔️ GeoSlope Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Sistema Avanzado de Analisis de Estabilidad de Taludes</div>', unsafe_allow_html=True)
st.markdown('<div class="author-info">📚 Curso: Introduccion a las Aplicaciones Digitales | 👨‍💻 Autor: Ing. Marcio Supo Pancca</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SIDEBAR - PANEL DE CONTROL
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎛️ Panel de Control</div>', unsafe_allow_html=True)
    material_props = render_materials_sidebar()
    st.markdown("---")
    st.markdown("### ℹ️ Informacion")
    st.info("""
    **GeoSlope Pro v1.0**

    Sistema integral para el analisis de estabilidad de taludes.

    **Metodos implementados:**
    - Talud Infinito
    - Culmann
    - Fellenius
    - Bishop Simplificado
    - Taylor
    - Hoek-Brown
    """)
    st.markdown("---")
    st.caption("© 2026 - Ing. Marcio Supo Pancca")

# ============================================================
# TABS PRINCIPALES
# ============================================================
tabs = st.tabs([
    "🏔️ GSI",
    "📐 Geometria", 
    "🔬 Metodos",
    "📈 Sensibilidad",
    "📊 Estadistica",
    "📄 Informe",
    "📚 Materiales"
])

with tabs[0]:
    render_gsi_module()

with tabs[1]:
    render_geometry_module()

with tabs[2]:
    render_methods_selector()

with tabs[3]:
    render_sensitivity_module()

with tabs[4]:
    st.markdown("### 📊 Simulacion Monte Carlo")
    render_statistics_module()
    st.markdown("---")
    st.markdown("### 🌪️ Analisis de Tornado")
    render_tornado_diagram()

with tabs[5]:
    render_report_module()

with tabs[6]:
    render_materials_table()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 12px; padding: 20px;">
    <b>GeoSlope Pro v1.0</b> | Curso: Introduccion a las Aplicaciones Digitales | Autor: Ing. Marcio Supo Pancca<br>
    © 2026
</div>
""", unsafe_allow_html=True)
