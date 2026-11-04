# Proyección 2027 — alcance y revisión

Fecha: 22 de octubre de 2026. Actualización acumulativa del módulo Socioeconómico.

V1 calculaba CAGR entre bases 2018/2024 y proyectaba tres años, con una tasa de respaldo para faltantes. Permitía LN y población de 18 años y más. El JSON socioeconómico verificado aporta población adulta de 2020, no una serie adulta 2018/2024. No se usan los valores aleatorios del fallback de demostración de V1 ni los campos de proyección precalculados del JSON electoral.

## Adaptación implementada

1. LN histórica por sección: g=(LN2024/LN2018)^(1/6)-1; escenario2027=LN2024*(1+g)^3. Se muestran 2018/2021/2024; 2021 no interviene en la fórmula. Se exige base positiva en ambos extremos; no se sustituye un extremo ausente con una tasa genérica.
2. LN con tasa propia: LN2024*(1+g)^3. La tasa es obligatoria y explícita; cero conserva la base.
3. Población18+ con tasa propia: P18_2020*(1+g)^7. Se usa POB_18MAS de la referencia separada del CSV INEGI/INE geoelectoral2020 ya cotejada. No se fabrican bases2018/2024, no se importa una tasa de LN ni se afirma que esta fórmula sea una proyección por cohortes.

Tasas propias entre más de -100% y hasta100% anual. Se admiten coma decimal, cero y decrecimiento. Desbordamientos, faltantes, bases históricas cero e inconsistencias electorales en extremos quedan N/D; los valores originales siguen visibles. Una tasa propia puede usar una base cero válida. Las fechas se respetan:3años desde2024,7desde2020.

Los mapas históricos deben tener mismo universo/contienda/métrica/procedencia; una geometría diferente para la misma clave impide extrapolar esa fila. Este control entre respuestas no certifica el límite histórico real porque CORE agrupa con la cartografía actual. Toda extrapolación por clave se presenta condicional a equivalencia territorial pendiente. LN se obtiene de Ayuntamiento(A), sin mezclar contiendas. El padrón y la población18+ son universos distintos, no se combinan.

## Presentación y cobertura

Universo estatal, municipal, distrito federal o local según catálogo. Mapa base compartido con secciones, selección y acercamiento; quintiles del conteo estimado, empates juntos y gris para N/D. Tabla por sección con bases, tasa anual, horizonte, resultado, cambio, estado/método y correspondencia territorial. Totales sobre la misma cobertura calculable, visibles como parciales cuando corresponde, sumados antes del redondeo. No se agregan geometrías bloqueadas ni se reconstruyen polígonos históricos. Cambiar controles conserva el resultado anterior con aviso hasta recalcular; solicitudes cancelables al salir o repetir.

Se activa la última entrada de Socioeconómico y se retira su texto residual de pendientes. Ninguna fuente original ni configuración del CORE fue modificada. No incorpora orientaciones partidistas ni prioridades de campaña.

## Validación y límites

192 pruebas en38archivos aprobadas;8nuevas verifican CAGR, horizonte, coma/cero/decrecimiento, faltantes, base cero, ausencia de tasa de respaldo, no herencia a nuevas claves, registros inconsistentes, desbordamiento y mezclas de universo/corte/métrica/geometría. Compilación correcta. Se corrigió el tipado incompleto de una fixture detectado durante la compilación posterior a la primera corrida; no se modificó producción por esa corrección.

No se ejecutó comprobación interactiva de navegador ni móvil. La evidencia de pruebas/compilación no certifica fuentes electorales ni equivalencia de límites. No se afirma que exista una proyección oficial seccional2027. Pendientes: instalación de Alex, prueba visual de esta consulta y auditoría final de los tres primeros módulos.

Fuentes: referencia censal2020 con SHA256 del CSV en sus metadatos; LN2018/2021/2024 de CORE con huellas de fuente electoral y geométrica expuestas en la consulta. Se conservan los reportes de los pasos anteriores.
