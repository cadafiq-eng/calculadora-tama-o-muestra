# 🔢 Calculadora Avanzada de Tamaño de Muestra

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Herramienta interactiva desarrollada en Python con Streamlit para calcular tamaños de muestra en diversos escenarios estadísticos y diseños de muestreo.

## 🌟 Características

### 📊 Módulo 1: Por Tipo de Estimación
- ✅ **Estimación de una media poblacional**
  - Distribución Z o t-Student
  - Corrección por población finita
  - Análisis de sensibilidad
  
- ✅ **Estimación de una proporción**
  - Enfoque conservador (p=0.5)
  - Visualización de efectos

- ✅ **Diferencia de medias (2 grupos)**
  - Cálculo de d de Cohen
  - Control de potencia estadística
  - Curvas de potencia

- ✅ **Diferencia de proporciones**
  - Comparación entre grupos
  - Potencia configurable

### 🎯 Módulo 2: Por Tipo de Muestreo
- ✅ **Muestreo Aleatorio Simple (MAS)**
  - Para medias y proporciones
  - Corrección FPC automática
  
- ✅ **Muestreo Estratificado**
  - Asignación proporcional
  - Asignación óptima (Neyman)
  - Asignación igual
  - Hasta 6 estratos
  
- ✅ **Muestreo por Conglomerados**
  - Una o dos etapas
  - Cálculo de DEFF e ICC
  - Visualización de estructura
  
- ✅ **Muestreo Sistemático**
  - Cálculo de intervalo k
  - Detección de periodicidad
  - Lista de selección completa

### ❓ Módulo 3: Ayuda y Glosario
- 📖 Glosario completo de 15+ términos estadísticos
- 📐 Fórmulas principales explicadas
- 💡 Guía de uso con 4 casos prácticos
- ⚠️ Errores comunes a evitar

## 🚀 Funcionalidades Avanzadas

- 📊 **Visualizaciones interactivas**: Gráficos de sensibilidad, curvas de potencia
- 📥 **Exportación a Excel**: Todos los resultados descargables
- 🎯 **Validaciones automáticas**: FPC, t-Student para n<30
- ⚡ **Cálculos estadísticos**: DEFF, ICC, d de Cohen, potencia
- 🔍 **Alertas inteligentes**: Periodicidad, homogeneidad

## 📋 Requisitos

- Python 3.8 o superior
- Navegador web moderno

## 🛠️ Instalación Local
```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/calculadora-tamaño-muestra.git
cd calculadora-tamaño-muestra

# 2. Crea un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Ejecuta la aplicación
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 🌐 Uso Online (Sin instalación)

**[¡Pruébala aquí!](https://TU_APP.streamlit.app)** *(Disponible después del despliegue)*

## 📖 Ejemplos de Uso

### 📊 Ejemplo 1: Encuesta de satisfacción empresarial
```
Objetivo: Estimar % de empleados satisfechos
Población: 5,000 empleados
Método: Estimación de Proporción

Parámetros:
- p = 0.50 (conservador)
- E = 0.05 (±5%)
- Confianza = 95%

✅ Resultado: n = 357 empleados
```

### 🔬 Ejemplo 2: Ensayo clínico controlado
```
Objetivo: Comparar dos tratamientos
Variable: Presión arterial (mmHg)
Método: Diferencia de Medias

Parámetros:
- Δ = 10 mmHg (diferencia a detectar)
- σ = 15 mmHg
- α = 0.05, Potencia = 80%

✅ Resultado: 37 pacientes/grupo (74 total)
📊 d de Cohen = 0.67 (efecto mediano)
```

### 🏫 Ejemplo 3: Evaluación educativa multi-nivel
```
Objetivo: Rendimiento académico regional
Unidades: 150 escuelas, ~200 estudiantes/escuela
Método: Muestreo por Conglomerados (2 etapas)

Parámetros:
- Submuestreo: 50%
- DEFF esperado: 1.5

✅ Resultado: 15 escuelas, 100 estudiantes/escuela
💰 Ahorro: Solo visitas 15 ubicaciones vs 1,500 dispersas
```

### 📦 Ejemplo 4: Control de calidad industrial
```
Objetivo: Estimar % de productos defectuosos
Lote: 10,000 unidades producidas
Método: Muestreo Sistemático

Parámetros:
- p = 0.03 (3% defectuosos esperado)
- E = 0.01 (±1%)
- Confianza = 95%

✅ Resultado: n = 269, k = 37
📋 Seleccionar 1 de cada 37 productos
```

## 🎓 Casos de Uso por Disciplina

| Área | Aplicación | Módulo Recomendado |
|------|------------|-------------------|
| 🏥 **Salud** | Ensayos clínicos, epidemiología | Diferencia de Medias/Proporciones |
| 📊 **Mercadeo** | Encuestas de satisfacción, NPS | Estimación de Proporción |
| 🎓 **Educación** | Evaluaciones multi-nivel | Conglomerados |
| 🏭 **Calidad** | Control estadístico de procesos | Sistemático |
| 🌾 **Agronomía** | Diseños experimentales | Estratificado |
| 📈 **Finanzas** | Auditoría, muestreo de transacciones | Aleatorio Simple |

## 📊 Comparación de Métodos

| Método | Eficiencia | Costo | Complejidad | Uso recomendado |
|--------|-----------|-------|-------------|-----------------|
| **MAS** | ⭐⭐⭐⭐⭐ | 💰💰💰💰 | 🟢 Simple | Población homogénea |
| **Estratificado** | ⭐⭐⭐⭐⭐ | 💰💰💰 | 🟡 Moderado | Subgrupos conocidos |
| **Conglomerados** | ⭐⭐⭐ | 💰💰 | 🟡 Moderado | Población dispersa |
| **Sistemático** | ⭐⭐⭐⭐ | 💰 | 🟢 Simple | Lista ordenada |

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Haz fork del proyecto
2. Crea una rama (`git checkout -b feature/MejorFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/MejorFeature`)
5. Abre un Pull Request

### Ideas para contribuir
- 🌍 Traducción a otros idiomas
- 📊 Nuevos tipos de gráficos
- 🧮 Métodos de muestreo adicionales
- 📝 Más casos de uso documentados
- 🐛 Reportar bugs

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**[Tu Nombre]**
- GitHub: [@tu_usuario](https://github.com/tu_usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- Email: tu.email@ejemplo.com

## 🙏 Agradecimientos

- **Teoría de muestreo**: Cochran, Lohr, Scheaffer
- **Framework**: [Streamlit](https://streamlit.io)
- **Comunidad**: Stack Overflow, GitHub

## 📚 Referencias Bibliográficas

1. Cochran, W.G. (1977). *Sampling Techniques* (3rd ed.). Wiley.
2. Lohr, S.L. (2019). *Sampling: Design and Analysis* (2nd ed.). CRC Press.
3. Scheaffer, R.L., Mendenhall III, W., Ott, R.L., & Gerow, K.G. (2011). *Elementary Survey Sampling* (7th ed.). Cengage Learning.
4. Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Routledge.
5. Kish, L. (1965). *Survey Sampling*. Wiley.

## 🔄 Changelog

### v2.0.0 (Actual) - 2024
- ✅ Módulo completo de tipos de muestreo (4 métodos)
- ✅ Glosario interactivo con 15+ términos
- ✅ Guía de uso con casos prácticos
- ✅ Visualizaciones mejoradas
- ✅ Exportación a Excel
- ✅ Validaciones automáticas

### v1.0.0 - 2024
- ✅ Módulo básico de estimación
- ✅ 4 tipos de cálculos básicos
- ✅ Interfaz inicial

## 🐛 Reporte de Bugs

¿Encontraste un bug? [Ábrelo como issue](https://github.com/TU_USUARIO/calculadora-tamaño-muestra/issues)

## 💬 Contacto y Soporte

- 📧 Email: tu.email@ejemplo.com
- 💼 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)
- 🐦 Twitter: [@tu_usuario](https://twitter.com/tu_usuario)

---

⭐ **Si te resultó útil, considera darle una estrella al repositorio!**

Desarrollado con ❤️ usando Python y Streamlit
```

4. Commit: `Update README with complete documentation`
5. Clic en **"Commit changes"**

### **Paso 5: Desplegar en Streamlit Cloud (GRATIS)**

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Haz clic en **"Sign in"** y usa tu cuenta de GitHub
3. Autoriza Streamlit Cloud a acceder a tu GitHub
4. Haz clic en **"New app"**
5. Configura:
   - **Repository**: Selecciona `calculadora-tamaño-muestra`
   - **Branch**: `main`
   - **Main file path**: `app.py`
6. Haz clic en **"Deploy!"**

⏱️ **Espera 2-5 minutos** mientras se despliega.

Tu app estará disponible en una URL como:
```
https://tu-usuario-calculadora-tamaño-muestra.streamlit.app# calculadora-tama-o-muestra
Calculadora avanzada de tamaño de muestra con Streamlit
