# 🕵️‍♀️ NOVA RETAIL: Forensic Loss Prevention & Risk Intelligence

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-Ver_Proyecto_Web-ff3366?style=for-the-badge)](https://evidaurri89-lgtm.github.io/nova-retail-forensic/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)]()

> **Caso de Estudio Analítico:** Consolidación ejecutiva de hallazgos críticos sobre discrepancias de inventario, detección de *Shadow Inventory* (Ghost SKUs) y priorización de riesgo operativo mediante un pipeline de datos end-to-end.

![Nova Retail Dashboard Hero](assets/hero-screenshot.png)

## 📊 El Problema de Negocio
Durante una auditoría en la red logística del Corredor Norte, se detectaron discrepancias atípicas entre los registros de despacho (SAP S/4HANA) y las recepciones en tienda (AS400). El análisis inicial reveló la existencia de "Apple Ghosts" (productos premium de alto valor movilizados físicamente pero invisibles para el sistema legacy). 

El objetivo de este proyecto fue pasar de un análisis forense de datos crudos a una **herramienta interactiva de decisión ejecutiva** para el comité de prevención de pérdidas.

## 🎯 Hallazgos y Resultados Clave (The 5-5-1 Framework)
En lugar de abrumar a la operación con decenas de tiendas sospechosas, el modelo priorizó el riesgo basándose en la convergencia de anomalías (pérdida material + horario atípico + vulnerabilidad de sistema):

* **Vulnerabilidad Estructural (05:00 AM):** Se detectó un patrón sistemático de recepciones en una ventana atípica, totalmente separada del clúster de la red normal (08:00 a 19:00).
* **Intervención Quirúrgica (Tier 1):** Aislamiento de **5 tiendas críticas** (Max. discrepancia del 20.5% en `NOVA-OBR-156`) que requieren auditoría física inmediata y congelamiento de inventario. Destaca la tienda `NOVA-MAZ-171` con una anomalía crítica de *Ghost Store* confirmada.
* **Separación de Señal y Ruido:** El 94% de la operación fue clasificada como *Baseline normal*, lo que valida estadísticamente la gravedad y urgencia de las anomalías detectadas en el Tier 1.

## 🛠️ Arquitectura Técnica y Stack

Este proyecto no es solo un Jupyter Notebook estático; es un *pipeline* completo de datos conectado a una interfaz de usuario viva:

1.  **Ingeniería de Datos (Python/Pandas):** Limpieza, consolidación de bases de datos distribuidas y cruces forenses de alta dimensionalidad.
2.  **Diseño de Matriz de Riesgo:** Modelado de priorización para clasificación de tiendas en niveles (Tiers) de intervención.
3.  **Data Binding & CI/CD:** Exportación automatizada de KPIs y DataFrames a formato JSON para consumo web.
4.  **Visualización Ejecutiva (HTML/CSS/Vanilla JS):** Un dashboard "Dark Premium" interactivo diseñado para comités directivos.
5.  **Geospatial Intelligence:** Integración con **Leaflet.js** para el mapeo interactivo de rutas de riesgo.

## 📁 Estructura del Proyecto

```text
nova-retail-forensic/
│
├── 01_exploration/         # Análisis exploratorio inicial de datos crudos
├── 02_cleaning/            # Reconciliación de SKUs y limpieza estructural
├── 03_forensic_analysis/   # Análisis de discrepancias y Matriz de Riesgo Ejecutiva
│
├── data/                   # Archivos JSON vivos generados por Python para el dashboard web
├── css/ & js/              # Estilos UI premium y lógica de data-binding / Leaflet
├── index.html              # Frontend del Dashboard Ejecutivo
└── README.md               # Documentación del proyecto y conclusiones