export function MasterOnlyCoverageNote({count}: {count:number|undefined}) {
  return <p className="heyti-party-chart-note"><strong>Archivo completo de Guanajuato:</strong> {count===undefined
    ? 'el CORE no informó el número de identidades presentes solo en el maestro.'
    : `${count.toLocaleString('es-MX')} identidades presentes solo en el maestro, sin geometría representada en este mapa.`} Esta referencia global no es un conteo de casos del distrito o municipio consultado.</p>
}

export function GeographicDataScope({universe,unit,year,source}: {universe:string;unit:'municipio completo'|'localidad urbana completa'|'AGEB urbana completa';year:number;source:string}) {
  return <section className="heyti-data-panel-detail" aria-label="Unidad geográfica del dato">
    <p><strong>Unidad del dato:</strong> {unit}.</p>
    <p><strong>Universo de referencia:</strong> {universe}.</p>
    <p><strong>Año del dato:</strong> {year} · {source}.</p>
    <p>Se muestra cada unidad completa. La intersección con el universo no reparte sus cifras entre secciones ni produce automáticamente un valor distrital.</p>
  </section>
}
