import {describe,it,expect,vi} from 'vitest'
import {renderToStaticMarkup} from 'react-dom/server'
import {WorkspaceContext} from '../platform/workspace.context'
import {INITIAL_WORKSPACE_STATE} from '../platform/workspace.state'
import {TerritorialAreaPanel} from './TerritorialAreaPanel'
import {attachAreaReading} from './territorialAreaAnalysis'
import type {AreaKind} from './territorialAreaAnalysis'
import type {UniverseMap} from '../gateway/universe.client'
const value={state:{...INITIAL_WORKSPACE_STATE,universe:{id:'6',level:'local-district' as const,label:'Distrito local 6',parentId:'11',truthStatus:'pending' as const}},setMapView:vi.fn(),selectModule:vi.fn(),selectUniverse:vi.fn(),setMode:vi.fn(),setComparisonModules:vi.fn()}
function render(kind:AreaKind,result:UniverseMap|null=null){return renderToStaticMarkup(<WorkspaceContext.Provider value={value}><TerritorialAreaPanel kind={kind} result={result} onResult={vi.fn()} onPending={vi.fn()}/></WorkspaceContext.Provider>)}
describe('Controles de las consultas de área de AT',()=>{
 for(const kind of ['area-comparison','area-competitiveness','area-top3'] as const)it(kind+' ofrece universo, contienda y año sin exigir sección',()=>{const html=render(kind);expect((html.match(/<select/g)??[]).length).toBe(3);expect(html).toContain('Distritos federales');expect(html).toContain('Distritos locales');expect(html).toContain('Municipios');expect(html).toContain('Estado');expect(html).toContain('Diputaciones locales');expect(html).toContain('Consultar universo y pintar mapa');expect(html).toContain('No es necesario seleccionar una sección individual')})
 it('muestra filas y métricas del área recibida',()=>{const map:UniverseMap={universe:{level:'local-district',id:'6',label:'Distrito local 6',sections:1},year:2024,contest:'DL',metric:'leaders',sections:[{sectionId:'1261',geometry:{type:'Polygon',coordinates:[]} as never,status:'TRACKED_LEAD',leader:'PAN',total:200,votes:{PAN:100,PRI:60,PVEM:20,MORENA:10}}],counts:{PAN:1},coverage:{geographic:1,represented:1,blocked:0},provenance:{electoral_validation:'AUDIT_PENDING'}};const html=render('area-competitiveness',attachAreaReading([map],'area-competitiveness',2024));expect(html).toContain('Distrito local 6');expect(html).toContain('Diferencia pp');expect(html).toContain('20 pp');expect(html).toContain('1261');expect(html).not.toContain('Selecciona y consulta una sección')})
})
