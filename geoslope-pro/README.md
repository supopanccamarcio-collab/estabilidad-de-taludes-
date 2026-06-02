# 🏔️ GeoSlope Pro - Análisis de Estabilidad de Taludes

**Curso:** Introducción a las Aplicaciones Digitales  
**Autor:** Marcio Supo Pancca  
**Versión:** 1.0.0  

---

## 📋 Descripción

Aplicativo web profesional para el análisis de estabilidad de taludes en ingeniería geotécnica. Implementa seis métodos de análisis (Talud Infinito, Culmann, Fellenius, Bishop Simplificado, Taylor y Hoek-Brown), clasificación GSI, análisis estadístico y generación de informes técnicos.

## 🚀 Características Principales

- **Módulo GSI:** Clasificación geomecánica con evaluación interactiva de discontinuidades
- **6 Métodos de Análisis:** Talud Infinito, Culmann, Fellenius, Bishop, Taylor, Hoek-Brown
- **Base de Datos de Materiales:** 20+ materiales con propiedades geotécnicas
- **Geometría del Talud:** Dibujo interactivo con múltiples materiales y capas
- **Análisis de Sensibilidad:** Variación paramétrica con gráficos dinámicos
- **Análisis Estadístico:** Monte Carlo, probabilidad de falla, índice de confiabilidad
- **Informe Técnico:** Generación automática de memoria de cálculo
- **Comparación entre Métodos:** Evaluación cruzada de resultados

## 📦 Instalación

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

```bash
streamlit run app.py
```

## 📁 Estructura del Proyecto

```
├── app.py                    # Aplicación principal
├── modules/
│   ├── gsi_module.py         # Clasificación GSI
│   ├── methods_module.py     # Métodos de análisis
│   ├── materials_module.py   # Base de datos de materiales
│   ├── geometry_module.py    # Geometría del talud
│   ├── sensitivity_module.py # Análisis de sensibilidad
│   ├── statistics_module.py  # Análisis estadístico
│   └── report_module.py      # Generación de informes
├── data/
│   └── materials.json        # Propiedades de materiales
└── requirements.txt
```

## 🎯 Metodología

Basado en la memoria de cálculo técnica que incluye:
- Sistema de Clasificación GSI (Hoek, Carter & Diederichs, 2013)
- Criterio de Rotura Hoek-Brown (2002)
- Métodos clásicos de estabilidad de taludes
- Análisis probabilístico y de confiabilidad

## 📚 Referencias

- Hoek, E., Carter, T.G., & Diederichs, M.S. (2013)
- Hoek, E., Carranza-Torres, C., & Corkum, B. (2002)
- Bieniawski, Z.T. (1989)
- Das, B.M. (2010)
- Bishop, A.W. (1955)
- Fellenius, W. (1927)
- Taylor, D.W. (1937)

## 👨‍💻 Desarrollador

**Marcio Supo Pancca**  
Ingeniero Geotécnico | Especialista en Aplicaciones Digitales

---
*© 2026 - Todos los derechos reservados*