"""
Módulo de Generación de Informes Técnicos
Curso: Introducción a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import streamlit as st
import numpy as np
from datetime import datetime

def generar_informe():
    """Genera el informe técnico completo"""

    material = st.session_state.get("material_props", {})
    geometry = st.session_state.get("geometry", {})
    gsi = st.session_state.get("gsi_calculado", None)
    resultado = st.session_state.get("ultimo_resultado", {})
    metodo = st.session_state.get("metodo_seleccionado", "No seleccionado")
    mc_results = st.session_state.get("mc_results", None)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    informe = f"""
# 📋 INFORME TÉCNICO DE ESTABILIDAD DE TALUDES

---

**Curso:** Introducción a las Aplicaciones Digitales  
**Autor:** Ing. Marcio Supo Pancca  
**Fecha:** {fecha}  
**Software:** GeoSlope Pro v1.0

---

## 1. RESUMEN EJECUTIVO

Este informe presenta el análisis de estabilidad de un talud utilizando métodos de equilibrio límite, basado en la memoria de cálculo técnica de ingeniería geotécnica.

### Resultado Principal
- **Método de Análisis:** {metodo}
- **Factor de Seguridad Calculado:** {resultado.get('FS', 'N/A')}
- **Estado de Estabilidad:** {resultado.get('estado', 'No calculado')}

---

## 2. CLASIFICACIÓN GEOMECÁNICA (GSI)

"""

    if gsi is not None:
        clasificacion = st.session_state.get("clasificacion_gsi", "No calculada")
        informe += f"""
- **GSI Calculado:** {gsi:.1f}
- **Clasificación del Macizo:** {clasificacion}
- **Método Recomendado:** {st.session_state.get('metodo_recomendado', 'No determinado')}

"""
    else:
        informe += "No se realizó clasificación GSI en esta sesión.

"

    informe += f"""
---

## 3. PROPIEDADES DEL MATERIAL

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Material | {material.get('name', 'No seleccionado')} | - |
| Categoría | {material.get('category', 'N/A')} | - |
| Cohesión c' | {material.get('c_prime', 'N/A')} | kPa |
| Ángulo de fricción φ' | {material.get('phi_prime', 'N/A')} | ° |
| Peso unitario γ | {material.get('gamma', 'N/A')} | kN/m³ |
"""

    if material.get('gamma_sat') is not None:
        informe += f"| Peso unitario saturado γ_sat | {material['gamma_sat']} | kN/m³ |
"
    if material.get('sigma_ci') is not None:
        informe += f"| Resistencia intacto σci | {material['sigma_ci']} | MPa |
"
    if material.get('mi') is not None:
        informe += f"| Parámetro mi | {material['mi']} | adimensional |
"
    if material.get('gsi') is not None:
        informe += f"| GSI | {material['gsi']} | adimensional |
"
    if material.get('cu') is not None:
        informe += f"| Cohesión no drenada cu | {material['cu']} | kPa |
"

    informe += f"""

---

## 4. GEOMETRÍA DEL TALUD

| Parámetro | Valor | Unidad |
|-----------|-------|--------|
| Altura H | {geometry.get('H', 'N/A')} | m |
| Ángulo β | {geometry.get('beta', 'N/A')} | ° |
| Condición hídrica | {geometry.get('condicion', 'seco')} | - |
| FS deseado | {geometry.get('FS_deseado', '1.5')} | adimensional |

"""

    if geometry.get('tiene_agua'):
        informe += f"| Altura de agua hw | {geometry.get('hw', 'N/A')} | m |
"
        informe += f"| Coeficiente de poros ru | {geometry.get('ru', 'N/A')} | adimensional |
"

    informe += f"""

---

## 5. ANÁLISIS DE ESTABILIDAD

### 5.1 Método Utilizado: {metodo}

"""

    if resultado.get('FS') is not None:
        informe += f"""
**Resultados del Cálculo:**

- **Factor de Seguridad (FS):** {resultado['FS']:.4f}
- **Estado:** {resultado['estado']}

"""

        if 'H_cr' in resultado and resultado['H_cr'] != float('inf'):
            informe += f"- **Altura Crítica (Hcr):** {resultado['H_cr']:.2f} m
"

        if 'term1' in resultado:
            informe += f"- **Término de cohesión:** {resultado['term1']:.4f}
"
        if 'term2' in resultado:
            informe += f"- **Término de fricción:** {resultado['term2']:.4f}
"

        if 'theta_cr' in resultado:
            informe += f"- **Ángulo crítico del plano de falla:** {resultado['theta_cr']:.2f}°
"

        if 'n_slices' in resultado:
            informe += f"- **Número de dovelas:** {resultado['n_slices']}
"

        if 'iterations' in resultado:
            informe += f"- **Iteraciones de convergencia:** {resultado['iterations']}
"

        if 'sigma_cm' in resultado:
            informe += f"- **Resistencia del macizo σcm:** {resultado['sigma_cm']:.3f} MPa
"

        if 'mb' in resultado:
            informe += f"- **Parámetro mb:** {resultado['mb']:.3f}
"
        if 's' in resultado:
            informe += f"- **Parámetro s:** {resultado['s']:.6f}
"
        if 'a' in resultado:
            informe += f"- **Parámetro a:** {resultado['a']:.4f}
"

        informe += "
"

        # Interpretación
        fs_val = resultado['FS']
        if fs_val >= 1.5:
            informe += """
### 📗 Interpretación

El talud se encuentra en **CONDICIÓN ESTABLE** bajo las condiciones analizadas. El factor de seguridad supera el valor mínimo recomendado de 1.5 para condiciones estáticas permanentes.

**Recomendación:** El diseño es aceptable. Se recomienda monitoreo periódico.
"""
        elif fs_val >= 1.0:
            informe += """
### 📙 Interpretación

El talud se encuentra en **CONDICIÓN PRECARIA**. El factor de seguridad está entre 1.0 y 1.5, lo que indica que el talud requiere atención.

**Recomendaciones:**
- Implementar sistema de drenaje
- Considerar reducción del ángulo del talud
- Establecer programa de monitoreo continuo
- Evaluar medidas de refuerzo si es necesario
"""
        else:
            informe += """
### 📕 Interpretación

El talud se encuentra en **CONDICIÓN INESTABLE**. El factor de seguridad es menor a 1.0, lo que indica que la falla es inminente.

**Recomendaciones URGENTES:**
- NO realizar actividades en la zona del talud
- Implementar medidas de emergencia inmediatamente
- Rediseñar el talud con ángulo más suave
- Considerar sistemas de anclaje o muros de contención
- Establecer sistema de alerta temprana
"""
    else:
        informe += "No se pudo calcular el factor de seguridad. Verifique los parámetros de entrada.
"

    informe += """

---

## 6. ANÁLISIS ESTADÍSTICO (Monte Carlo)

"""

    if mc_results is not None:
        informe += f"""
Se realizó una simulación Monte Carlo para evaluar la incertidumbre en los parámetros geotécnicos.

| Parámetro | Valor |
|-----------|-------|
| Media de FS | {mc_results['mu']:.4f} |
| Desviación estándar | {mc_results['sigma']:.4f} |
| Probabilidad de falla | {mc_results['P_falla']:.2f}% |
| Probabilidad precaria | {mc_results['P_precario']:.2f}% |
| Probabilidad estable | {mc_results['P_estable']:.2f}% |
| Índice de confiabilidad β | {mc_results['beta']:.4f} |

"""

        if mc_results['beta'] >= 2.5:
            informe += "**Confiabilidad: ALTA** - El talud presenta bajo riesgo de falla.
"
        elif mc_results['beta'] >= 1.5:
            informe += "**Confiabilidad: MEDIA** - El talud requiere monitoreo.
"
        else:
            informe += "**Confiabilidad: BAJA** - El talud presenta alto riesgo de falla.
"
    else:
        informe += "No se realizó análisis estadístico en esta sesión.
"

    informe += """

---

## 7. CRITERIOS DE DISEÑO

| Condición | FS Mínimo Recomendado |
|-----------|----------------------|
| Estática (permanente) | 1.5 |
| Estática (temporal) | 1.3 |
| Sísmica | 1.1 - 1.3 |
| Obras críticas | > 1.5 |

---

## 8. CONCLUSIONES

"""

    if resultado.get('FS') is not None:
        fs_val = resultado['FS']
        if fs_val >= 1.5:
            informe += f"1. El talud analizado con el método de {metodo} presenta un factor de seguridad de {fs_val:.3f}, superando el mínimo requerido de 1.5.
"
            informe += "2. El diseño es considerado seguro bajo condiciones estáticas permanentes.
"
        elif fs_val >= 1.0:
            informe += f"1. El talud analizado con el método de {metodo} presenta un factor de seguridad de {fs_val:.3f}, encontrándose en condición precaria.
"
            informe += "2. Se requieren medidas de mitigación para garantizar la estabilidad a largo plazo.
"
        else:
            informe += f"1. El talud analizado con el método de {metodo} presenta un factor de seguridad de {fs_val:.3f}, indicando condición inestable.
"
            informe += "2. Se requieren medidas correctivas urgentes.
"

    informe += """
3. Los resultados deben ser verificados por un ingeniero geotecnista especializado.
4. Se recomienda realizar investigaciones de campo adicionales para validar los parámetros utilizados.

---

## 9. REFERENCIAS

- Hoek, E., Carter, T.G., & Diederichs, M.S. (2013). Quantification of the Geological Strength Index Chart. *47th US Rock Mechanics/Geomechanics Symposium*.
- Hoek, E., Carranza-Torres, C., & Corkum, B. (2002). Hoek-Brown failure criterion - 2002 edition. *Proceedings of NARMS-TAC*.
- Bieniawski, Z.T. (1989). *Engineering Rock Mass Classifications*. Wiley.
- Das, B.M. (2010). *Principles of Geotechnical Engineering*, 7th Edition. Cengage Learning.
- Bishop, A.W. (1955). The use of the slip circle in the stability analysis of slopes. *Géotechnique*, 5(1), 7-17.
- Fellenius, W. (1927). *Erdstatische Berechnungen*. Ernst, Berlin.
- Taylor, D.W. (1937). Stability of earth slopes. *Journal of the Boston Society of Civil Engineers*, 24(3), 197-246.

---

*Informe generado automáticamente por GeoSlope Pro v1.0*  
*© 2026 - Ing. Marcio Supo Pancca*
"""

    return informe

def render_report_module():
    """Renderiza el módulo de informes"""
    st.markdown("## 📄 Informe Técnico")
    st.markdown("*Generación de memoria de cálculo y reporte técnico*")

    # Verificar que haya datos
    if "ultimo_resultado" not in st.session_state or not st.session_state["ultimo_resultado"]:
        st.warning("⚠️ Primero ejecute un análisis de estabilidad")
        return

    # Generar informe
    informe = generar_informe()

    # Mostrar informe
    st.markdown(informe)

    # Botón de descarga
    st.download_button(
        label="📥 Descargar Informe (Markdown)",
        data=informe,
        file_name=f"informe_estabilidad_talud_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown"
    )

    # Comparación entre métodos
    st.markdown("---")
    st.markdown("## 🔬 Comparación entre Métodos")

    material = st.session_state.get("material_props", {})
    geometry = st.session_state.get("geometry", {})

    if material and geometry:
        from modules.methods_module import ejecutar_metodo

        metodos = ["Talud Infinito", "Culmann", "Fellenius", "Bishop Simplificado", "Taylor"]
        resultados_comp = []

        for met in metodos:
            try:
                res = ejecutar_metodo(met, material, geometry)
                if res.get("FS") is not None:
                    resultados_comp.append({
                        "Método": met,
                        "FS": f"{res['FS']:.3f}",
                        "Estado": res.get("estado", "N/A"),
                        "Hcr (m)": f"{res.get('H_cr', 'N/A'):.2f}" if res.get('H_cr') != float('inf') else "∞"
                    })
            except:
                pass

        if resultados_comp:
            import pandas as pd
            df_comp = pd.DataFrame(resultados_comp)
            st.dataframe(df_comp, hide_index=True, use_container_width=True)

            # Gráfico de barras comparativo
            fig, ax = plt.subplots(figsize=(12, 6))

            metodos_nombres = [r["Método"] for r in resultados_comp]
            fs_vals = [float(r["FS"]) for r in resultados_comp]

            colors = ['green' if fs >= 1.5 else 'orange' if fs >= 1.0 else 'red' for fs in fs_vals]

            bars = ax.bar(metodos_nombres, fs_vals, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

            ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='FS = 1.0 (Crítico)')
            ax.axhline(y=geometry.get('FS_deseado', 1.5), color='green', linestyle='--', linewidth=2, label=f'FS = {geometry.get("FS_deseado", 1.5)} (Deseado)')

            ax.set_ylabel("Factor de Seguridad FS", fontsize=12)
            ax.set_title("Comparación de FS entre Métodos", fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')

            st.pyplot(fig)
