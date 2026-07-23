# Sprint 9.1 – Modelo del ADN Territorial

## 1. Identificación del Sprint

**Proyecto:** HEYTI – Sistema de Inteligencia Territorial
**Componente:** Motor de Inteligencia Territorial (MIT)
**Sprint:** 9.1 – Modelo del ADN Territorial
**Versión:** 1.0
**Estado:** En construcción

---

## 2. Objetivo

Diseñar el modelo conceptual, funcional y matemático del ADN Territorial de HEYTI, mediante el cual cada sección electoral será representada por un conjunto estructurado de indicadores estratégicos.

El ADN Territorial permitirá integrar en un solo perfil la información electoral, territorial, socioeconómica, operativa y organizacional disponible en la plataforma.

Este modelo será la base para:

* calcular el Score Territorial;
* identificar fortalezas, debilidades, riesgos y oportunidades;
* comparar secciones y territorios;
* establecer prioridades de intervención;
* generar recomendaciones estratégicas;
* construir escenarios y simulaciones;
* proporcionar contexto al Copilot HEYTI.

---

## 3. Definición del ADN Territorial

El ADN Territorial es la representación multidimensional del estado político, electoral, social, territorial y operativo de una sección electoral.

No corresponde a un único indicador ni a una calificación aislada.

Cada sección tendrá un perfil compuesto por dimensiones, variables, indicadores, evidencias, niveles de confianza y temporalidad.

El ADN Territorial deberá responder, como mínimo, las siguientes preguntas:

1. ¿Cuál es la fortaleza electoral de la sección?
2. ¿Qué tan competitiva o disputada se encuentra?
3. ¿Existe crecimiento, pérdida o estabilidad electoral?
4. ¿Qué tan sólida es la estructura territorial?
5. ¿Qué nivel de presencia existe en campo?
6. ¿Cuál es la cobertura operativa para el Día D?
7. ¿Qué riesgos estratégicos presenta?
8. ¿Qué oportunidades de crecimiento existen?
9. ¿Qué tan urgente es intervenir?
10. ¿Qué acción concreta debería recomendar HEYTI?

---

## 4. Unidad principal de análisis

La unidad mínima de inteligencia territorial será la:

**Sección electoral**

La clave de integración será:

```text
section_id
section_code
```

A partir de la sección podrán construirse agregaciones para:

* municipio;
* distrito local;
* distrito federal;
* región operativa;
* zona estratégica;
* entidad federativa.

La sección será la unidad principal porque permite relacionar:

* resultados electorales;
* lista nominal;
* participación;
* geometría;
* población;
* indicadores socioeconómicos;
* personas y liderazgos;
* estructura territorial;
* casillas;
* cobertura operativa;
* incidencias del Día D;
* recomendaciones;
* escenarios.

---

## 5. Dimensiones iniciales del ADN Territorial

### 5.1 Fortaleza Electoral

Mide la posición electoral histórica y actual de la fuerza política analizada dentro de la sección.

Indicadores candidatos:

* porcentaje de voto propio;
* posición electoral;
* margen frente al primer lugar;
* margen frente al segundo lugar;
* elecciones ganadas;
* promedio histórico de votación;
* estabilidad del voto;
* presencia electoral acumulada.

---

### 5.2 Competitividad

Mide qué tan cerrada, concentrada o disputada se encuentra la competencia electoral.

Indicadores candidatos:

* margen entre primero y segundo lugar;
* margen porcentual;
* índice de concentración electoral;
* número efectivo de competidores;
* volatilidad electoral;
* alternancia;
* clasificación de sección segura, competida o adversa.

---

### 5.3 Tendencia y Crecimiento

Mide la dirección del comportamiento electoral de una sección.

Indicadores candidatos:

* variación absoluta de votos;
* variación porcentual;
* tasa de crecimiento electoral;
* tendencia histórica;
* aceleración o desaceleración;
* crecimiento de lista nominal;
* crecimiento de participación;
* proyección electoral.

---

### 5.4 Participación Electoral

Mide el nivel de movilización electoral y el potencial de votos disponibles.

Indicadores candidatos:

* participación histórica;
* abstención;
* variación de participación;
* participación estimada para 2027;
* votos emitidos;
* lista nominal;
* potencial movilizable;
* brecha entre participación real y esperada.

---

### 5.5 Estructura Territorial

Mide la capacidad organizativa existente dentro de la sección.

Indicadores candidatos:

* número de representantes;
* cobertura de casillas;
* representantes faltantes;
* líderes registrados;
* promotores activos;
* simpatizantes identificados;
* observadores;
* densidad de estructura;
* nivel de cobertura organizacional.

---

### 5.6 Presencia y Actividad de Campo

Mide la existencia y actividad real de operación territorial.

Indicadores candidatos:

* registros de campo;
* visitas realizadas;
* fecha de última actividad;
* promotores activos;
* productividad por promotor;
* distribución geográfica de registros;
* cobertura de colonias o localidades;
* frecuencia de actividad;
* calidad y actualización de la información.

---

### 5.7 Capacidad Operativa Día D

Mide la preparación y capacidad de respuesta para la jornada electoral.

Indicadores candidatos:

* casillas con representante;
* casillas sin cobertura;
* representantes confirmados;
* incidencias;
* estatus de casillas;
* actas capturadas;
* avance de operación;
* tiempo de respuesta;
* nivel de riesgo operativo.

---

### 5.8 Contexto Socioeconómico

Mide las condiciones demográficas y sociales que pueden influir en el comportamiento territorial.

Indicadores candidatos:

* población total;
* población mayor de 18 años;
* crecimiento poblacional;
* escolaridad;
* empleo;
* condiciones de vivienda;
* acceso a servicios;
* urbanización;
* marginación;
* composición por edad;
* correspondencia entre población y lista nominal.

---

### 5.9 Riesgo Territorial

Mide la probabilidad de pérdida, deterioro, conflicto o insuficiencia operativa.

Indicadores candidatos:

* bastión en caída;
* pérdida sostenida de votos;
* reducción de participación propia;
* estructura insuficiente;
* casillas sin cobertura;
* baja actividad de campo;
* alta competitividad;
* presencia adversaria;
* información desactualizada;
* incidencias operativas.

---

### 5.10 Oportunidad Territorial

Mide el potencial de crecimiento o recuperación de una sección.

Indicadores candidatos:

* margen electoral recuperable;
* abstencionismo movilizable;
* crecimiento de lista nominal;
* baja diferencia frente al ganador;
* tendencia positiva;
* estructura con capacidad disponible;
* alta participación potencial;
* presencia de liderazgos;
* concentración geográfica favorable;
* relación entre esfuerzo e impacto esperado.

---

### 5.11 Prioridad Estratégica

Determina la urgencia y conveniencia de intervenir una sección.

La prioridad no deberá confundirse con el riesgo.

Una sección puede tener:

* alto riesgo y baja oportunidad;
* bajo riesgo y alta oportunidad;
* alto riesgo y alta oportunidad;
* baja urgencia operativa;
* alta prioridad de defensa;
* alta prioridad de recuperación;
* alta prioridad de crecimiento.

La prioridad estratégica deberá integrar:

```text
Prioridad =
    Impacto esperado
  × Urgencia
  × Viabilidad
  × Oportunidad
  × Confianza de los datos
```

---

## 6. Escala común de evaluación

Cada dimensión será normalizada inicialmente en una escala de:

```text
0 a 100
```

Interpretación preliminar:

|  Rango | Nivel    |
| -----: | -------- |
|   0–19 | Crítico  |
|  20–39 | Bajo     |
|  40–59 | Medio    |
|  60–79 | Alto     |
| 80–100 | Muy alto |

La interpretación dependerá de la dimensión.

Por ejemplo:

* un valor alto en Fortaleza será favorable;
* un valor alto en Oportunidad será favorable;
* un valor alto en Riesgo será desfavorable;
* un valor alto en Prioridad indicará necesidad de atención.

Por lo tanto, cada indicador deberá declarar su dirección:

```text
POSITIVE
NEGATIVE
NEUTRAL
```

---

## 7. Estructura preliminar del ADN Territorial

Cada sección podrá representarse mediante una estructura lógica semejante a la siguiente:

```json
{
  "section_id": 1456,
  "section_code": "1456",
  "calculation_date": "2026-07-10",
  "political_force": "PAN",
  "dimensions": {
    "electoral_strength": 68.4,
    "competitiveness": 82.1,
    "growth": 74.8,
    "participation": 53.2,
    "territorial_structure": 41.5,
    "field_presence": 36.0,
    "election_day_capacity": 28.7,
    "socioeconomic_context": 62.0,
    "territorial_risk": 71.3,
    "territorial_opportunity": 84.6,
    "strategic_priority": 88.2
  },
  "classification": {
    "territorial_type": "OPPORTUNITY",
    "priority_level": "VERY_HIGH",
    "recommended_strategy": "RECOVERY_AND_STRUCTURE"
  },
  "confidence": {
    "overall": 0.82,
    "electoral": 1.0,
    "structure": 0.75,
    "field": 0.60,
    "socioeconomic": 0.95
  }
}
```

---

## 8. Principios del modelo

El ADN Territorial deberá ser:

### Explicable

Cada resultado deberá mostrar las variables que lo originaron.

HEYTI no deberá emitir una calificación sin explicar:

* qué datos utilizó;
* qué cálculo aplicó;
* qué evidencias encontró;
* qué datos faltaron;
* por qué emitió una recomendación.

### Trazable

Cada indicador deberá vincularse con:

* fuente;
* tabla;
* fecha de actualización;
* versión del algoritmo;
* parámetros utilizados.

### Configurable

Los pesos y umbrales no deberán quedar fijados permanentemente en el código.

Deberán almacenarse como configuración versionada.

### Temporal

El ADN Territorial podrá cambiar con cada:

* elección;
* actualización de lista nominal;
* captura de campo;
* integración de estructura;
* cambio en cobertura de casillas;
* incidencia del Día D;
* nuevo escenario.

### Comparable

Todas las secciones deberán usar escalas homogéneas que permitan comparación territorial.

### Multinivel

El mismo modelo deberá generar resultados para sección, municipio, distrito y estado.

### Consciente de la calidad de los datos

Una recomendación no deberá presentarse con la misma certeza cuando existen datos completos que cuando la información es parcial o antigua.

---

## 9. Nivel de confianza

Cada resultado deberá contar con un nivel de confianza calculado a partir de:

* cobertura de fuentes;
* antigüedad de los datos;
* consistencia;
* integridad;
* cantidad de observaciones;
* calidad de georreferenciación;
* presencia de valores estimados;
* disponibilidad histórica.

Escala inicial:

| Confianza | Interpretación |
| --------: | -------------- |
| 0.00–0.39 | Baja           |
| 0.40–0.69 | Media          |
| 0.70–0.89 | Alta           |
| 0.90–1.00 | Muy alta       |

HEYTI deberá diferenciar entre:

```text
dato observado
dato calculado
dato estimado
dato proyectado
dato simulado
```

---

## 10. Clasificaciones estratégicas iniciales

El MIT podrá clasificar cada sección en uno o varios arquetipos:

* Bastión consolidado
* Bastión en riesgo
* Sección competitiva
* Sección recuperable
* Oportunidad de crecimiento
* Alta abstención movilizable
* Estructura insuficiente
* Estructura sólida
* Operación crítica
* Territorio adverso
* Territorio volátil
* Prioridad de defensa
* Prioridad de recuperación
* Prioridad de expansión
* Información insuficiente

Estas clasificaciones serán generadas mediante reglas explicables y posteriormente podrán complementarse con modelos estadísticos.

---

## 11. Primer resultado esperado del MIT

Al concluir esta etapa, HEYTI deberá ser capaz de producir una respuesta semejante a la siguiente:

> La sección 1456 presenta una oportunidad estratégica alta. La fuerza política analizada ha mantenido una tendencia electoral positiva, pero la estructura territorial y la cobertura de casillas permanecen por debajo del nivel requerido. La diferencia frente al primer lugar es recuperable y existe un volumen relevante de abstención potencialmente movilizable. Se recomienda fortalecer la estructura, asignar representantes de casilla y realizar trabajo de campo focalizado antes de ampliar la inversión territorial.

La respuesta deberá acompañarse de:

* indicadores utilizados;
* nivel de confianza;
* principales evidencias;
* riesgos detectados;
* acciones sugeridas;
* impacto esperado.

---

## 12. Entregables del Sprint 9.1

1. Catálogo oficial de dimensiones del ADN Territorial.
2. Diccionario de indicadores.
3. Fórmulas preliminares.
4. Dirección e interpretación de cada indicador.
5. Pesos iniciales.
6. Reglas de clasificación.
7. Modelo de confianza.
8. Diseño de tablas PostgreSQL.
9. Consulta piloto para una sección.
10. Validación manual con secciones reales.
11. ADR correspondiente a la arquitectura del ADN Territorial.

---

## 13. Criterios de aceptación

El Sprint 9.1 se considerará terminado cuando:

* todas las dimensiones estén definidas;
* cada dimensión tenga indicadores medibles;
* cada indicador tenga una fuente identificada;
* las fórmulas estén documentadas;
* los pesos sean configurables;
* exista un esquema de normalización;
* se contemple la calidad y antigüedad de los datos;
* una sección pueda generar un ADN Territorial completo;
* el resultado pueda explicarse en lenguaje natural;
* el modelo pueda implementarse posteriormente en PostgreSQL y Python.

---

## 14. Resultado esperado

Al finalizar el Sprint 9.1, HEYTI contará con el lenguaje formal necesario para interpretar un territorio.

A partir de este modelo podrán construirse el Score Territorial, el Motor de Diagnóstico, el Motor de Recomendaciones, el Motor de Escenarios y el Copilot HEYTI.

Este Sprint constituye el inicio formal de la inteligencia territorial de la plataforma.
