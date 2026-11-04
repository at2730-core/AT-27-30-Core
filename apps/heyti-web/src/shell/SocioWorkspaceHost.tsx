import { useEffect, useState } from 'react'
import { SocioeconomicWorkspace } from './SocioeconomicWorkspace'
import { SocioEducationWorkspace } from './SocioEducationWorkspace'
import { SocioServicesWorkspace } from './SocioServicesWorkspace'
import { SocioMarginationWorkspace } from './SocioMarginationWorkspace'
import { SocioIncomeWorkspace } from './SocioIncomeWorkspace'
import { SocioPovertyWorkspace } from './SocioPovertyWorkspace'
import { SocioRuralWorkspace } from './SocioRuralWorkspace'
import { SocioProjectionWorkspace } from './SocioProjectionWorkspace'
import { rememberSocioView } from './socioWorkspaceMemory'
import type { SocioView } from './socioWorkspaceMemory'

const views = {
  'socio-indicators': SocioeconomicWorkspace,
  'socio-education': SocioEducationWorkspace,
  'socio-services': SocioServicesWorkspace,
  'socio-margination': SocioMarginationWorkspace,
  'socio-income': SocioIncomeWorkspace,
  'socio-poverty': SocioPovertyWorkspace,
  'socio-rural': SocioRuralWorkspace,
  'socio-projection': SocioProjectionWorkspace,
}

export function SocioWorkspaceHost({query, requestId}: {query: string; requestId: number}) {
  const [previous, setPrevious] = useState<SocioView>(() => rememberSocioView('socio-indicators', query))
  const selected = rememberSocioView(previous, query)
  useEffect(() => { setPrevious(selected) }, [selected])
  const View = views[selected]
  return <View requestId={requestId} />
}
