import streamlit as st
import numpy as np
import pandas as pd
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
            
            **Ejemplo:** 
            - Si E = 2 kg, tu estimación estará a ±2 kg del valor real
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
            
            **Expresión:** 
            - Decimal: p = 0.30 (30%)
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
    # MUESTREO ESTRATIFICADO
    # ==========================================
    elif tipo_muestreo == "📊 Muestreo Estratificado":
        st.header("Muestreo Estratificado")
        
        st.info("""
        **Características:**
        - Población dividida en estratos homogéneos internamente
        - Muestreo independiente dentro de cada estrato
        - Mayor precisión que MAS si los estratos son homogéneos
        
        **Ventajas:** Mayor precisión, estimaciones por subgrupo
        **Desventajas:** Requiere conocer la estructura poblacional
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros Generales")
            
            objetivo_est = st.radio(
                "Objetivo:",
                ["Media", "Proporción"],
                key="obj_est"
            )
            
            num_estratos = st.slider(
                "Número de estratos",
                2, 6, 3,
                help="Ejemplo: regiones, grupos de edad, niveles socioeconómicos"
            )
            
            confianza_est = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%",
                key="conf_est"
            )
            
            error_est = st.number_input(
                "Error máximo (E)",
                min_value=0.01,
                value=5.0 if objetivo_est == "Media" else 0.05,
                step=0.01,
                key="error_est"
            )
            
            metodo_asignacion = st.selectbox(
                "Método de asignación:",
                ["Proporcional", "Óptima de Neyman", "Igual"],
                help="Proporcional: según tamaño | Óptima: según variabilidad | Igual: mismo n en cada estrato"
            )
        
        # Tabla de estratos
        st.markdown("---")
        st.subheader("Información por Estrato")
        
        estratos_data = []
        total_N = 0
        
        for i in range(num_estratos):
            st.markdown(f"**Estrato {i+1}:**")
            cols = st.columns(3)
            
            with cols[0]:
                N_h = st.number_input(
                    f"N{i+1} (tamaño)",
                    min_value=1,
                    value=1000 * (i+1),
                    step=100,
                    key=f"N_est_{i}"
                )
            
            with cols[1]:
                if objetivo_est == "Media":
                    sigma_h = st.number_input(
                        f"σ{i+1}",
                        min_value=0.1,
                        value=10.0 + i*2,
                        step=0.5,
                        key=f"sigma_est_{i}"
                    )
                else:
                    sigma_h = st.slider(
                        f"p{i+1}",
                        0.01, 0.99, 0.3 + i*0.1,
                        0.01,
                        key=f"p_est_{i}"
                    )
                    sigma_h = np.sqrt(sigma_h * (1 - sigma_h))
            
            with cols[2]:
                if metodo_asignacion == "Óptima de Neyman":
                    costo_h = st.number_input(
                        f"Costo{i+1}",
                        min_value=1.0,
                        value=10.0,
                        step=1.0,
                        key=f"costo_est_{i}",
                        help="Costo relativo por unidad"
                    )
                else:
                    costo_h = 1.0
            
            estratos_data.append({
                'Estrato': i+1,
                'N_h': N_h,
                'sigma_h': sigma_h,
                'costo_h': costo_h
            })
            total_N += N_h
        
        st.markdown("---")
        
        # Cálculos
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.subheader("Cálculo del Tamaño Total")
            
            alpha_est = 1 - confianza_est
            z_est = norm.ppf(1 - alpha_est/2)
            
            # Calcular n total según método
            if metodo_asignacion == "Proporcional":
                # n₀ = (Σ N_h × σ_h²) / (N²D + Σ N_h × σ_h²)
                # donde D = E²/Z²
                suma_Nh_sigmah2 = sum([d['N_h'] * d['sigma_h']**2 for d in estratos_data])
                D = (error_est ** 2) / (z_est ** 2)
                n_total = suma_Nh_sigmah2 / (total_N**2 * D + suma_Nh_sigmah2)
                n_total = int(np.ceil(n_total))
                
            elif metodo_asignacion == "Óptima de Neyman":
                # n₀ = (Σ N_h × σ_h)² / (N²D + Σ N_h × σ_h²)
                suma_Nh_sigmah = sum([d['N_h'] * d['sigma_h'] for d in estratos_data])
                suma_Nh_sigmah2 = sum([d['N_h'] * d['sigma_h']**2 for d in estratos_data])
                D = (error_est ** 2) / (z_est ** 2)
                n_total = (suma_Nh_sigmah ** 2) / (total_N**2 * D + suma_Nh_sigmah2)
                n_total = int(np.ceil(n_total))
                
            else:  # Igual
                n_por_estrato_base = 30
                n_total = n_por_estrato_base * num_estratos
            
            st.metric("Tamaño total (n)", f"{n_total:,}")
            st.metric("Población (N)", f"{total_N:,}")
            st.metric("% muestreado", f"{(n_total/total_N)*100:.2f}%")
        
        with col_res2:
            st.subheader("Asignación por Estrato")
            
            # Asignar a cada estrato
            asignaciones = []
            
            if metodo_asignacion == "Proporcional":
                for d in estratos_data:
                    W_h = d['N_h'] / total_N  # Peso del estrato
                    n_h = int(np.ceil(n_total * W_h))
                    n_h = min(n_h, d['N_h'])  # No exceder población del estrato
                    asignaciones.append(n_h)
                    
            elif metodo_asignacion == "Óptima de Neyman":
                suma_Nh_sigmah = sum([d['N_h'] * d['sigma_h'] for d in estratos_data])
                for d in estratos_data:
                    n_h = int(np.ceil(n_total * (d['N_h'] * d['sigma_h']) / suma_Nh_sigmah))
                    n_h = min(n_h, d['N_h'])
                    asignaciones.append(n_h)
                    
            else:  # Igual
                n_base = n_total // num_estratos
                asignaciones = [n_base] * num_estratos
            
            # Ajustar si la suma no coincide exactamente
            diferencia = n_total - sum(asignaciones)
            if diferencia > 0:
                asignaciones[0] += diferencia
            
            # Mostrar tabla
            df_estratos = pd.DataFrame([{
                'Estrato': d['Estrato'],
                'N_h': d['N_h'],
                'n_h': asignaciones[i],
                '% muestreado': f"{(asignaciones[i]/d['N_h'])*100:.2f}%",
                'Peso': f"{(d['N_h']/total_N)*100:.1f}%"
            } for i, d in enumerate(estratos_data)])
            
            st.dataframe(df_estratos, use_container_width=True)
        
        # Gráfico
        st.markdown("---")
        st.subheader("📊 Visualización de la Asignación")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico 1: Tamaños poblacionales vs muestrales
        estratos_nombres = [f"E{i+1}" for i in range(num_estratos)]
        x_pos = np.arange(len(estratos_nombres))
        
        N_values = [d['N_h'] for d in estratos_data]
        n_values = asignaciones
        
        width = 0.35
        ax1.bar(x_pos - width/2, N_values, width, label='Población (N_h)', alpha=0.8)
        ax1.bar(x_pos + width/2, n_values, width, label='Muestra (n_h)', alpha=0.8)
        ax1.set_xlabel('Estratos')
        ax1.set_ylabel('Cantidad')
        ax1.set_title('Distribución Poblacional vs Muestral')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(estratos_nombres)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Gráfico 2: Proporción de muestreo
        proporciones = [(n_values[i]/N_values[i])*100 for i in range(num_estratos)]
        colors = plt.cm.viridis(np.linspace(0, 1, num_estratos))
        ax2.bar(estratos_nombres, proporciones, color=colors, alpha=0.8)
        ax2.set_xlabel('Estratos')
        ax2.set_ylabel('% Muestreado')
        ax2.set_title('Fracción de Muestreo por Estrato')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Interpretación
        st.success(f"""
        ✅ **Interpretación:**
        
        Con **muestreo estratificado {metodo_asignacion.lower()}**, necesitas un total de **{n_total:,} elementos** 
        distribuidos en {num_estratos} estratos para estimar con un error de ±{error_est} 
        y {confianza_est*100:.0f}% de confianza.
        
        Este método es más eficiente que MAS cuando los estratos son homogéneos internamente.
        """)
        
        # Procedimiento
        with st.expander("📋 Procedimiento de Implementación"):
            st.markdown(f"""
            **Pasos para implementar Muestreo Estratificado:**
            
            1. **Identificar y definir estratos** basados en características relevantes
            
            2. **Determinar tamaño de cada estrato:**
            """)
            for i, d in enumerate(estratos_data):
                st.markdown(f"   - Estrato {i+1}: N = {d['N_h']:,}, seleccionar n = {asignaciones[i]:,}")
            
            st.markdown("""
            3. **Aplicar MAS dentro de cada estrato** de forma independiente
            
            4. **Combinar resultados** usando pesos proporcionales:
            """)
            st.latex(r"\bar{y}_{est} = \sum_{h=1}^{L} W_h \bar{y}_h")
            st.latex(r"W_h = \frac{N_h}{N}")
        
        # Exportar
        st.download_button(
            "📥 Descargar asignación (Excel)",
            exportar_excel(df_estratos),
            "muestreo_estratificado.xlsx"
        )
    
    # ==========================================
    # MUESTREO POR CONGLOMERADOS
    # ==========================================
    elif tipo_muestreo == "🏘️ Muestreo por Conglomerados":
        st.header("Muestreo por Conglomerados")
        
        st.info("""
        **Características:**
        - Población dividida en conglomerados (grupos naturales)
        - Se seleccionan conglomerados completos aleatoriamente
        - Útil cuando no existe marco muestral de elementos individuales
        
        **Ventajas:** Económico, práctico para poblaciones dispersas
        **Desventajas:** Menor precisión que MAS (efecto de diseño > 1)
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            tipo_conglom = st.radio(
                "Tipo de muestreo:",
                ["Una etapa (conglomerados completos)", "Dos etapas (submuestreo dentro)"],
                key="tipo_cong"
            )
            
            M_total = st.number_input(
                "Número total de conglomerados (M)",
                min_value=2,
                value=200,
                step=10,
                help="Ejemplo: escuelas, manzanas, localidades"
            )
            
            tamaño_promedio = st.number_input(
                "Tamaño promedio por conglomerado (M̄)",
                min_value=1,
                value=50,
                step=5,
                help="Número promedio de elementos por conglomerado"
            )
            
            objetivo_cong = st.radio(
                "Estimar:",
                ["Media", "Proporción"],
                key="obj_cong"
            )
            
            if objetivo_cong == "Media":
                sigma_intra = st.number_input(
                    "Varianza intra-conglomerado (σ²_w)",
                    min_value=0.1,
                    value=100.0,
                    step=1.0,
                    help="Variabilidad dentro de conglomerados"
                )
                sigma_entre = st.number_input(
                    "Varianza entre-conglomerados (σ²_b)",
                    min_value=0.0,
                    value=50.0,
                    step=1.0,
                    help="Variabilidad entre medias de conglomerados"
                )
                error_cong = st.number_input(
                    "Error máximo (E)",
                    min_value=0.1,
                    value=5.0,
                    step=0.1,
                    key="error_cong"
                )
            else:
                p_cong = st.slider(
                    "Proporción estimada (p)",
                    0.01, 0.99, 0.50, 0.01,
                    key="p_cong"
                )
                error_cong = st.number_input(
                    "Margen de error (E)",
                    min_value=0.001,
                    max_value=0.5,
                    value=0.05,
                    step=0.001,
                    format="%.3f",
                    key="error_cong2"
                )
            
            confianza_cong = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%",
                key="conf_cong"
            )
            
            if tipo_conglom == "Dos etapas (submuestreo dentro)":
                tasa_subm = st.slider(
                    "Tasa de submuestreo (% elementos por conglomerado)",
                    10, 100, 50, 5,
                    help="% de elementos a muestrear dentro de cada conglomerado seleccionado"
                )
            else:
                tasa_subm = 100
        
        with col2:
            st.subheader("Resultados")
            
            alpha_cong = 1 - confianza_cong
            z_cong = norm.ppf(1 - alpha_cong/2)
            
            N_total = M_total * tamaño_promedio
            
            if objetivo_cong == "Media":
                # Calcular ICC (Coeficiente de Correlación Intraclase)
                sigma_total = sigma_intra + sigma_entre
                rho = sigma_entre / sigma_total if sigma_total > 0 else 0
                
                # Efecto de diseño (DEFF)
                deff = 1 + (tamaño_promedio - 1) * rho
                
                # n_mas = (Z² × σ²_total) / E²
                n_mas = (z_cong ** 2 * sigma_total) / (error_cong ** 2)
                
                # n_cluster = n_mas × DEFF
                n_efectivo = n_mas * deff
                
                # Número de conglomerados
                m_clusters = int(np.ceil(n_efectivo / (tamaño_promedio * (tasa_subm/100))))
                m_clusters = min(m_clusters, M_total)
                
                n_por_cluster = int((tamaño_promedio * tasa_subm) / 100)
                n_total_final = m_clusters * n_por_cluster
                
            else:  # Proporción
                # Asumir rho moderado para proporciones
                rho = 0.05
                deff = 1 + (tamaño_promedio - 1) * rho
                
                # n_mas
                n_mas = (z_cong ** 2 * p_cong * (1 - p_cong)) / (error_cong ** 2)
                
                # n con efecto de diseño
                n_efectivo = n_mas * deff
                
                # Conglomerados necesarios
                m_clusters = int(np.ceil(n_efectivo / (tamaño_promedio * (tasa_subm/100))))
                m_clusters = min(m_clusters, M_total)
                
                n_por_cluster = int((tamaño_promedio * tasa_subm) / 100)
                n_total_final = m_clusters * n_por_cluster
            
            st.metric("Conglomerados a seleccionar (m)", f"{m_clusters:,}")
            st.metric("Elementos por conglomerado", f"{n_por_cluster:,}")
            st.metric("Total de elementos", f"{n_total_final:,}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("DEFF (Efecto de diseño)", f"{deff:.3f}")
                st.metric("ICC (ρ)", f"{rho:.4f}")
            with col_b:
                st.metric("% de conglomerados", f"{(m_clusters/M_total)*100:.2f}%")
                st.metric("% de población", f"{(n_total_final/N_total)*100:.2f}%")
            
            if deff > 2:
                st.warning(f"⚠️ DEFF alto ({deff:.2f}): Los conglomerados son muy homogéneos internamente. Considera aumentar el número de conglomerados.")
            elif deff > 1.5:
                st.info(f"📌 DEFF moderado ({deff:.2f}): Pérdida aceptable de eficiencia por conglomeración.")
            else:
                st.success(f"✅ DEFF bajo ({deff:.2f}): Conglomerados relativamente heterogéneos.")
            
            st.success(f"""
            ✅ **Interpretación:**
            
            Selecciona **{m_clusters} conglomerados** de los {M_total} disponibles.
            
            {"Muestrea **todos** los elementos en cada conglomerado seleccionado." if tasa_subm == 100 
             else f"Muestrea **{tasa_subm}% de los elementos** ({n_por_cluster}) en cada conglomerado seleccionado."}
            
            Total: **{n_total_final:,} elementos** para estimar con error ±{error_cong}.
            """)
        
        # Visualización
        st.markdown("---")
        st.subheader("📊 Estructura del Muestreo por Conglomerados")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Mostrar solo algunos conglomerados para visualizar
        num_mostrar = min(10, M_total)
        seleccionados = list(range(m_clusters))
        no_seleccionados = list(range(m_clusters, num_mostrar))
        
        for i in range(num_mostrar):
            y_pos = num_mostrar - i
            if i in seleccionados:
                color = 'green'
                alpha = 0.7
                label = f"C{i+1} (✓)" if i < 3 else f"C{i+1}"
            else:
                color = 'lightgray'
                alpha = 0.3
                label = f"C{i+1}"
            
            # Dibujar rectángulo del conglomerado
            rect = plt.Rectangle((0, y_pos-0.4), 10, 0.8,
                                facecolor=color, edgecolor='black',
                                linewidth=2, alpha=alpha)
            ax.add_patch(rect)
            ax.text(-0.5, y_pos, label, ha='right', va='center',
                   fontsize=10, fontweight='bold')
            
            # Dibujar elementos dentro (puntos)
            if i in seleccionados:
                n_elementos = n_por_cluster
                x_positions = np.linspace(0.5, 9.5, min(n_elementos, 20))
                ax.scatter(x_positions, [y_pos]*len(x_positions),
                          color='darkgreen', s=50, zorder=5)
        
        ax.set_xlim(-2, 11)
        ax.set_ylim(0, num_mostrar + 1)
        ax.set_xlabel('Elementos dentro del conglomerado', fontsize=12)
        ax.set_ylabel('Conglomerados', fontsize=12)
        ax.set_title(f'Muestreo por Conglomerados: {m_clusters} de {M_total} conglomerados seleccionados',
                    fontsize=14, fontweight='bold')
        ax.grid(False)
        ax.set_yticks([])
        
        # Leyenda
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Conglomerados seleccionados'),
            Patch(facecolor='lightgray', alpha=0.3, label='Conglomerados no seleccionados')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Procedimiento
        with st.expander("📋 Procedimiento de Implementación"):
            st.markdown(f"""
            **Pasos para Muestreo por Conglomerados:**
            
            1. **Listar todos los conglomerados** (M = {M_total})
            
            2. **Seleccionar aleatoriamente {m_clusters} conglomerados** usando MAS
               ```python
               import random
               conglomerados_seleccionados = random.sample(range(1, {M_total+1}), {m_clusters})
               ```
            
            3. **Para cada conglomerado seleccionado:**
               {"- Incluir TODOS los elementos (censo completo del conglomerado)" if tasa_subm == 100
                else f"- Seleccionar aleatoriamente {n_por_cluster} elementos ({tasa_subm}% del total)"}
            
            4. **Calcular estimadores:**
            """)
            
            if tipo_conglom == "Una etapa (conglomerados completos)":
                st.latex(r"\bar{y} = \frac{1}{m} \sum_{i=1}^{m} \bar{y}_i")
                st.markdown("Donde $\\bar{y}_i$ es la media del conglomerado i")
            else:
                st.latex(r"\bar{y} = \frac{\sum_{i=1}^{m} M_i \bar{y}_i}{\sum_{i=1}^{m} M_i}")
                st.markdown("Donde $M_i$ es el tamaño del conglomerado i")
            
            st.markdown(f"""
            **Ventajas en este caso:**
            - Ahorro de costos: solo visitas {m_clusters} ubicaciones
            - Marco muestral simplificado: solo necesitas lista de conglomerados
            
            **Consideraciones:**
            - DEFF = {deff:.2f}: la muestra es {deff:.2f}× menos eficiente que MAS
            - Compensado por el ahorro logístico y económico
            """)
        
        # Comparación con MAS
        st.markdown("---")
        st.subheader("⚖️ Comparación con MAS")
        
        if objetivo_cong == "Media":
            n_mas_equiv = int(np.ceil((z_cong ** 2 * sigma_total) / (error_cong ** 2)))
        else:
            n_mas_equiv = int(np.ceil((z_cong ** 2 * p_cong * (1-p_cong)) / (error_cong ** 2)))
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.markdown("**Muestreo Aleatorio Simple**")
            st.metric("Elementos necesarios", f"{n_mas_equiv:,}")
            st.metric("Ubicaciones a visitar", f"~{n_mas_equiv:,}")
            st.info("Máxima eficiencia estadística pero costoso logísticamente")
        
        with col_comp2:
            st.markdown("**Muestreo por Conglomerados**")
            st.metric("Elementos necesarios", f"{n_total_final:,}")
            st.metric("Ubicaciones a visitar", f"{m_clusters:,}")
            st.success(f"Ahorro de {((n_mas_equiv-m_clusters)/n_mas_equiv)*100:.1f}% en ubicaciones")
        
        # Exportar
        df_conglom = pd.DataFrame([{
            'Método': 'Conglomerados',
            'Tipo': tipo_conglom,
            'M (total)': M_total,
            'm (seleccionados)': m_clusters,
            'Tamaño promedio': tamaño_promedio,
            'n por conglomerado': n_por_cluster,
            'n total': n_total_final,
            'DEFF': f"{deff:.3f}",
            'ICC (ρ)': f"{rho:.4f}"
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_conglom),
            "muestreo_conglomerados.xlsx"
        )
    
    # ==========================================
    # MUESTREO SISTEMÁTICO
    # ==========================================
    else:  # Muestreo Sistemático
        st.header("Muestreo Sistemático")
        
        st.info("""
        **Características:**
        - Selección cada k-ésimo elemento de la lista
        - Inicio aleatorio, después sistemático
        - Equivalente a MAS si no hay periodicidad en la población
        
        **Ventajas:** Simple, rápido, distribución espacial uniforme
        **Desventajas:** Problemas si existe periodicidad, difícil calcular varianza
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            
            N_sist = st.number_input(
                "Tamaño de población (N)",
                min_value=1,
                value=5000,
                step=100,
                key="N_sist"
            )
            
            objetivo_sist = st.radio(
                "Objetivo:",
                ["Media", "Proporción"],
                key="obj_sist"
            )
            
            if objetivo_sist == "Media":
                sigma_sist = st.number_input(
                    "Desviación estándar (σ)",
                    min_value=0.1,
                    value=20.0,
                    step=0.5,
                    key="sigma_sist"
                )
                error_sist = st.number_input(
                    "Error máximo (E)",
                    min_value=0.1,
                    value=3.0,
                    step=0.1,
                    key="error_sist"
                )
            else:
                p_sist = st.slider(
                    "Proporción estimada (p)",
                    0.01, 0.99, 0.50, 0.01,
                    key="p_sist"
                )
                error_sist = st.number_input(
                    "Margen de error (E)",
                    min_value=0.001,
                    max_value=0.5,
                    value=0.05,
                    step=0.001,
                    format="%.3f",
                    key="error_sist2"
                )
            
            confianza_sist = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%",
                key="conf_sist"
            )
            
            periodicidad = st.checkbox(
                "¿Existe periodicidad conocida en la población?",
                value=False,
                help="Ejemplo: patrón semanal, ciclos estacionales"
            )
            
            if periodicidad:
                periodo = st.number_input(
                    "Longitud del período",
                    min_value=2,
                    value=7,
                    step=1,
                    help="Ejemplo: 7 para patrón semanal"
                )
                ajuste_periodo = 1.2  # Factor de ajuste
            else:
                periodo = None
                ajuste_periodo = 1.0
        
        with col2:
            st.subheader("Resultados")
            
            alpha_sist = 1 - confianza_sist
            z_sist = norm.ppf(1 - alpha_sist/2)
            
            # Calcular n como si fuera MAS
            if objetivo_sist == "Media":
                n0_sist = (z_sist ** 2 * sigma_sist ** 2) / (error_sist ** 2)
            else:
                n0_sist = (z_sist ** 2 * p_sist * (1 - p_sist)) / (error_sist ** 2)
            
            # Corrección por población finita
            n_sist = n0_sist / (1 + (n0_sist - 1) / N_sist)
            n_sist = int(np.ceil(n_sist * ajuste_periodo))
            n_sist = min(n_sist, N_sist)
            
            # Calcular k (intervalo de selección)
            k = int(N_sist / n_sist)
            n_sist_ajustado = int(N_sist / k)  # Ajustar n para que sea exacto
            
            # Inicio aleatorio
            np.random.seed()
            inicio_aleatorio = np.random.randint(1, k+1)
            
            st.metric("Tamaño de muestra (n)", f"{n_sist_ajustado:,}")
            st.metric("Intervalo de selección (k)", f"{k:,}")
            st.metric("Inicio aleatorio sugerido", f"{inicio_aleatorio}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("% de población", f"{(n_sist_ajustado/N_sist)*100:.2f}%")
                st.metric("Z crítico", f"{z_sist:.4f}")
            with col_b:
                st.metric("Primera selección", f"#{inicio_aleatorio}")
                st.metric("Última selección", f"#{inicio_aleatorio + (n_sist_ajustado-1)*k}")
            
            if periodicidad:
                if k % periodo == 0 or periodo % k == 0:
                    st.error(f"""
                    ⚠️ **ADVERTENCIA CRÍTICA:**
                    
                    k={k} y período={periodo} son múltiplos. Esto causará sesgo severo.
                    
                    **Solución:** Ajusta k manualmente o usa muestreo estratificado.
                    """)
                else:
                    st.warning(f"⚠️ Periodicidad detectada (período={periodo}). Se aplicó ajuste del {(ajuste_periodo-1)*100:.0f}%.")
            else:
                st.success(f"""
                ✅ **Interpretación:**
                
                Selecciona cada **{k}-ésimo elemento** comenzando desde una posición aleatoria 
                entre 1 y {k}. Por ejemplo, si inicias en {inicio_aleatorio}:
                
                Elementos: {inicio_aleatorio}, {inicio_aleatorio+k}, {inicio_aleatorio+2*k}, ...
                
                Total: **{n_sist_ajustado:,} elementos** para estimar con error ±{error_sist}.
                """)
        
        # Visualización de la selección
        st.markdown("---")
        st.subheader("📊 Patrón de Selección Sistemática")
        
        # Generar las primeras selecciones para mostrar
        num_mostrar = min(100, n_sist_ajustado)
        selecciones = [inicio_aleatorio + i*k for i in range(num_mostrar)]
        
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Mostrar población como línea
        poblacion = np.arange(1, min(N_sist, 1000) + 1)
        y_base = np.zeros(len(poblacion))
        
        ax.scatter(poblacion, y_base, c='lightgray', s=5, alpha=0.5, label='Población')
        
        # Marcar elementos seleccionados
        selecciones_mostrar = [s for s in selecciones if s <= min(N_sist, 1000)]
        ax.scatter(selecciones_mostrar, [0]*len(selecciones_mostrar),
                  c='red', s=50, marker='^', label='Seleccionados', zorder=5)
        
        # Marcar inicio
        ax.scatter([inicio_aleatorio], [0], c='green', s=200, marker='*',
                  label='Inicio aleatorio', zorder=6)
        
        ax.set_xlabel('Número de elemento en la población', fontsize=12)
        ax.set_title(f'Muestreo Sistemático: k={k}, inicio={inicio_aleatorio}',
                    fontsize=14, fontweight='bold')
        ax.set_ylim(-0.5, 0.5)
        ax.set_yticks([])
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3, axis='x')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Procedimiento paso a paso
        st.markdown("---")
        st.subheader("📋 Procedimiento de Implementación")
        
        col_proc1, col_proc2 = st.columns([1, 1])
        
        with col_proc1:
            st.markdown(f"""
            **Pasos:**
            
            1. **Calcular k** (intervalo):
               - k = N / n = {N_sist:,} / {n_sist_ajustado:,} = **{k}**
            
            2. **Seleccionar inicio aleatorio** (r) entre 1 y k:
               - r = **{inicio_aleatorio}** (generado aleatoriamente)
            
            3. **Seleccionar elementos**:
               - r = {inicio_aleatorio}
               - r + k = {inicio_aleatorio + k}
               - r + 2k = {inicio_aleatorio + 2*k}
               - r + 3k = {inicio_aleatorio + 3*k}
               - ...
               - r + (n-1)k = {inicio_aleatorio + (n_sist_ajustado-1)*k}
            
            4. **Medir/encuestar** los {n_sist_ajustado:,} elementos seleccionados
            """)
        
        with col_proc2:
            st.markdown("**Código de ejemplo (Python):**")
            codigo = f"""
# Parámetros
N = {N_sist}
n = {n_sist_ajustado}
k = {k}

# Inicio aleatorio
import random
r = random.randint(1, k)
# r = {inicio_aleatorio} (ejemplo)

# Generar muestra
muestra = [r + i*k for i in range(n)]

# Primeros 10 elementos:
print(muestra[:10])
# [{', '.join(map(str, selecciones[:10]))}...]
            """
            st.code(codigo, language='python')
        
        # Generar lista completa
        with st.expander("📄 Ver lista completa de elementos a seleccionar"):
            todas_selecciones = [inicio_aleatorio + i*k for i in range(n_sist_ajustado)]
            
            # Mostrar en columnas
            num_cols = 5
            elementos_por_col = int(np.ceil(len(todas_selecciones) / num_cols))
            
            cols = st.columns(num_cols)
            for idx, col in enumerate(cols):
                inicio_idx = idx * elementos_por_col
                fin_idx = min((idx + 1) * elementos_por_col, len(todas_selecciones))
                elementos_mostrar = todas_selecciones[inicio_idx:fin_idx]
                
                with col:
                    for elem in elementos_mostrar:
                        st.text(f"#{elem}")
            
            # Botón de descarga
            lista_texto = "\n".join([f"Elemento #{s}" for s in todas_selecciones])
            st.download_button(
                "📥 Descargar lista completa (.txt)",
                lista_texto,
                f"muestra_sistematica_k{k}_r{inicio_aleatorio}.txt",
                "text/plain"
            )
        
        # Ventajas y limitaciones
        st.markdown("---")
        col_vent, col_lim = st.columns(2)
        
        with col_vent:
            st.subheader("✅ Ventajas")
            st.markdown("""
            - **Simplicidad:** Fácil de implementar en campo
            - **Distribución uniforme:** Cobertura espacial/temporal equilibrada
            - **Rapidez:** No requiere tabla de números aleatorios
            - **Costo:** Eficiente logísticamente
            """)
        
        with col_lim:
            st.subheader("⚠️ Limitaciones")
            st.markdown("""
            - **Periodicidad:** Riesgo de sesgo si hay patrones cíclicos
            - **Varianza:** Difícil de estimar con precisión
            - **Una sola muestra:** No permite muestreo repetido
            - **Correlación:** Elementos cercanos pueden ser similares
            """)
        
        # Comparación con MAS
        st.markdown("---")
        st.subheader("⚖️ Comparación con Muestreo Aleatorio Simple")
        
        if objetivo_sist == "Media":
            n_mas_equiv = int(np.ceil((z_sist ** 2 * sigma_sist ** 2) / (error_sist ** 2)))
            n_mas_equiv = int(np.ceil(n_mas_equiv / (1 + (n_mas_equiv - 1) / N_sist)))
        else:
            n_mas_equiv = int(np.ceil((z_sist ** 2 * p_sist * (1-p_sist)) / (error_sist ** 2)))
            n_mas_equiv = int(np.ceil(n_mas_equiv / (1 + (n_mas_equiv - 1) / N_sist)))
        
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        with col_comp1:
            st.metric("MAS (n)", f"{n_mas_equiv:,}")
            st.caption("Requiere números aleatorios")
        
        with col_comp2:
            st.metric("Sistemático (n)", f"{n_sist_ajustado:,}")
            st.caption("Solo 1 número aleatorio")
        
        with col_comp3:
            dif_pct = ((n_sist_ajustado - n_mas_equiv) / n_mas_equiv * 100) if n_mas_equiv > 0 else 0
            st.metric("Diferencia", f"{dif_pct:+.1f}%")
            if abs(dif_pct) < 5:
                st.caption("✅ Muy similar")
            else:
                st.caption("⚠️ Ajuste aplicado")
        
        st.info("""
        **Recomendación:** El muestreo sistemático es apropiado cuando:
        - No existe periodicidad conocida en la población
        - Se busca simplicidad operativa
        - Se desea distribución espacial uniforme
        
        Si existe periodicidad, considera **Muestreo Estratificado** en su lugar.
        """)
        
        # Exportar
        df_sist = pd.DataFrame([{
            'Método': 'Sistemático',
            'N (población)': N_sist,
            'n (muestra)': n_sist_ajustado,
            'k (intervalo)': k,
            'Inicio aleatorio': inicio_aleatorio,
            'Confianza': f"{confianza_sist*100:.0f}%",
            'Error': error_sist,
            'Periodicidad': 'Sí' if periodicidad else 'No'
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_sist),
            "muestreo_sistematico.xlsx"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<p>🔢 Calculadora Avanzada de Tamaño de Muestra</p>
<p><small>Incluye: Estimación de Medias y Proporciones | 4 Tipos de Muestreo</small></p>
<p><small>Versión 2.0 - Herramienta educativa y profesional</small></p>
</div>
""", unsafe_allow_html=True)"""
        **Objetivo:** Estimar la media poblacional μ con un intervalo de confianza especificado.
        
        **Fórmula básica:** n = (Z_{α/2} × σ / E)²
        
        Para muestras pequeñas (n < 30), se usa distribución t-Student.
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Parámetros")
            sigma = st.number_input(
                "Desviación estándar poblacional (σ)",
                min_value=0.1,
                value=15.0,
                step=0.5,
                help="Si no conoces σ, usa una estimación de estudios previos"
            )
            
            error = st.number_input(
                "Error máximo aceptable (E)",
                min_value=0.1,
                value=3.0,
                step=0.1,
                help="Precisión deseada en las unidades de la variable"
            )
            
            confianza = st.select_slider(
                "Nivel de confianza",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{x*100:.0f}%"
            )
            
            poblacion = st.number_input(
                "Tamaño de población (N)",
                min_value=0,
                value=0,
                help="Dejar en 0 si la población es infinita o muy grande (N > 100,000)"
            )
            
            usar_t = st.checkbox(
                "Usar distribución t-Student (muestras pequeñas)",
                value=True,
                help="Recomendado cuando n < 30 o σ es estimado"
            )
        
        with col2:
            st.subheader("Resultados")
            
            # Cálculo con Z
            alpha = 1 - confianza
            z_alpha = norm.ppf(1 - alpha/2)
            n_z = int(np.ceil((z_alpha * sigma / error) ** 2))
            
            # Cálculo iterativo con t (si se solicita)
            if usar_t:
                n_prev = n_z
                max_iter = 50
                for i in range(max_iter):
                    gl = max(n_prev - 1, 1)
                    t_alpha = t_dist.ppf(1 - alpha/2, gl)
                    n_new = int(np.ceil((t_alpha * sigma / error) ** 2))
                    if abs(n_new - n_prev) <= 1:
                        break
                    n_prev = n_new
                n_final = n_new
                valor_critico = t_alpha
                distribucion = f"t({gl} gl)"
            else:
                n_final = n_z
                valor_critico = z_alpha
                distribucion = "Z (Normal)"
            
            # Corrección por población finita
            if poblacion > 0 and poblacion < 100000:
                n_ajustado = int(np.ceil(n_final / (1 + (n_final - 1) / poblacion)))
                st.warning(f"⚠️ Población finita detectada (N = {poblacion:,})")
            else:
                n_ajustado = n_final
            
            # Mostrar resultados
            st.metric("Tamaño de muestra requerido", f"{n_ajustado:,}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Distribución usada", distribucion)
                st.metric("Valor crítico", f"{valor_critico:.4f}")
            with col_b:
                st.metric("Error relativo", f"{(error/sigma)*100:.1f}%")
                if poblacion > 0:
                    st.metric("% de la población", f"{(n_ajustado/poblacion)*100:.2f}%")
            
            # Interpretación
            st.success(f"""
            ✅ **Interpretación:**
            
            Con una muestra de **{n_ajustado:,} observaciones**, podrás estimar la media poblacional 
            con un error máximo de ±{error} unidades, con un nivel de confianza del {confianza*100:.0f}%.
            
            Intervalo de confianza esperado: [μ - {error}, μ + {error}]
            """)
            
            if usar_t and n_final < 30:
                st.info("📌 Se usó distribución t-Student porque n < 30 (muestra pequeña)")
        
        # Análisis de sensibilidad
        st.markdown("---")
        st.subheader("📊 Análisis de Sensibilidad")
        
        errores = np.linspace(error*0.5, error*2, 50)
        tamaños = []
        
        for e in errores:
            if usar_t:
                n_temp = n_z
                for _ in range(20):
                    gl_temp = max(n_temp - 1, 1)
                    t_temp = t_dist.ppf(1 - alpha/2, gl_temp)
                    n_temp = int(np.ceil((t_temp * sigma / e) ** 2))
            else:
                n_temp = int(np.ceil((z_alpha * sigma / e) ** 2))
            
            if poblacion > 0 and poblacion < 100000:
                n_temp = int(np.ceil(n_temp / (1 + (n_temp - 1) / poblacion)))
            
            tamaños.append(n_temp)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(errores, tamaños, 'b-', linewidth=2)
        ax.axvline(error, color='r', linestyle='--', label=f'Error actual: {error}')
        ax.axhline(n_ajustado, color='r', linestyle='--', alpha=0.5)
        ax.scatter([error], [n_ajustado], color='r', s=100, zorder=5)
        ax.set_xlabel('Error Máximo (E)', fontsize=12)
        ax.set_ylabel('Tamaño de Muestra (n)', fontsize=12)
        ax.set_title('Relación entre Error y Tamaño de Muestra', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close()
        
        # Exportar resultados
        df_resultados = pd.DataFrame([{
            'Tipo': 'Estimación de Media',
            'Sigma': sigma,
            'Error': error,
            'Confianza': f"{confianza*100:.0f}%",
            'Distribución': distribucion,
            'N (sin ajuste)': n_final,
            'N (final)': n_ajustado,
            'Población': poblacion if poblacion > 0 else 'Infinita'
        }])
        
        st.download_button(
            "📥 Descargar resultados (Excel)",
            exportar_excel(df_resultados),
            "tamano_muestra_media.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
else:  # Por Tipo de Muestreo
    
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
    # MUESTREO ALEATORIO SIMPLE
    # ==========================================
    if tipo_muestreo == "🎲 Muestreo Aleatorio Simple (MAS)":
        st.header("Muestreo Aleatorio Simple (MAS)")
        
        st.info(
