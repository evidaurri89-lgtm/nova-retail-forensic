# NOVA RETAIL — Forensic Loss Prevention Diagnostic

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13-blue)

## Resumen del Proyecto

Diagnostico forense end-to-end que simula un caso real de prevencion de perdidas para una cadena de retail de 187 tiendas con 49.9M MXN en riesgo operativo.

El analisis identifico un patron sistematico de discrepancias de inventario (13-20.5%) concentrado en la Ruta Norte, con recepciones atipicas a las 05:00 AM y productos de alto valor invisibles para el sistema legacy (Ghost SKUs).

## Presentacion Interactiva

Ver Dashboard en Vivo: https://evidaurri89-lgtm.github.io/nova-retail-forensic/07_presentation/

Incluye:
- Mapa geoespacial interactivo (Leaflet.js) con los nodos de riesgo
- Matriz de riesgo filtrable por Tier 1, 2 y 3
- Evidencia tecnica del patron 05:00 AM
- Comparativo SAP vs AS400 (Ghost SKUs)
- Executive Action Plan

## Estructura del Proyecto

- 00_data_generation: Scripts de generacion de datos sinteticos
- 01_exploration: Auditoria inicial de datos
- 02_cleaning: Reconciliacion de catalogo SKU (SAP vs AS400)
- 03_forensic_analysis: Analisis forense principal
  - 03_dispatch_vs_reception.ipynb
  - 04_shadow_inventory_and_ghost_skus.ipynb
  - 05_unified_risk_matrix.ipynb
- 07_presentation: Dashboard HTML interactivo
- 08_executive_report: Reporte ejecutivo formal

## Metodologia (4 Fases)

Fase 1: Reconciliacion de Catalogo
Cruce entre SAP S/4HANA y sistema legacy AS400. Identificacion de SKUs con trazabilidad incompleta. Decision: reconciliacion selectiva por valor economico.

Fase 2: Analisis Forense de Despacho vs Recepcion
Cruce de registros de despacho desde CEDIS vs recepciones en tienda. Hallazgo: 8 tiendas con discrepancias del 13-20.5% y recepciones a las 05:00 AM.

Fase 3: Shadow Inventory y Ghost SKUs
Identificacion de SKUs activos en SAP pero invisibles para AS400. Productos Apple con movilizacion fisica confirmada sin trazabilidad en legacy.

Fase 4: Matriz de Riesgo Unificada
Score compuesto por tienda integrando todos los vectores de riesgo. Estructura de Tiers operativamente accionable para escalamiento ejecutivo.

## Hallazgos Criticos

- Discrepancia: 8 tiendas con 13-20.5% vs menos del 5% normal
- Temporal: Recepciones a las 05:00 AM exclusivamente en Ruta Norte
- Catalogo: Ghost SKUs (Apple) visibles en SAP, precio NULL en AS400
- Geografico: Concentracion 100% en corredor logistico Norte

## Stack Tecnologico

- Analisis de datos: Python, Pandas, NumPy
- Machine Learning: Scikit-learn
- Visualizacion: Plotly, Matplotlib, Seaborn
- Geoespacial: Leaflet.js
- Frontend: HTML5, CSS3, JavaScript
- Control de versiones: Git / GitHub Pages

## Instalacion

git clone https://github.com/evidaurri89-lgtm/nova-retail-forensic.git
cd nova-retail-forensic
pip install -r requirements.txt
jupyter lab

## Disclaimer

Nova Retail es una simulacion con fines de portafolio. Todos los datos son sinteticos y generados algoritmicamente. Este analisis no atribuye responsabilidad individual ni constituye evidencia legal.

## Autor

Denz One - Forensic Data Analyst
GitHub: https://github.com/evidaurri89-lgtm
