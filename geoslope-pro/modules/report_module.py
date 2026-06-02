"""
Modulo de Generacion de Informes Tecnicos
Curso: Introduccion a las Aplicaciones Digitales
Autor: Marcio Supo Pancca
"""
import streamlit as st
import numpy as np
from datetime import datetime

def generar_informe():
    """Genera el informe tecnico completo"""

    material = st.session_state.get("material_props", {})
    geometry = st.session_state.get("geometry", {})
    gsi = st.session_state.get("gsi_calculado", None)
    resultado = st.session_state.get("ultimo_resultado", {})
    metodo = st.session_state.get("metodo_seleccionado", "No seleccionado")
    mc_results = st.session_state.get("mc_results", None)

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    informe = f"""
# INFORME TECNICO DE ESTABILIDAD DE TALUDES

---

**Curso:** Introduccion a las Aplicaciones Digitales
**Autor:** Ing. Marcio Supo Pancca
**Fecha:** {fecha}
**Software:** GeoSlope Pro v1.0

---

## 1. RESUMEN EJECUTIVO

Este informe presenta el analisis de estabilidad de un talud utilizando metodos de equilibrio limite.

### Resultado Principal
- **Metodo de Analisis:** {metodo}
- **Factor de Seguridad Calculado:** {resultado.get('FS', 'N/A')}
- **Estado de Estabilidad:** {resultado.get('estado', 'No calculado')}

---

## 2. CLASIFICACION GEOMECANICA (GSI)

"""

    if gsi is not None:
        clasificacion = st.session_state.get("clasificacion_gsi", "No calculada")
        informe += f"""
- **GSI Calculado:** {gsi:.1f}
- **Clasificacion del Macizo:** {clasificacion}
- **Metodo Recomendado:** {st.session_state.get('metodo_recomendado', 'No determinado')}

"""
    else:
        informe += "No se realizo clasificacion GSI en esta sesion.

"

    informe += f"""
---

## 3. PROPIEDADES DEL MATERIAL

| Parametro | Valor | Unidad |
|-----------|-------|--------|
| Material | {material.get('name', 'No seleccionado')} | - |
| Categoria | {material.get('category', 'N/A')} | - |
| Cohesion c' | {material.get('c_prime', 'N/A')} | kPa |
| Angulo de friccion phi' | {material.get('phi_prime', 'N/A')} | grados |
| Peso unitario gamma | {material.get('gamma', 'N/A')} | kN/m3 |
"""

    if material.get('gamma_sat') is not None:
        informe += f"| Peso unitario saturado gamma_sat | {material['gamma_sat']} | kN/m3 |
"
    if material.get('sigma_ci') is not None:
        informe += f"| Resistencia intacto sigma_ci | {material['sigma_ci']} | MPa |
"
    if material.get('mi') is not None:
        informe += f"| Parametro mi | {material['mi']} | adimensional |
"
    if material.get('gsi') is not None:
        informe += f"| GSI | {material['gsi']} | adimensional |
"
    if material.get('cu') is not None:
        informe += f"| Cohesion no drenada cu | {material['cu']} | kPa |
"

    informe += f"""

---

## 4. GEOMETRIA DEL TALUD

| Parametro | Valor | Unidad |
|-----------|-------|--------|
| Altura H | {geometry.get('H', 'N/A')} | m |
| Angulo beta | {geometry.get('beta', 'N/A')} | grados |
| Condicion hidrica | {geometry.get('condicion', 'seco')} | - |
| FS deseado | {geometry.get('FS_deseado', '1.5')} | adimensional |

"""

    if geometry.get('tiene_agua'):
        informe += f"| Altura de agua hw | {geometry.get('hw', 'N/A')} | m |
"
        informe += f"| Coeficiente de poros ru | {geometry.get('ru', 'N/A')} | adimensional |
"

    informe += f"""

---

## 5. ANALISIS DE ESTABILIDAD

### 5.1 Metodo Utilizado: {metodo}

"""

    if resultado.get('FS') is not None:
        informe += f"""
**Resultados del Calculo:**

- **Factor de Seguridad (FS):** {resultado['FS']:.4f}
- **Estado:** {resultado['estado']}

"""

        if 'H_cr' in resultado and resultado['H_cr'] != float('inf'):
            informe += f"- **Altura Critica (Hcr):** {resultado['H_cr']:.2f} m
"

        if 'term1' in resultado:
            informe += f"- **Termino de cohesion:** {resultado['term1']:.4f}
"
        if 'term2' in resultado:
            informe += f"- **Termino de friccion:** {resultado['term2']:.4f}
"

        if 'theta_cr' in resultado:
            informe += f"- **Angulo critico del plano de falla:** {resultado['theta_cr']:.2f} grados
"

        if 'n_slices' in resultado:
            informe += f"- **Numero de dovelas:** {resultado['n_slices']}
"

        if 'iterations' in resultado:
            informe += f"- **Iteraciones de convergencia:** {resultado['iterations']}
"

        if 'sigma_cm' in resultado:
            informe += f"- **Resistencia del macizo sigma_cm:** {resultado['sigma_cm']:.3f} MPa
"

        if 'mb' in resultado:
            informe += f"- **Parametro mb:** {resultado['mb']:.3f}
"
        if 's' in resultado:
            informe += f"- **Parametro s:** {resultado['s']:.6f}
"
        if 'a' in resultado:
            informe += f"- **Parametro a:** {resultado['a']:.4f}
"

        informe += "
"

        fs_val = resultado['FS']
        if fs_val >= 1.5:
            informe += """
### Interpretacion

El talud se encuentra en CONDICION ESTABLE. El factor de seguridad supera el valor minimo recomendado de 1.5.

**Recomendacion:** El diseno es aceptable. Se recomienda monitoreo periodico.
"""
        elif fs_val >= 1.0:
            informe += """
### Interpretacion

El talud se encuentra en CONDICION PRECARIA. El factor de seguridad esta entre 1.0 y 1.5.

**Recomendaciones:**
- Implementar sistema de drenaje
- Considerar reduccion del angulo del talud
- Establecer programa de monitoreo continuo
"""
        else:
            informe += """
### Interpretacion

El talud se encuentra en CONDICION INESTABLE. El factor de seguridad es menor a 1.0.

**Recomendaciones URGENTES:**
- NO realizar actividades en la zona del talud
- Implementar medidas de emergencia inmediatamente
- Redisenar el talud con angulo mas suave
- Considerar sistemas de anclaje o muros de contencion
"""
    else:
        informe += "No se pudo calcular el factor de seguridad. Verifique los parametros de entrada.
"

    informe += """

---

## 6. ANALISIS ESTADISTICO (Monte Carlo)

"""

    if mc_results is not None:
        informe += f"""
Se realizo una simulacion Monte Carlo para evaluar la incertidumbre en los parametros geotecnicos.

| Parametro | Valor |
|-----------|-------|
| Media de FS | {mc_results['mu']:.4f} |
| Desviacion estandar | {mc_results['sigma']:.4f} |
| Probabilidad de falla | {mc_results['P_falla']:.2f}% |
| Probabilidad precaria | {mc_results['P_precario']:.2f}% |
| Probabilidad estable | {mc_results['P_estable']:.2f}% |
| Indice de confiabilidad beta | {mc_results['beta']:.4f} |

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
        informe += "No se realizo analisis estadistico en esta sesion.
"

    informe += """

---

## 7. CRITERIOS DE DISENO

| Condicion | FS Minimo Recomendado |
|-----------|----------------------|
| Estatica (permanente) | 1.5 |
| Estatica (temporal) | 1.3 |
| Sismica | 1.1 - 1.3 |
| Obras criticas | > 1.5 |

---

## 8. CONCLUSIONES

"""

    if resultado.get('FS') is not None:
        fs_val = resultado['FS']
        if fs_val >= 1.5:
            informe += f"1. El talud analizado con el metodo de {metodo} presenta un factor de seguridad de {fs_val:.3f}, superando el minimo requerido de 1.5.
"
            informe += "2. El diseno es considerado seguro bajo condiciones estaticas permanentes.
"
        elif fs_val >= 1.0:
            informe += f"1. El talud analizado con el metodo de {metodo} presenta un factor de seguridad de {fs_val:.3f}, encontrandose en condicion precaria.
"
            informe += "2. Se requieren medidas de mitigacion para garantizar la estabilidad a largo plazo.
"
        else:
            informe += f"1. El talud analizado con el metodo de {metodo} presenta un factor de seguridad de {fs_val:.3f}, indicando condicion inestable.
"
            informe += "2. Se requieren medidas correctivas urgentes.
"

    informe += """
3. Los resultados deben ser verificados por un ingeniero geotecnista especializado.
4. Se recomienda realizar investigaciones de campo adicionales para validar los parametros utilizados.

---

## 9. REFERENCIAS

- Hoek, E., Carter, T.G., & Diederichs, M.S. (2013). Quantification of the Geological Strength Index Chart.
- Hoek, E., Carranza-Torres, C., & Corkum, B. (2002). Hoek-Brown failure criterion - 2002 edition.
- Bieniawski, Z.T. (1989). Engineering Rock Mass Classifications. Wiley.
- Das, B.M. (2010). Principles of Geotechnical Engineering, 7th Edition. Cengage Learning.
- Bishop, A.W. (1955). The use of the slip circle in the stability analysis of slopes.
- Fellenius, W. (1927). Erdstatische Berechnungen. Ernst, Berlin.
- Taylor, D.W. (1937). Stability of earth slopes. Journal of the Boston Society of Civil Engineers.

---

*Informe generado automaticamente por GeoSlope Pro v1.0*
*2026 - Ing. Marcio Supo Pancca*
"""

    return informe

def render_report_module():
    """Renderiza el modulo de informes"""
    st.markdown("## 📄 Informe Tecnico")
    st.markdown("*Generacion de memoria de calculo y reporte tecnico*")

    if "ultimo_resultado" not in st.session_state or not st.session_state["ultimo_resultado"]:
        st.warning("Primero ejecute un analisis de estabilidad")
        return

    informe = generar_informe()
    st.markdown(informe)

    st.download_button(
        label="📥 Descargar Informe (Markdown)",
        data=informe,
        file_name=f"informe_estabilidad_talud_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
        mime="text/markdown"
    )

    # Comparacion entre metodos
    st.markdown("---")
    st.markdown("## 🔬 Comparacion entre Metodos")

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
                        "Metodo": met,
                        "FS": f"{res['FS']:.3f}",
                        "Estado": res.get("estado", "N/A"),
                        "Hcr (m)": f"{res.get('H_cr', 'N/A'):.2f}" if res.get('H_cr') != float('inf') else "inf"
                    })
            except:
                pass

        if resultados_comp:
            import pandas as pd
            df_comp = pd.DataFrame(resultados_comp)
            st.dataframe(df_comp, hide_index=True, use_container_width=True)

            # Grafico de barras comparativo
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(12, 6))

            metodos_nombres = [r["Metodo"] for r in resultados_comp]
            fs_vals = [float(r["FS"]) for r in resultados_comp]

            colors = ['green' if fs >= 1.5 else 'orange' if fs >= 1.0 else 'red' for fs in fs_vals]

            bars = ax.bar(metodos_nombres, fs_vals, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

            ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='FS = 1.0 (Critico)')
            ax.axhline(y=geometry.get('FS_deseado', 1.5), color='green', linestyle='--', linewidth=2, label=f'FS = {geometry.get("FS_deseado", 1.5)} (Deseado)')

            ax.set_ylabel("Factor de Seguridad FS", fontsize=12)
            ax.set_title("Comparacion de FS entre Metodos", fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')

            st.pyplot(fig)
