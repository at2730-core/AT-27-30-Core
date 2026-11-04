import {describe,expect,it,vi} from 'vitest'
import {renderToStaticMarkup} from 'react-dom/server'
import {WorkspaceContext} from '../platform/workspace.context'
import type {WorkspaceState} from '../platform/platform.types'
import {INITIAL_WORKSPACE_STATE} from '../platform/workspace.state'
import {ContextQueryDialog} from './ContextQueryDialog'
import {ComparisonWorkspace} from './ComparisonWorkspace'
import type {ReactNode} from 'react'
const state:WorkspaceState={...INITIAL_WORKSPACE_STATE,universe:{id:'228',level:'section',label:'Sección 228',parentId:null,truthStatus:'pending'},comparisonModuleIds:['territorial-analysis','win-all','socioeconomic']}
function render(children:ReactNode,workspace=state){return renderToStaticMarkup(<WorkspaceContext.Provider value={{state:workspace,setMapView:vi.fn(),selectModule:vi.fn(),selectUniverse:vi.fn(),setMode:vi.fn(),setComparisonModules:vi.fn()}}>{children}</WorkspaceContext.Provider>)}
describe('context panels initial UI',()=>{
 it('section cross query offers section paths and retains identity',()=>{
  const html=render(<ContextQueryDialog kind="cross-query" onClose={vi.fn()} onLaunch={vi.fn()}/>)
  expect(html).toContain('Sección 228');expect(html).toContain('section-history');expect(html).not.toContain('value="socio-indicators"');expect(html).toContain('aria-modal="true"')
 })
 it('comparison configuration offers exactly the three descriptive modules',()=>{
  const html=render(<ContextQueryDialog kind="comparison" onClose={vi.fn()} onLaunch={vi.fn()}/>)
  expect(html.match(/type="checkbox"/g)).toHaveLength(3);expect(html).toContain('Aplicar configuración')
 })
 it('comparison does not pretend to have numbers before query',()=>{
  const html=render(<ComparisonWorkspace onConfigure={vi.fn()}/>)
  expect(html).toContain('Sección 228');expect(html).toContain('Consultar perspectivas');expect(html).not.toContain('Resultados 2024 por sección');expect(html).toContain('Volver a Individual')
 })
})
