AT-27-30
Catálogo de Algoritmos Estratégicos
Motor Analítico Electoral
Versión 1.0
Objetivo

Este documento identifica y documenta los algoritmos estratégicos que conforman el núcleo analítico de la plataforma AT-27-30.

Su propósito es separar la lógica de negocio del código de interfaz (HTML, JavaScript y Leaflet), permitiendo que todos los módulos consuman un único motor de análisis mediante PostgreSQL, PostGIS y API REST.

Este catálogo constituye la base para la migración hacia el Copilot Electoral Territorial HEYTI.

Arquitectura General
                FRONTEND

 Análisis Territorial
 Ganar Todo
 Campo
 Estructura Territorial
 Día D
 Portal

            │
            │ API
            ▼

──────────────────────────────────
     MOTOR ANALÍTICO ELECTORAL
──────────────────────────────────

Competitividad
Ganadores
Historial
Participación
Proyecciones
Estabilidad
Indicadores
Escenarios

            │

        PostgreSQL
        PostGIS
Catálogo de Algoritmos
AE-001
Índice de Competitividad Electoral
Objetivo

Determinar el nivel de competencia existente dentro de una sección electoral.

Entradas
PAN
PRI
PVEM
MORENA
VOTOS
Salidas
Partido ganador
Segundo lugar
Diferencia absoluta
Diferencia porcentual
Nivel de competitividad
Consumido por
Análisis Territorial
Ganar Todo
Heyti

Estado

✅ Identificado

AE-002
Historial Electoral
Objetivo

Construir la serie histórica electoral de una sección.

Entradas

Resultados históricos por puesto:

2018
2021
2024

(según corresponda)

Salidas

Series temporales para:

votos
partidos
participación
evolución
Consumido por
Análisis Territorial
Reportes
Heyti

Estado

✅ Identificado

AE-003
Determinación del Ganador Electoral
Función original
winnerOf()
Objetivo

Encontrar el partido con mayor votación.

Entradas
PAN
PRI
PVEM
MORENA
Salidas
Ganador

Votos

Total de votos

Estado

✅ Identificado

AE-004
Cálculo de Margen Electoral
Función original
winnerAndMargin()
Objetivo

Calcular la diferencia entre el primero y segundo lugar.

Salidas
Ganador

Margen absoluto

Margen porcentual

Estado

✅ Identificado

AE-005
Participación Electoral
Fórmula
Participación =

VOTOS

─────────

LN
Resultado
Porcentaje de participación

Estado

✅ Identificado

AE-006
Votos de Otros Partidos
Fórmula
OTROS =

VOTOS

-

(PAN+PRI+PVEM+MORENA)
Utilidad

Permite identificar:

votos nulos
independientes
partidos menores
coaliciones no desagregadas

Estado

✅ Identificado

AE-007
Estabilidad Política
Objetivo

Medir la estabilidad electoral de una sección entre elecciones.

Clasificación

Verde

Mismo ganador durante las tres elecciones.

Amarillo

Existe al menos un cambio.

Rojo

Tres ganadores distintos.

Consumido por
Análisis Territorial
Ganar Todo
Heyti

Estado

✅ Identificado

AE-008
Ganadores por Sección
Función original
AT27_GPA_computeWinners()
Objetivo

Determinar el partido ganador de todas las secciones del universo seleccionado.

Resultado
Sección

↓

Ganador

↓

Conteo por partido

Estado

✅ Identificado

Algoritmos de Interfaz (No migran al CORE)

Estos componentes pertenecen exclusivamente al FrontEnd.

Código	Función	Destino
UI-001	Fit Universe Bounds	Leaflet
UI-002	Flash Overlay	Leaflet
UI-003	Build Overlay	Leaflet
UI-004	Toolbars	HTML
UI-005	Paneles flotantes	HTML
UI-006	Historial Charts	Chart.js
UI-007	Etiquetas dinámicas	Leaflet
UI-008	Zoom automático	Leaflet

Estos componentes deberán consumir información del Motor Analítico Electoral, pero no contendrán lógica estratégica.

Módulos consumidores

El Motor Analítico Electoral será utilizado por:

Módulo	Consume algoritmos
Portal	✔
Análisis Territorial	✔
Ganar Todo	✔
Campo	✔
Estructura Territorial	✔
Día D	✔
Socioeconómico	✔
Heyti	✔
Beneficios de la separación
Un único lugar para toda la inteligencia electoral.
Eliminación de lógica duplicada entre módulos.
APIs reutilizables.
Mayor velocidad de mantenimiento.
Algoritmos independientes de la interfaz gráfica.
Compatibilidad con PostgreSQL/PostGIS.
Base para entrenamiento y razonamiento del Copilot HEYTI.
Estado del inventario
Código	Algoritmo	Estado
AE-001	Competitividad Electoral	✅
AE-002	Historial Electoral	✅
AE-003	Ganador Electoral	✅
AE-004	Margen Electoral	✅
AE-005	Participación Electoral	✅
AE-006	Otros Votos	✅
AE-007	Estabilidad Política	✅
AE-008	Ganadores por Sección	✅
Próximos algoritmos candidatos (v1.1)

Durante la auditoría del código se identificarán y documentarán nuevos algoritmos, entre ellos:

AE-009 Índice de Volatilidad Electoral.
AE-010 Swing Electoral.
AE-011 Bastiones y Territorios Prioritarios.
AE-012 Meta Electoral 2027.
AE-013 Proyección Electoral.
AE-014 Simulación de Escenarios.
AE-015 Riesgo Electoral.
AE-016 Prioridad Territorial.
AE-017 Índice Estratégico Integral.
AE-018 Recomendaciones Inteligentes para HEYTI.
Observación técnica

A partir de esta versión, cualquier algoritmo estratégico descubierto durante la auditoría del código deberá incorporarse primero a este catálogo antes de implementarse en PostgreSQL o exponerse mediante API. De esta forma, el catálogo se convierte en la referencia oficial del Motor Analítico Electoral de AT-27-30