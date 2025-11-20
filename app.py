import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, t as t_dist
from io import BytesIO

# Configuración de estilo
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10, 6)

def exportar_excel(df):
    """Exporta DataFrame a Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
    return output.getvalue()

# Configuración de página
st.set_page_config(page_title="Calculadora de Tamaño de Muestra", layout="wide", page_icon="🔢")

st.title("🔢 Calculadora Avanzada de Tamaño de Muestra")
st.markdown("Herramienta completa para calcular tamaños de muestra en diferentes escenarios y tipos de muestreo")

# Selección principal
opcion_principal = st.sidebar.radio(
    "Selecciona el módulo:",
    ["📊 Por Tipo de Estimación", "🎯 Por Tipo de Muestreo", "❓ Ayuda y Glosario"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Módulos disponibles:**
- **Por Tipo de Estimación:** Media, Proporción, Diferencias
- **Por Tipo de Muestreo:** Aleatorio, Estratificado, Conglomerados, Sistemático
- **Ayuda:** Glosario y conceptos clave
""")

# ==========================================
# MÓDULO DE AYUDA Y GLOSARIO
# ==========================================
if opcion_principal == "❓ Ayuda y Glosario":
    st.header("📚 Ayuda y Glosario de Términos")
    
    tab_glosario, tab_formulas, tab_ejemplos = st.tabs([
        "📖 Glosario de Términos",
        "📐 Fórmulas Principales",
        "💡 Guía de Uso"
    ])
    
    # TAB 1: GLOSARIO
    with tab_glosario:
        st.subheader("Términos Estadísticos Clave")
        
        with st.expander("⭐ **N (Tamaño de población)**", expanded=True):
            st.markdown("""
            **Definición:** Número total de elementos en la población objetivo.
            
            **Ejemplo:** Si quieres estudiar a los estudiantes de una universidad con 10,000 alumnos, N = 10,000.
            
            **Nota:** Si N > 100,000 o es desconocido, se considera población infinita.
            """)
        
        with st.expander("⭐ **n (Tamaño de muestra)**"):
            st.markdown("""
            **Definición:** Número de elementos que debes seleccionar y medir de la población.
            
            **Ejemplo:** Si calculas n = 370, debes encuestar/medir 370 personas.
            
            **Objetivo:** Obtener información representativa con el mínimo costo.
            """)
        
        with st.expander("⭐ **σ (Sigma - Desviación estándar poblacional)**"):
            st.markdown("""
            **Definición:** Medida de dispersión de los datos en la población. Indica qué tan variables son los valores.
            
            **¿Cómo obtenerla?**
            - Estudios piloto previos
            - Literatura especializada
            - Datos históricos
            - Estimación conservadora (usar valor alto)
            
            **Ejemplo:** Si mides altura (σ = 10 cm), significa que la mayoría de alturas varían ±10 cm del promedio.
            """)
        
        with st.expander("⭐ **E (Error máximo o margen de error)**"):
            st.markdown("""
            **Definición:** Diferencia máxima aceptable entre el estimador muestral y el parámetro poblacional real.
            
            **Para medias:** En las mismas unidades de la variable (kg, cm, puntos, etc.)
            **Para proporciones:** Generalmente expresado como decimal (0.05 = ±5%)
            
            **Ejemplo:** - Si E = 2 kg, tu estimación estará a ±2 kg del valor real
            - Si E = 0.05 (5%), tu estimación estará a ±5 puntos porcentuales
            """)
        
        with st.expander("⭐ **α (Alpha - Nivel de significancia)**"):
            st.markdown("""
            **Definición:** Probabilidad de cometer Error Tipo I (rechazar H₀ siendo verdadera).
            
            **Valores comunes:**
            - α = 0.05 → 5% de riesgo → **95% de confianza**
            - α = 0.01 → 1% de riesgo → **99% de confianza**
            - α = 0.10 → 10% de riesgo → **90% de confianza**
            
            **Interpretación:** Con α = 0.05, en 5 de cada 100 estudios podrías encontrar una diferencia que no existe.
            """)
        
        with st.expander("⭐ **1-β (Potencia estadística)**"):
            st.markdown("""
            **Definición:** Probabilidad de detectar un efecto cuando realmente existe.
            
            **Valores recomendados:**
            - **0.80 (80%)**: Estándar en ciencias sociales
            - **0.90 (90%)**: Preferible en investigación clínica
            - **0.95 (95%)**: Para decisiones críticas
            
            **Interpretación:** Con potencia de 80%, si hay una diferencia real, la detectarás en 8 de cada 10 estudios.
            
            **β (Beta):** Error Tipo II = no detectar un efecto que sí existe. Típicamente β = 0.20 (20%).
            """)
        
        with st.expander("⭐ **d de Cohen (Tamaño del efecto)**"):
            st.markdown("""
            **Definición:** Medida estandarizada de la magnitud de una diferencia.
            
            **Fórmula:** d = Δ / σ
            
            **Clasificación:**
            - d < 0.2: Efecto muy pequeño 🔴
            - 0.2 ≤ d < 0.5: Efecto pequeño 🟡
            - 0.5 ≤ d < 0.8: Efecto mediano 🔵
            - d ≥ 0.8: Efecto grande 🟢
            
            **Ejemplo:** Si Δ = 10 kg y σ = 5 kg, entonces d = 2.0 (efecto muy grande).
            """)
        
        with st.expander("⭐ **p (Proporción poblacional)**"):
            st.markdown("""
            **Definición:** Porcentaje o fracción de la población que tiene una característica.
            
            **Expresión:** - Decimal: p = 0.30 (30%)
            - Porcentaje: 30%
            
            **¿Qué hacer si no conoces p?**
            - Usar p = 0.50 (enfoque conservador, da el n máximo)
            - Usar datos de estudios piloto
            - Usar literatura previa
            
            **Ejemplo:** Si 30% de estudiantes fuma, p = 0.30.
            """)
        
        with st.expander("⭐ **DEFF (Efecto de diseño)**"):
            st.markdown("""
            **Definición:** Factor que indica la pérdida de eficiencia al usar un diseño complejo vs. MAS.
            
            **Fórmula:** DEFF = n_diseño / n_MAS
            
            **Interpretación:**
            - DEFF = 1.0: Igual eficiencia que MAS
            - DEFF = 1.5: Necesitas 50% más muestra
            - DEFF = 2.0: Necesitas el doble de muestra
            
            **Causas:** Correlación intra-clase, heterogeneidad entre conglomerados.
            """)
        
        with st.expander("⭐ **ICC o ρ (Coeficiente de correlación intraclase)**"):
            st.markdown("""
            **Definición:** Medida de similitud entre elementos dentro del mismo conglomerado.
            
            **Rango:** 0 ≤ ρ ≤ 1
            
            **Interpretación:**
            - ρ = 0: Elementos independientes (como MAS)
            - ρ = 0.01-0.05: Baja correlación (típico)
            - ρ = 0.10-0.30: Moderada correlación
            - ρ > 0.30: Alta correlación (conglomerados muy homogéneos)
            
            **Ejemplo:** En escuelas, estudiantes de la misma clase son más similares (ρ alto).
            """)
        
        with st.expander("⭐ **W_h (Peso del estrato)**"):
            st.markdown("""
            **Definición:** Proporción que representa cada estrato respecto al total poblacional.
            
            **Fórmula:** W_h = N_h / N
            
            **Uso:** Para calcular estimadores ponderados en muestreo estratificado.
            
            **Ejemplo:** Si el estrato 1 tiene 3,000 elementos de una población de 10,000:
            W₁ = 3,000 / 10,000 = 0.30 (30%)
            """)
        
        with st.expander("⭐ **k (Intervalo de selección sistemática)**"):
            st.markdown("""
            **Definición:** Paso o salto entre elementos seleccionados en muestreo sistemático.
            
            **Fórmula:** k = N / n (se redondea)
            
            **Uso:** Seleccionar cada k-ésimo elemento.
            
            **Ejemplo:** Si N = 1,000 y n = 100, entonces k = 10. 
            Seleccionas: 3, 13, 23, 33, 43... (si inicio aleatorio = 3)
            """)
        
        with st.expander("⭐ **FPC (Corrección por población finita)**"):
            st.markdown("""
            **Definición:** Ajuste que reduce el tamaño de muestra cuando se muestrea una fracción grande de la población.
            
            **Fórmula:** n_ajustado = n₀ / (1 + (n₀-1)/N)
            
            **¿Cuándo aplicar?**
            - Cuando n/N > 0.05 (muestreas más del 5%)
            - Cuando N < 100,000
            
            **Efecto:** Reduce el tamaño de muestra necesario.
            """)
    
    # TAB 2: FÓRMULAS
    with tab_formulas:
        st.subheader("📐 Fórmulas Principales")
        
        st.markdown("### 1️⃣ Estimación de una Media")
        st.latex(r"n_0 = \frac{Z_{\alpha/2}^2 \cdot \sigma^2}{E^2}")
        st.markdown("Con corrección por población finita:")
        st.latex(r"n = \frac{n_0}{1 + \frac{n_0 - 1}{N}}")
        
        st.markdown("---")
        st.markdown("### 2️⃣ Estimación de una Proporción")
        st.latex(r"n_0 = \frac{Z_{\alpha/2}^2 \cdot p \cdot (1-p)}{E^2}")
        st.markdown("Valor máximo (conservador): usar p = 0.5")
        
        st.markdown("---")
        st.markdown("### 3️⃣ Diferencia de Medias (2 grupos)")
        st.latex(r"n = 2 \cdot \left[\frac{(Z_{\alpha/2} + Z_\beta) \cdot \sigma}{\Delta}\right]^2")
        st.markdown("Donde:")
        st.markdown("- Δ: diferencia mínima a detectar")
        st.markdown("- σ: desviación estándar común")
        st.markdown("- Z_β: valor Z asociado a la potencia")
        
        st.markdown("---")
        st.markdown("### 4️⃣ Muestreo Estratificado (Asignación Proporcional)")
        st.latex(r"n_h = n \cdot \frac{N_h}{N} = n \cdot W_h")
        st.markdown("**Asignación Óptima (Neyman):**")
        st.latex(r"n_h = n \cdot \frac{N_h \cdot \sigma_h}{\sum_{i=1}^{L} N_i \cdot \sigma_i}")
        
        st.markdown("---")
        st.markdown("### 5️⃣ Muestreo por Conglomerados")
        st.latex(r"DEFF = 1 + (m - 1) \cdot \rho")
        st.latex(r"n_{conglomerados} = n_{MAS} \cdot DEFF")
        st.markdown("Donde:")
        st.markdown("- m: tamaño promedio del conglomerado")
        st.markdown("- ρ: coeficiente de correlación intraclase")
        
        st.markdown("---")
        st.markdown("### 6️⃣ Muestreo Sistemático")
        st.latex(r"k = \left\lfloor \frac{N}{n} \right\rfloor")
        st.markdown("Selección: r, r+k, r+2k, r+3k, ...")
        st.markdown("Donde r es un inicio aleatorio entre 1 y k")
        
        st.markdown("---")
        st.markdown("### 7️⃣ Tamaño del Efecto (d de Cohen)")
        st.latex(r"d = \frac{\Delta}{\sigma}")
        
        st.markdown("---")
        st.markdown("### 8️⃣ Valores Críticos Comunes")
        
        df_valores = pd.DataFrame({
            'Confianza': ['90%', '95%', '99%'],
            'α': [0.10, 0.05, 0.01],
            'Z_{α/2}': [1.645, 1.960, 2.576],
            'Uso': ['Exploratorio', 'Estándar', 'Riguroso']
        })
        st.dataframe(df_valores, use_container_width=True)
    
    # TAB 3: GUÍA DE USO
    with tab_ejemplos:
        st.subheader("💡 Guía de Uso Rápida")
        
        st.markdown("### 🎯 ¿Qué módulo debo usar?")
        
        st.markdown("#### **Use 'Por Tipo de Estimación' cuando:**")
        st.markdown("""
        - Quieres estimar un parámetro poblacional (media o proporción)
        - Necesitas comparar dos grupos
        - Tienes una población claramente definida
        - Buscas cálculos estándar de tamaño de muestra
        """)
        
        st.markdown("#### **Use 'Por Tipo de Muestreo' cuando:**")
        st.markdown("""
        - Ya decidiste qué método de muestreo usar
        - Necesitas optimizar costos y logística
        - Tienes una población con estructura especial (estratos, conglomerados)
        - Quieres comparar diferentes métodos de muestreo
        """)
        
        st.markdown("---")
        st.markdown("### 📋 Casos de Uso Comunes")
        
        with st.expander("🔹 Caso 1: Encuesta de satisfacción en una empresa"):
            st.markdown("""
            **Situación:** Empresa con 5,000 empleados, quieres estimar % de satisfacción.
            
            **Pasos:**
            1. Ir a: **Por Tipo de Estimación → Estimación de una Proporción**
            2. Configurar:
               - Proporción estimada: 0.50 (conservador)
               - Margen de error: 0.05 (±5%)
               - Confianza: 95%
               - Población: 5,000
            3. Resultado: ~357 empleados
            
            **Método de muestreo sugerido:** Aleatorio Simple o Estratificado (por departamento)
            """)
        
        with st.expander("🔹 Caso 2: Estudio clínico comparando dos tratamientos"):
            st.markdown("""
            **Situación:** Comparar efectividad de dos medicamentos para reducir presión arterial.
            
            **Pasos:**
            1. Ir a: **Por Tipo de Estimación → Diferencia de Medias**
            2. Configurar:
               - Diferencia a detectar (Δ): 10 mmHg
               - Desviación estándar: 15 mmHg
               - α: 0.05
               - Potencia: 80%
            3. Resultado: ~37 pacientes por grupo (74 total)
            
            **d de Cohen:** 10/15 = 0.67 (efecto mediano)
            """)
        
        with st.expander("🔹 Caso 3: Muestreo en escuelas (varios niveles)"):
            st.markdown("""
            **Situación:** Evaluar rendimiento académico en 150 escuelas con ~200 estudiantes c/u.
            
            **Pasos:**
            1. Ir a: **Por Tipo de Muestreo → Muestreo por Conglomerados**
            2. Configurar:
               - M total: 150 escuelas
               - Tamaño promedio: 200 estudiantes
               - Dos etapas con 50% submuestreo
            3. Resultado: ~15 escuelas, 100 estudiantes por escuela
            
            **Ventaja:** Solo visitas 15 escuelas vs. 3,000 estudiantes dispersos
            """)
        
        with st.expander("🔹 Caso 4: Control de calidad en producción"):
            st.markdown("""
            **Situación:** Inspeccionar lote de 10,000 productos para estimar % defectuosos.
            
            **Pasos:**
            1. Ir a: **Por Tipo de Muestreo → Muestreo Sistemático**
            2. Configurar:
               - N: 10,000
               - Proporción estimada: 0.03 (3%)
               - Error: 0.01 (±1%)
            3. Resultado: n = 269, k = 37
            
            **Implementación:** Selecciona 1 de cada 37 productos, comenzando en posición aleatoria.
            """)
        
        st.markdown("---")
        st.markdown("### ⚠️ Errores Comunes a Evitar")
        
        col_err1, col_err2 = st.columns(2)
        
        with col_err1:
            st.markdown("#### ❌ NO hacer:")
            st.markdown("""
            - Usar n muy pequeño (< 30) sin justificación
            - Ignorar la corrección por población finita cuando n/N > 0.05
            - Usar muestreo sistemático con periodicidad conocida
            - Estimar σ demasiado pequeño (subestima n)
            - Usar α muy alto (> 0.10) sin justificación
            """)
        
        with col_err2:
            st.markdown("#### ✅ SÍ hacer:")
            st.markdown("""
            - Realizar estudio piloto para estimar σ o p
            - Documentar todas las suposiciones
            - Considerar tasa de no respuesta (inflar n 10-20%)
            - Validar que n sea factible económicamente
            - Consultar con experto si hay dudas
            """)
        
        st.markdown("---")
        st.markdown("### 📚 Recursos Adicionales")
        
        st.info("""
        **Libros recomendados:**
        - Cochran, W.G. (1977). *Sampling Techniques*
        - Lohr, S.L. (2019). *Sampling: Design and Analysis*
        - Scheaffer, R.L. et al. (2011). *Elementary Survey Sampling*
        
        **Software complementario:**
        - R: paquetes `survey`, `sampling`
        - Python: `scipy.stats`, `statsmodels`
        - SPSS, Stata, SAS (módulos de muestreo)
        """)

# ==========================================
# MÓDULO 1: POR TIPO DE ESTIMACIÓN
# ==========================================
elif opcion_principal == "📊 Por Tipo de Estimación":
    
    tipo_calculo = st.selectbox(
        "Selecciona el tipo de estimación:",
        [
            "📊 Estimación de una Media",
            "📈 Estimación de una Proporción",
            "🔄 Diferencia de Medias (2 grupos)",
            "⚖️ Diferencia de Proporciones (2 grupos)"
        ]
    )
    
    st.markdown("---")
    
    # ==========================================
    # 1. ESTIMACIÓN DE UNA MEDIA
    # ==========================================
    if tipo_calculo == "📊 Estimación de una Media":
        st.header("Estimación de una Media Poblacional")
        
        st.info("""
        **Características:**
        - Cada elemento tiene la misma probabilidad de ser seleccionado
        - Selección independiente de cada unidad
        - Fórmula básica con corrección por población finita
        
        **Ventajas:** Simple, fácil de implementar, base teórica sólida
        **Desventajas:** Requiere marco muestral completo, puede ser costoso
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            objetivo_mas = st.radio(
                "Objetivo de estimación:",
                ["Media poblacional", "Proporción poblacional"],
                key="obj_mas"
            )
            
            if objetivo_mas == "Media poblacional":
                sigma_mas = st.number_input(
                    "Desviación estándar (σ)",
                    min_value=0.1,
                    value=20.0,
                    step=0.5,
                    key="sigma_mas"
                )
                error_mas = st.number_input(
                    "Error máximo (E)",
                    min_value=0.1,
                    value=5.0,
                    step=0.1,
                    key="error_mas"
                )
            else:
                p_mas = st.slider(
                    "Proporción estimada (p)",
                    0.01, 0.99, 0.50, 0.01,
                    key="p_mas"
                )
                error_mas = st.number_input(
                    "Margen de error (E)",
                    min_value=0.001,
                    max_value=0.5,
                    value=0.05,
                    step=0.001,
                    format="%.3f",
                    key="error_mas2"
                )
            
            confianza_mas = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%",
                key="conf_mas"
            )
            
            N_mas = st.number_input(
                "Tamaño de población (N)",
                min_value=1,
                value=10000,
                step=100,
                help="Tamaño total de la población",
                key="N_mas"
            )
        
        with col2:
            st.subheader("Resultados")
            
            alpha_mas = 1 - confianza_mas
            z_mas = norm.ppf(1 - alpha_mas/2)
            
            if objetivo_mas == "Media poblacional":
                # n₀ = (Z² × σ²) / E²
                n0_mas = (z_mas ** 2 * sigma_mas ** 2) / (error_mas ** 2)
                # n = n₀ / (1 + (n₀-1)/N)
                n_mas = n0_mas / (1 + (n0_mas - 1) / N_mas)
                n_mas = int(np.ceil(n_mas))
                
                st.metric("Tamaño de muestra (n)", f"{n_mas:,}")
                st.metric("n₀ (sin corrección)", f"{int(n0_mas):,}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("% de población", f"{(n_mas/N_mas)*100:.2f}%")
                    st.metric("Error relativo", f"{(error_mas/sigma_mas)*100:.1f}%")
                with col_b:
                    st.metric("Z crítico", f"{z_mas:.4f}")
                    st.metric("Reducción", f"{((n0_mas-n_mas)/n0_mas)*100:.1f}%")
                
                st.success(f"""
                ✅ **Interpretación:**
                
                Necesitas una muestra de **{n_mas:,} elementos** seleccionados aleatoriamente 
                de una población de {N_mas:,} para estimar la media con un error máximo de ±{error_mas} 
                y {confianza_mas*100:.0f}% de confianza.
                
                La corrección por población finita redujo la muestra en {((n0_mas-n_mas)/n0_mas)*100:.1f}%.
                """)
                
            else:  # Proporción
                # n₀ = (Z² × p × (1-p)) / E²
                n0_mas = (z_mas ** 2 * p_mas * (1 - p_mas)) / (error_mas ** 2)
                # n = n₀ / (1 + (n₀-1)/N)
                n_mas = n0_mas / (1 + (n0_mas - 1) / N_mas)
                n_mas = int(np.ceil(n_mas))
                
                st.metric("Tamaño de muestra (n)", f"{n_mas:,}")
                st.metric("n₀ (sin corrección)", f"{int(n0_mas):,}")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("% de población", f"{(n_mas/N_mas)*100:.2f}%")
                    st.metric("p estimado", f"{p_mas:.2%}")
                with col_b:
                    st.metric("Error", f"±{error_mas*100:.1f}%")
                    st.metric("Reducción", f"{((n0_mas-n_mas)/n0_mas)*100:.1f}%")
                
                st.success(f"""
                ✅ **Interpretación:**
                
                Necesitas **{n_mas:,} elementos** seleccionados aleatoriamente para estimar 
                la proporción con un margen de error de ±{error_mas*100:.1f}% y {confianza_mas*100:.0f}% de confianza.
                """)
        
        # Procedimiento
        st.markdown("---")
        st.subheader("📋 Procedimiento de Selección")
        
        with st.expander("Ver procedimiento paso a paso"):
            st.markdown(f"""
            **Pasos para implementar MAS:**
            
            1. **Enumerar la población:** Asignar un número único a cada elemento (1 a {N_mas:,})
            
            2. **Generar números aleatorios:** Usar tabla de números aleatorios, software o calculadora
            
            3. **Seleccionar {n_mas:,} elementos** sin reemplazo
            
            4. **Contactar/medir** cada elemento seleccionado
            
            **Ejemplo de selección:**
            """)
            
            # Generar muestra ejemplo
            np.random.seed(42)
            muestra_ejemplo = np.random.choice(N_mas, min(10, n_mas), replace=False) + 1
            muestra_ejemplo = sorted(muestra_ejemplo)
            
            st.code(f"Elementos seleccionados (primeros 10): {muestra_ejemplo}")
            
            st.markdown("""
            **Herramientas útiles:**
            - Python: `random.sample(range(1, N+1), n)`
            - R: `sample(1:N, n)`
            - Excel: `=ALEATORIO.ENTRE(1, N)`
            - Tabla de números aleatorios
            """)
        
        # Exportar
        df_mas = pd.DataFrame([{
            'Método': 'MAS',
            'Objetivo': objetivo_mas,
            'N (población)': N_mas,
            'n (muestra)': n_mas,
            'n₀ (sin corrección)': int(n0_mas),
            'Confianza': f"{confianza_mas*100:.0f}%",
            'Error': error_mas,
            '% muestreado': f"{(n_mas/N_mas)*100:.2f}%"
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_mas),
            "muestreo_aleatorio_simple.xlsx"
        )
    
    # ==========================================
    # 2. ESTIMACIÓN DE UNA PROPORCIÓN
    # ==========================================
    elif tipo_calculo == "📈 Estimación de una Proporción":
        st.header("Estimación de una Proporción Poblacional")
        
        st.info("""
        **Objetivo:** Estimar la proporción poblacional p con un margen de error especificado.
        
        **Fórmula:** n = (Z_{α/2})² × p × (1-p) / E²
        
        Cuando no conoces p, usa p = 0.5 (máximo conservador).
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            metodo_p = st.radio(
                "¿Tienes una estimación previa de p?",
                ["Sí, tengo una estimación", "No, usar p = 0.5 (conservador)"]
            )
            
            if metodo_p == "Sí, tengo una estimación":
                p = st.slider(
                    "Proporción estimada (p)",
                    0.01, 0.99, 0.30, 0.01,
                    help="Basado en estudios piloto o datos previos"
                )
            else:
                p = 0.5
                st.info("📌 Usando p = 0.5 (produce el tamaño de muestra más conservador)")
            
            error_prop = st.number_input(
                "Margen de error (E)",
                min_value=0.001,
                max_value=0.5,
                value=0.05,
                step=0.001,
                format="%.3f",
                help="Error expresado como proporción (ej: 0.05 = ±5%)"
            )
            
            confianza_prop = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%"
            )
            
            poblacion_prop = st.number_input(
                "Tamaño de población (N)",
                min_value=0,
                value=0,
                help="Dejar en 0 si la población es infinita",
                key="pob_prop"
            )
        
        with col2:
            st.subheader("Resultados")
            
            # Cálculo
            alpha_prop = 1 - confianza_prop
            z_prop = norm.ppf(1 - alpha_prop/2)
            
            n_prop = int(np.ceil((z_prop ** 2 * p * (1 - p)) / (error_prop ** 2)))
            
            # Corrección por población finita
            if poblacion_prop > 0 and poblacion_prop < 100000:
                n_prop_ajustado = int(np.ceil(n_prop / (1 + (n_prop - 1) / poblacion_prop)))
                st.warning(f"⚠️ Población finita detectada (N = {poblacion_prop:,})")
            else:
                n_prop_ajustado = n_prop
            
            st.metric("Tamaño de muestra requerido", f"{n_prop_ajustado:,}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Z crítico", f"{z_prop:.4f}")
                st.metric("p estimado", f"{p:.2%}")
            with col_b:
                st.metric("Error (%)", f"±{error_prop*100:.1f}%")
                if poblacion_prop > 0:
                    st.metric("% de población", f"{(n_prop_ajustado/poblacion_prop)*100:.2f}%")
            
            # Intervalo esperado
            ic_lower = max(0, p - error_prop)
            ic_upper = min(1, p + error_prop)
            
            st.success(f"""
            ✅ **Interpretación:**
            
            Con una muestra de **{n_prop_ajustado:,} observaciones**, podrás estimar la proporción 
            poblacional con un margen de error de ±{error_prop*100:.1f}%, con {confianza_prop*100:.0f}% de confianza.
            
            Si la proporción real es {p:.1%}, el intervalo será aproximadamente [{ic_lower:.1%}, {ic_upper:.1%}]
            """)
            
            if p == 0.5:
                st.info("📌 Este es el tamaño máximo necesario para cualquier valor de p")
        
        # Gráfico de sensibilidad a p
        st.markdown("---")
        st.subheader("📊 Efecto de p en el Tamaño de Muestra")
        
        p_values = np.linspace(0.01, 0.99, 100)
        n_values = []
        
        for p_val in p_values:
            n_temp = int(np.ceil((z_prop ** 2 * p_val * (1 - p_val)) / (error_prop ** 2)))
            if poblacion_prop > 0 and poblacion_prop < 100000:
                n_temp = int(np.ceil(n_temp / (1 + (n_temp - 1) / poblacion_prop)))
            n_values.append(n_temp)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(p_values, n_values, 'b-', linewidth=2)
        ax.axvline(p, color='r', linestyle='--', label=f'p usado: {p:.2f}')
        ax.axhline(n_prop_ajustado, color='r', linestyle='--', alpha=0.5)
        ax.scatter([p], [n_prop_ajustado], color='r', s=100, zorder=5)
        ax.set_xlabel('Proporción Poblacional (p)', fontsize=12)
        ax.set_ylabel('Tamaño de Muestra (n)', fontsize=12)
        ax.set_title('Tamaño de Muestra según Proporción (máximo en p=0.5)', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close()
        
        # Exportar
        df_resultados = pd.DataFrame([{
            'Tipo': 'Estimación de Proporción',
            'p': p,
            'Error': f"±{error_prop*100:.1f}%",
            'Confianza': f"{confianza_prop*100:.0f}%",
            'Z': f"{z_prop:.4f}",
            'N (final)': n_prop_ajustado,
            'Población': poblacion_prop if poblacion_prop > 0 else 'Infinita'
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_resultados),
            "tamano_muestra_proporcion.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # ==========================================
    # 3. DIFERENCIA DE MEDIAS
    # ==========================================
    elif tipo_calculo == "🔄 Diferencia de Medias (2 grupos)":
        st.header("Comparación de Medias entre Dos Grupos")
        
        st.info("""
        **Objetivo:** Detectar una diferencia mínima (Δ) entre dos medias poblacionales.
        
        **Fórmula:** n = 2 × [(Z_{α/2} + Z_{β}) × σ / Δ]²
        
        Incluye control de potencia estadística (1-β).
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            delta = st.number_input(
                "Diferencia mínima a detectar (Δ)",
                min_value=0.1,
                value=5.0,
                step=0.1,
                help="Diferencia clínicamente o prácticamente importante"
            )
            
            sigma_dif = st.number_input(
                "Desviación estándar (σ)",
                min_value=0.1,
                value=10.0,
                step=0.1,
                help="Desviación estándar común o promedio de ambos grupos"
            )
            
            alpha_dif = st.select_slider(
                "Nivel de significancia (α)",
                options=[0.01, 0.05, 0.10],
                value=0.05,
                format_func=lambda x: f"{x*100:.0f}%"
            )
            
            potencia_dif = st.select_slider(
                "Potencia estadística (1-β)",
                options=[0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
                value=0.80,
                format_func=lambda x: f"{x*100:.0f}%",
                help="Probabilidad de detectar la diferencia si existe"
            )
            
            tipo_prueba = st.radio(
                "Tipo de prueba",
                ["Bilateral (two-tailed)", "Unilateral (one-tailed)"]
            )
            
            usar_t_dif = st.checkbox(
                "Usar distribución t-Student",
                value=True,
                help="Recomendado para muestras < 30"
            )
        
        with col2:
            st.subheader("Resultados")
            
            # Tamaño del efecto
            d_cohen = delta / sigma_dif
            
            # Valores críticos
            if tipo_prueba == "Bilateral (two-tailed)":
                z_alpha_dif = norm.ppf(1 - alpha_dif/2)
            else:
                z_alpha_dif = norm.ppf(1 - alpha_dif)
            
            beta_dif = 1 - potencia_dif
            z_beta_dif = norm.ppf(1 - beta_dif)
            
            # Cálculo con Z
            n_por_grupo_z = int(np.ceil(2 * ((z_alpha_dif + z_beta_dif) * sigma_dif / delta) ** 2))
            
            # Ajuste con t si se solicita
            if usar_t_dif:
                n_iter = n_por_grupo_z
                for _ in range(50):
                    gl_dif = 2 * n_iter - 2
                    t_alpha_dif = t_dist.ppf(1 - alpha_dif/2 if tipo_prueba == "Bilateral (two-tailed)" else 1 - alpha_dif, gl_dif)
                    t_beta_dif = t_dist.ppf(1 - beta_dif, gl_dif)
                    n_new = int(np.ceil(2 * ((t_alpha_dif + t_beta_dif) * sigma_dif / delta) ** 2))
                    if abs(n_new - n_iter) <= 1:
                        break
                    n_iter = n_new
                n_por_grupo = n_new
            else:
                n_por_grupo = n_por_grupo_z
            
            # Asegurar mínimo
            n_por_grupo = max(n_por_grupo, 3)
            n_total = 2 * n_por_grupo
            
            # Mostrar resultados
            st.metric("Tamaño por grupo", f"{n_por_grupo:,}")
            st.metric("Tamaño total", f"{n_total:,}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("d de Cohen", f"{d_cohen:.3f}")
                st.metric("α", f"{alpha_dif:.2%}")
            with col_b:
                st.metric("Potencia (1-β)", f"{potencia_dif:.0%}")
                st.metric("β (Error tipo II)", f"{beta_dif:.2%}")
            
            # Clasificación del efecto
            if d_cohen < 0.2:
                efecto_tipo = "Muy pequeño 🔴"
            elif d_cohen < 0.5:
                efecto_tipo = "Pequeño 🟡"
            elif d_cohen < 0.8:
                efecto_tipo = "Mediano 🔵"
            else:
                efecto_tipo = "Grande 🟢"
            
            st.success(f"""
            ✅ **Interpretación:**
            
            Necesitas **{n_por_grupo:,} sujetos por grupo** ({n_total:,} total) para detectar 
            una diferencia de {delta} unidades con {potencia_dif*100:.0f}% de potencia y α={alpha_dif:.2%}.
            
            **Tamaño del efecto:** {efecto_tipo} (d = {d_cohen:.3f})
            """)
            
            if usar_t_dif:
                st.info(f"📌 Se usó distribución t con {2*n_por_grupo-2} grados de libertad")
        
        # Curva de potencia
        st.markdown("---")
        st.subheader("📊 Curva de Potencia Estadística")
        
        deltas_range = np.linspace(delta * 0.3, delta * 2, 100)
        potencias = []
        
        for d_temp in deltas_range:
            d_cohen_temp = d_temp / sigma_dif
            ncp = d_cohen_temp * np.sqrt(n_por_grupo / 2)
            if tipo_prueba == "Bilateral (two-tailed)":
                critico = norm.ppf(1 - alpha_dif/2)
            else:
                critico = norm.ppf(1 - alpha_dif)
            pot_temp = 1 - norm.cdf(critico - ncp)
            potencias.append(pot_temp)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(deltas_range, potencias, 'b-', linewidth=2)
        ax.axvline(delta, color='r', linestyle='--', label=f'Δ especificada: {delta}')
        ax.axhline(potencia_dif, color='g', linestyle='--', alpha=0.5, label=f'Potencia: {potencia_dif:.0%}')
        ax.scatter([delta], [potencia_dif], color='r', s=100, zorder=5)
        ax.set_xlabel('Diferencia entre Medias (Δ)', fontsize=12)
        ax.set_ylabel('Potencia Estadística (1-β)', fontsize=12)
        ax.set_title('Curva de Potencia', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim([0, 1])
        st.pyplot(fig)
        plt.close()
        
        # Exportar
        df_resultados = pd.DataFrame([{
            'Tipo': 'Diferencia de Medias',
            'Δ': delta,
            'σ': sigma_dif,
            'd Cohen': f"{d_cohen:.3f}",
            'α': alpha_dif,
            'Potencia': f"{potencia_dif:.0%}",
            'n por grupo': n_por_grupo,
            'n total': n_total,
            'Tipo prueba': tipo_prueba
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_resultados),
            "tamano_muestra_dif_medias.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # ==========================================
    # 4. DIFERENCIA DE PROPORCIONES
    # ==========================================
    else:
        st.header("Comparación de Proporciones entre Dos Grupos")
        
        st.info("""
        **Objetivo:** Detectar una diferencia entre dos proporciones poblacionales.
        
        **Fórmula:** n = [Z_{α/2}√(2p̄(1-p̄)) + Z_{β}√(p₁(1-p₁) + p₂(1-p₂))]² / (p₁ - p₂)²
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            p1 = st.slider(
                "Proporción grupo 1 (p₁)",
                0.01, 0.99, 0.40, 0.01,
                help="Proporción esperada en el grupo 1"
            )
            p2 = st.slider(
                "Proporción grupo 2 (p₂)",
                0.01, 0.99, 0.25, 0.01,
                help="Proporción esperada en el grupo 2"
            )
            
            alpha_prop2 = st.select_slider(
                "Nivel de significancia (α)",
                options=[0.01, 0.05, 0.10],
                value=0.05
            )
            
            potencia_prop2 = st.select_slider(
                "Potencia (1-β)",
                options=[0.70, 0.75, 0.80, 0.85, 0.90, 0.95],
                value=0.80
            )
        
        with col2:
            st.subheader("Resultados")
            
            # Diferencia
            dif_prop = abs(p1 - p2)
            p_promedio = (p1 + p2) / 2
            
            # Valores críticos
            z_alpha_prop2 = norm.ppf(1 - alpha_prop2/2)
            beta_prop2 = 1 - potencia_prop2
            z_beta_prop2 = norm.ppf(1 - beta_prop2)
            
            # Cálculo
            numerador = (z_alpha_prop2 * np.sqrt(2 * p_promedio * (1 - p_promedio)) + 
                        z_beta_prop2 * np.sqrt(p1*(1-p1) + p2*(1-p2)))
            n_por_grupo = int(np.ceil((numerador / dif_prop) ** 2))
            n_total = 2 * n_por_grupo
            
            st.metric("Tamaño por grupo", f"{n_por_grupo:,}")
            st.metric("Tamaño total", f"{n_total:,}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Diferencia", f"{dif_prop:.2%}")
                st.metric("α", f"{alpha_prop2:.2%}")
            with col_b:
                st.metric("Potencia", f"{potencia_prop2:.0%}")
                st.metric("p promedio", f"{p_promedio:.2%}")
            
            st.success(f"""
            ✅ **Interpretación:**
            
            Necesitas **{n_por_grupo:,} sujetos por grupo** para detectar 
            una diferencia de {dif_prop*100:.1f} puntos porcentuales con {potencia_prop2*100:.0f}% de potencia.
            """)

# ==========================================
# MÓDULO 2: POR TIPO DE MUESTREO
# ==========================================
else:  # Este 'else' cierra el bloque de opcion_principal
    
    tipo_muestreo = st.selectbox(
        "Selecciona el tipo de muestreo:",
        [
            "🎲 Muestreo Aleatorio Simple (MAS)",
            "📊 Muestreo Estratificado",
            "🏘️ Muestreo por Conglomerados",
            "📏 Muestreo Sistemático"
        ]
    )
    
    st.markdown("---")
    
    # ==========================================
    # A. MUESTREO ALEATORIO SIMPLE (MAS)
    # ==========================================
    if tipo_muestreo == "🎲 Muestreo Aleatorio Simple (MAS)":
        st.header("Muestreo Aleatorio Simple (MAS)")
        st.info("Todos los elementos tienen la misma probabilidad de ser seleccionados. Ideal para poblaciones homogéneas con marco muestral completo.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Parámetros")
            objetivo_mas = st.radio("Objetivo de la estimación:", ["Estimar Media (Promedio)", "Estimar Proporción (%)"], key="obj_mas_sample")
            
            N_mas = st.number_input("Tamaño de la Población (N)", min_value=1, value=5000, help="Total de elementos en el universo de estudio")
            confianza_mas = st.select_slider("Nivel de Confianza", [0.90, 0.95, 0.99], value=0.95, key="conf_mas_ok")
            
            if objetivo_mas == "Estimar Media (Promedio)":
                sigma_mas = st.number_input("Desviación estándar (σ)", value=20.0, help="Variabilidad estimada de la población")
                error_mas = st.number_input("Error máximo aceptable (E)", value=2.0, help="En las mismas unidades que la media")
            else:
                p_mas = st.slider("Proporción esperada (p)", 0.01, 0.99, 0.50, help="Si no se conoce, usar 0.50 para máxima varianza")
                error_mas = st.number_input("Margen de Error (E)", 0.01, 0.20, 0.05, format="%.3f", help="Ejemplo: 0.05 es 5%")

        with col2:
            st.subheader("Resultados")
            # Cálculo de Z
            alpha = 1 - confianza_mas
            z_val = norm.ppf(1 - alpha/2)
            
            # Cálculo de n0 (Muestra infinita)
            if objetivo_mas == "Estimar Media (Promedio)":
                n0 = (z_val**2 * sigma_mas**2) / error_mas**2
            else:
                n0 = (z_val**2 * p_mas * (1-p_mas)) / error_mas**2
            
            # Ajuste por Población Finita
            n_final = int(np.ceil(n0 / (1 + (n0 - 1) / N_mas)))
            
            st.metric("Tamaño de muestra (n)", f"{n_final:,}")
            
            c_a, c_b = st.columns(2)
            c_a.metric("% de la población", f"{(n_final/N_mas)*100:.2f}%")
            c_b.metric("Error Configurado", f"±{error_mas}" if objetivo_mas == "Estimar Media (Promedio)" else f"±{error_mas*100:.1f}%")
        
        st.success(f"""
        ✅ **Interpretación:** Debes seleccionar aleatoriamente **{n_final:,} elementos** de tu lista de {N_mas:,} registros.
        """)
        
        # Botón de exportación
        df_mas = pd.DataFrame([{'Método': 'MAS', 'N': N_mas, 'n': n_final, 'Confianza': confianza_mas, 'Error': error_mas}])
        st.download_button("📥 Descargar Resultado (Excel)", exportar_excel(df_mas), "calculo_mas.xlsx")

    # ==========================================
    # B. MUESTREO ESTRATIFICADO
    # ==========================================
    elif tipo_muestreo == "📊 Muestreo Estratificado":
        st.header("Muestreo Estratificado")
        st.info("Útil cuando la población se divide en subgrupos (estratos) internamente homogéneos pero diferentes entre sí.")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Configuración Global")
            objetivo_est = st.radio("Objetivo:", ["Media", "Proporción"], key="obj_est")
            num_estratos = st.slider("Número de estratos", 2, 6, 3)
            confianza_est = st.select_slider("Confianza", [0.90, 0.95, 0.99], value=0.95, key="conf_est")
            error_est = st.number_input("Error total deseado (E)", value=2.0 if objetivo_est == "Media" else 0.05)
            metodo_asignacion = st.selectbox("Tipo de Asignación:", ["Proporcional", "Óptima de Neyman", "Igual"])
        
        st.subheader("Configuración por Estrato")
        estratos_data = []
        total_N = 0
        
        # Loop para generar inputs dinámicos
        for i in range(num_estratos):
            st.markdown(f"**Estrato {i+1}**")
            cols = st.columns(3)
            with cols[0]:
                N_h = st.number_input(f"Población N_{i+1}", min_value=1, value=1000*(i+1), key=f"N_est_{i}")
            with cols[1]:
                label_v = f"Desv. Std (σ_{i+1})" if objetivo_est=='Media' else f"Proporción (p_{i+1})"
                val_h = st.number_input(label_v, value=10.0 if objetivo_est=='Media' else 0.5, key=f"v_est_{i}")
                # Si es proporción, calculamos sigma implícita
                sigma_h = val_h if objetivo_est=='Media' else np.sqrt(val_h*(1-val_h))
            with cols[2]:
                costo_h = st.number_input(f"Costo unitario", value=1.0, disabled=(metodo_asignacion != "Óptima de Neyman"), key=f"c_est_{i}")
            
            estratos_data.append({'Estrato': i+1, 'N_h': N_h, 'sigma_h': sigma_h, 'costo_h': costo_h})
            total_N += N_h

        # Cálculos
        z_est = norm.ppf(1 - (1-confianza_est)/2)
        D = (error_est**2) / (z_est**2)
        
        suma_Nh_sigmah = sum([d['N_h'] * d['sigma_h'] for d in estratos_data])
        suma_Nh_sigmah2 = sum([d['N_h'] * d['sigma_h']**2 for d in estratos_data])
        
        # Fórmula del tamaño total n
        if metodo_asignacion == "Proporcional":
            n_total = suma_Nh_sigmah2 / (total_N**2 * D + suma_Nh_sigmah2)
        elif metodo_asignacion == "Óptima de Neyman":
            # Simplificación asumiendo costos iguales para la fórmula básica de Neyman mostrada aquí
            n_total = (suma_Nh_sigmah**2) / (total_N**2 * D + suma_Nh_sigmah2)
        else: # Asignación Igual (aproximación simple)
            n_total = 30 * num_estratos 

        n_total = int(np.ceil(n_total))
        
        st.divider()
        c1, c2 = st.columns(2)
        c1.metric("Tamaño de Muestra Total (n)", f"{n_total:,}")
        c1.metric("Población Total (N)", f"{total_N:,}")
        
        # Distribución de la muestra (n_h)
        asignaciones = []
        if metodo_asignacion == "Proporcional":
            for d in estratos_data: asignaciones.append(int(n_total * (d['N_h']/total_N)))
        elif metodo_asignacion == "Óptima de Neyman":
            for d in estratos_data: asignaciones.append(int(n_total * (d['N_h']*d['sigma_h'])/suma_Nh_sigmah))
        else:
            asignaciones = [int(n_total/num_estratos)] * num_estratos
            
        # Tabla de resultados
        df_res = pd.DataFrame({
            'Estrato': [d['Estrato'] for d in estratos_data],
            'Población (N_h)': [d['N_h'] for d in estratos_data],
            'Muestra Asignada (n_h)': asignaciones,
            '% de Muestreo': [f"{(n/N)*100:.1f}%" for n, N in zip(asignaciones, [d['N_h'] for d in estratos_data])]
        })
        c2.dataframe(df_res, hide_index=True)
        st.download_button("📥 Descargar Asignación (Excel)", exportar_excel(df_res), "asignacion_estratificada.xlsx")

    # ==========================================
    # C. MUESTREO POR CONGLOMERADOS
    # ==========================================
    elif tipo_muestreo == "🏘️ Muestreo por Conglomerados":
        st.header("Muestreo por Conglomerados")
        st.info("Se seleccionan grupos completos (escuelas, cajas, manzanas) en lugar de individuos. Es más barato pero menos preciso (DEFF > 1).")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Datos de Población")
            M_total = st.number_input("Número total de conglomerados (M)", value=200, help="Total de grupos disponibles")
            tam_prom = st.number_input("Tamaño promedio del conglomerado", value=50, help="Promedio de elementos dentro de cada grupo")
            icc = st.number_input("Coeficiente Correlación Intraclase (ICC)", 0.0, 1.0, 0.05, help="Qué tan parecidos son los elementos dentro de un grupo. 0=distintos, 1=idénticos")
            
            st.subheader("Parámetros de Estimación")
            objetivo_cong = st.radio("Objetivo", ["Media", "Proporción"], key="obj_cong")
            
            if objetivo_cong == "Media":
                sigma_tot = st.number_input("Desviación estándar global (σ)", value=20.0)
                error_cong = st.number_input("Error máximo (E)", value=2.0)
            else:
                p_cong = st.slider("Proporción estimada (p)", 0.01, 0.99, 0.50)
                error_cong = st.number_input("Error máximo (E)", 0.01, 0.2, 0.05)
                
        with col2:
            st.subheader("Resultados")
            # 1. Calcular Efecto de Diseño (DEFF)
            deff = 1 + (tam_prom - 1) * icc
            
            # 2. Calcular n como si fuera MAS
            z_val = 1.96 # Asumiendo 95%
            if objetivo_cong == "Media":
                n_mas = (z_val**2 * sigma_tot**2) / error_cong**2
            else:
                n_mas = (z_val**2 * p_cong * (1-p_cong)) / error_cong**2
            
            # 3. Ajustar n con DEFF
            n_complex = n_mas * deff
            
            # 4. Calcular número de conglomerados (m)
            m_clusters = int(np.ceil(n_complex / tam_prom))
            
            st.metric("Conglomerados a seleccionar (m)", f"{m_clusters:,}")
            st.metric("Total de elementos (n)", f"{m_clusters * int(tam_prom):,}")
            st.metric("Efecto de Diseño (DEFF)", f"{deff:.2f}")
            
            if deff > 2:
                st.warning("⚠️ El DEFF es alto. Los elementos dentro de los grupos son muy parecidos. Necesitas mucha más muestra que en un aleatorio simple.")
            
        st.success(f"Plan de acción: De tus {M_total} conglomerados, selecciona aleatoriamente **{m_clusters}** y censa a todos sus elementos.")

    # ==========================================
    # D. MUESTREO SISTEMÁTICO
    # ==========================================
    else:  # Sistemático
        st.header("Muestreo Sistemático")
        st.info("Se elige un punto de partida aleatorio y luego se selecciona cada k-ésimo elemento de la lista ordenada.")
        
        col1, col2 = st.columns(2)
        with col1:
            N_sys = st.number_input("Tamaño de la Población (N)", value=5000)
            n_deseado = st.number_input("Tamaño de muestra deseado (n)", value=384, help="Calcula este valor usando el módulo de 'Estimación de una Media/Proporción' primero")
        
        with col2:
            # Calcular intervalo k
            if n_deseado > 0:
                k = int(N_sys / n_deseado)
            else:
                k = 0
            
            # Arranque aleatorio
            if k > 0:
                inicio = np.random.randint(1, k+1)
            else:
                inicio = 0
            
            st.metric("Intervalo de salto (k)", k)
            st.metric("Arranque aleatorio (r)", inicio)
            
            st.markdown(f"""
            **Instrucciones:**
            1. Ordena tu lista de población del 1 al {N_sys}.
            2. Selecciona el sujeto número **{inicio}**.
            3. Selecciona el sujeto **{inicio} + {k} = {inicio+k}**.
            4. Continúa sumando {k} hasta completar la muestra.
            """)

        st.markdown("---")
        st.markdown("### 📄 Generar Lista de Selección")
        if st.button("Generar lista de números a muestrear"):
            if k > 0:
                muestra = [inicio + i*k for i in range(n_deseado)]
                # Filtramos si alguno se pasa de N (por redondeos)
                muestra = [x for x in muestra if x <= N_sys]
                
                st.write(f"Mostrando primeros 20 números de identificación:")
                st.code(f"{muestra[:20]} ...")
                
                st.download_button("📥 Descargar lista completa (.txt)", str(muestra), "seleccion_sistematica.txt")
            else:
                st.error("El tamaño de muestra debe ser mayor a 0.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<p>🔢 Calculadora Avanzada de Tamaño de Muestra</p>
<p><small>Incluye: Estimación de Medias y Proporciones | 4 Tipos de Muestreo</small></p>
<p><small>Versión 2.0 - Herramienta educativa y profesional</small></p>
</div>
""", unsafe_allow_html=True)
