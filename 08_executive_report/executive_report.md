# NOVA RETAIL — Reporte Ejecutivo de Riesgo Operativo
**Diagnóstico Forense de Pérdidas y Vulnerabilidad Operativa**  
**Clasificación:** Confidencial — Solo Distribución Ejecutiva  
**Fecha:** Q1 2024  
**Analista:** Denz One — Forensic Data Analyst  

---

## 1. Resumen Ejecutivo

El presente diagnóstico identifica una vulnerabilidad operativa activa y localizada en la red de tiendas de Nova Retail. El análisis forense de datos cruzados (despachos, recepciones, inventario y catálogo de sistemas) revela un patrón sistemático e incompatible con ruido operativo normal.

**Las conclusiones principales son:**

- Un subconjunto de **8 tiendas en la Ruta Norte** presenta discrepancias de recepción entre **13% y 20.5%**, muy por encima del rango operativo normal.
- Estas mismas tiendas concentran recepciones en la franja de las **05:00 AM**, ausente en el resto de la red.
- Se detectó movilización de mercancía bajo **SKUs invisibles para el sistema legacy (AS400)**, confirmando una vulnerabilidad estructural de trazabilidad.
- La convergencia de estos tres vectores en los mismos nodos geográficos descarta la hipótesis de error distribuido y apunta a un **patrón operativo localizado y priorizable**.

> El análisis no atribuye responsabilidad individual ni prueba fraude por sí mismo. Su función es identificar un patrón operativo defendible para escalamiento investigativo.

---

## 2. Contexto del Caso

| Parámetro | Valor |
|-----------|-------|
| Empresa | Nova Retail (simulación) |
| Red total de tiendas | 187 tiendas |
| Corredor analizado | Ruta Norte (Noreste de México) |
| Capital en riesgo estimado | $49.9M MXN |
| Período de análisis | Q1 2024 |
| Sistemas involucrados | SAP S/4HANA · Legacy AS400 |

---

## 3. Metodología

El diagnóstico se estructuró en **4 fases secuenciales**:

### Fase 1 — Reconciliación de Catálogo (SKU Matching)
Cruce entre el catálogo SAP y el catálogo AS400 para identificar productos con trazabilidad incompleta. Se detectaron inconsistencias estructurales: categorías vacías, precios nulos y productos activos en SAP sin equivalente funcional en AS400.

**Decisión metodológica:** Reconciliación selectiva por valor económico, no limpieza masiva de los 14,000 SKUs del catálogo.

### Fase 2 — Análisis de Despacho vs Recepción
Cruce entre los registros de despacho desde cedis y las recepciones registradas en tienda. La métrica clave no fue la frecuencia de incidencias, sino la **severidad porcentual de discrepancia** por producto prioritario en unidad.

**Hallazgo:** Subconjunto de tiendas con diferencias del 13% al 20.5%, concentradas en la Ruta Norte con recepciones en franja de 05:00 AM.

### Fase 3 — Shadow Inventory & Ghost SKUs
Identificación de SKUs visibles en SAP pero invisibles para AS400, con movilización física activa confirmada. Se denominaron **"Apple Ghosts"** por su concentración en productos premium de la categoría Apple.

**Hallazgo:** Superposición entre el flujo de Ghost SKUs y las tiendas de mayor severidad de discrepancia.

### Fase 4 — Matriz de Riesgo Unificada
Consolidación de todas las señales en un score de riesgo compuesto por tienda, generando una estructura de tiers operativamente accionable.

---

## 4. Hallazgos Críticos

### Vector 01 — Severidad de Discrepancia
Las tiendas de la Ruta Norte presentan discrepancias de recepción entre **13% y 20.5%** en productos prioritarios registrados como UNIDAD. Este rango es incompatible con el margen operativo normal de la red (< 5%).

### Vector 02 — Patrón Temporal Anómalo (05:00 AM)
La franja horaria de recepciones en las tiendas Tier 1 es **05:00 AM**, completamente ausente en tiendas de comportamiento normal. La combinación de severidad + ruta + horario constituye una señal operativa localizada.

### Vector 03 — Shadow Inventory (Ghost SKUs)
Productos de alto valor (categoría Apple) con presencia activa en SAP pero **precio NULL y categoría EMPTY** en AS400. Esto impide su seguimiento completo en el entorno legacy, creando una ventana de opacidad operativa explotable.

---

## 5. Matriz de Riesgo por Tienda

### Tier 1 — Intervención Inmediata (8 tiendas)

| ID | Tienda | Discrepancia | Recepción | Ghost SKUs |
|----|--------|-------------|-----------|------------|
| MX-112 | Monterrey Cumbres | 20.5% | 05:00 AM | Detectados |
| MX-034 | Saltillo Norte | 19.2% | 05:00 AM | Detectados |
| MX-076 | Torreón Galerías | 18.5% | 05:00 AM | Detectados |
| MX-025 | Nuevo Laredo Centro | 17.8% | 05:00 AM | Detectados |
| MX-102 | Monterrey Sur | 16.4% | 05:00 AM | Detectados |
| MX-088 | Apodaca Aeropuerto | 15.0% | 05:00 AM | Detectados |
| MX-055 | Reynosa Frontera | 14.2% | 05:00 AM | Detectados |
| MX-091 | Santa Catarina | 13.5% | 05:00 AM | Detectados |

### Tier 2 — Prevención Reforzada (3 tiendas)

| ID | Tienda | Discrepancia | Ghost SKUs |
|----|--------|-------------|------------|
| MX-089 | San Nicolás Centro | 13.0% | Riesgo Alto |
| MX-044 | Saltillo Sur | 10.0% | Riesgo Medio |
| MX-062 | Monclova Industrial | 8.5% | Watchlist |

### Tier 3 — Monitoreo (Baseline Normal)

| ID | Tienda | Discrepancia | Estado |
|----|--------|-------------|--------|
| MX-041 | Guadalupe Sur | 2.1% | Normal |
| MX-105 | San Pedro Valle | 1.8% | Normal |

---

## 6. Recomendaciones Ejecutivas

### Acción 01 — Intervención Quirúrgica Inmediata
Ejecutar auditoría física controlada en las **8 tiendas Tier 1** de la Ruta Norte. Congelar el inventario de electrónicos de alto valor durante el proceso. Establecer cadena de custodia para la evidencia nominal.

**Prioridad:** CRÍTICA  
**Plazo sugerido:** 72 horas

### Acción 02 — Trazabilidad de Usuarios
Integrar metadata de autorización de los sistemas para identificar qué usuarios están validando recepciones en la franja de las **05:00 AM**. Cruzar con registros de acceso físico a los almacenes.

**Prioridad:** ALTA  
**Plazo sugerido:** 1 semana

### Acción 03 — Reconciliación Selectiva de Catálogo
Priorizar la limpieza y matching entre SAP y AS400 exclusivamente para **SKUs de alto valor** (categoría Apple y electrónicos premium). No intentar reconciliación masiva de los 14,000 productos en esta fase.

**Prioridad:** ALTA  
**Plazo sugerido:** 2 semanas

---

## 7. Límites del Análisis

- Este reporte **no atribuye responsabilidad individual** ni constituye prueba de fraude.
- Los hallazgos son **patrones estadísticos y operativos**, no evidencia legal.
- La siguiente fase requiere integrar **trazabilidad de usuarios, metadata de autorización y evidencia nominal** bajo control de cadena de custodia.
- La reconciliación total del catálogo (14,000 SKUs) **no es operativamente eficiente** en esta fase. El enfoque correcto es selectivo por valor económico.

---

*Reporte generado como parte del proyecto de portafolio de análisis forense de datos.*  
*Nova Retail es una simulación. Todos los datos son sintéticos.*
