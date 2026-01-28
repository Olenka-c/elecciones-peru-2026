#Análisis de la agenda mediática electoral en Perú (Elecciones 2026)

Este proyecto analiza los titulares publicados en la sección “Elecciones” del medio digital *La República*, con el objetivo de identificar los temas predominantes en la cobertura periodística durante el periodo previo a las Elecciones Generales del Perú 2026.

#Pregunta de investigación

¿Qué temas predominan en las portadas digitales de la sección "Elecciones" de La República durante el periodo previo a las Elecciones Generales del Perú 2026?

#Metodología

#1. Extracción de datos
- Fuente: https://larepublica.pe/elecciones
- Técnica: Web scraping estático
- Herramientas: Python, requests, BeautifulSoup
- Output: titulares_elecciones_raw.csv

#2. Limpieza y procesamiento
- Eliminación de titulares duplicados
- Normalización de texto
- Tokenización y eliminación de stopwords
- Clasificación temática por palabras clave
- Outputs:
  - titulares_elecciones_limpio.csv
  - top_palabras_elecciones.csv

#3. Análisis NLP
- Análisis de frecuencia léxica
- Identificación de agenda temática
- Análisis de sentimiento (positivo, negativo, neutral)

#Principales hallazgos

La cobertura de la sección “Elecciones” se caracteriza por un fuerte énfasis en:
- Fiscalización legal de candidaturas
- Decisiones del JNE y JEE
- Verificación de información y desinformación
- Personalización de la política en figuras individuales

La agenda mediática prioriza el control institucional y la controversia legal por encima de propuestas programáticas.

#Visualización
Los resultados del proyecto se presentan mediante un website publicado con GitHub Pages en la carpeta `/docs`.
