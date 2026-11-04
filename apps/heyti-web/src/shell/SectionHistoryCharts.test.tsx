import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import type { DemoContest, DemoContestId, SectionDemo } from '../gateway/section.demo'
import { SectionHistoryCharts, sectionHistoryChartModel } from './SectionHistoryCharts'
const make = (status = 'AVAILABLE', votes: DemoContest['votes'] = { PAN: 358, PRI: 40, PVEM: 38, MORENA: 32 }): DemoContest => ({ status, total: 511, nominal: 674, votes })
const years = (): SectionDemo['years'] => [2018, 2021, 2024].map(year => ({ year, contests: Object.fromEntries((['A', 'DL', 'DF', 'G', 'S', 'P'] as DemoContestId[]).map(id => [id, make()])) as Record<DemoContestId, DemoContest> }))
describe('Gráficas históricas de sección', () => {
  it('comparte escala entre años y conserva votos y orden de partidos', () => {
    const source = years(); source[2].contests.A.votes.PAN = 417
    const model = sectionHistoryChartModel(source, 'A')
    expect(model.charts.map(c => c.year)).toEqual([2018, 2021, 2024])
    expect(model.axisMax).toBeGreaterThanOrEqual(417)
    expect(model.charts[0].bars.map(b => b.party)).toEqual(['PAN', 'PRI', 'PVEM', 'MORENA'])
    expect(model.charts[2].bars[0].value).toBe(417)
    expect(model.ticks[0]).toBe(0)
  })
  it('distingue cero de N/D y no rellena votos faltantes', () => {
    const source = years(); source[0].contests.A.votes = { PAN: 0, PRI: null, PVEM: 3, MORENA: 1 }
    const model = sectionHistoryChartModel(source, 'A')
    expect(model.charts[0].bars[0].value).toBe(0)
    expect(model.charts[0].bars[1].value).toBeNull()
  })
  it('omite barras de elecciones no celebradas y cifras inconsistentes', () => {
    const source = years(); source[0].contests.G.status = 'INCONSISTENT'; source[1].contests.G.status = 'NOT_CONTESTED'
    const model = sectionHistoryChartModel(source, 'G')
    expect(model.charts[0].bars.every(b => b.value === null)).toBe(true)
    expect(model.charts[1].bars.every(b => b.value === null)).toBe(true)
    expect(model.charts[2].bars[0].value).toBe(358)
  })
  it('mantiene una escala finita con todos los valores ausentes', () => {
    const source = years(); source.forEach(y => y.contests.A.votes = { PAN: null, PRI: null, PVEM: null, MORENA: null })
    expect(sectionHistoryChartModel(source, 'A').axisMax).toBe(1)
    expect(sectionHistoryChartModel(source, 'A').ticks).toEqual([0, 1])
  })
  it('cambia de contienda sin modificar la fuente', () => {
    const source = years(); source[2].contests.DF.votes.PAN = 99
    const before = JSON.stringify(source)
    expect(sectionHistoryChartModel(source, 'DF').charts[2].bars[0].value).toBe(99)
    expect(sectionHistoryChartModel(source, 'A').charts[2].bars[0].value).toBe(358)
    expect(JSON.stringify(source)).toBe(before)
  })
  it('muestra tres gráficas accesibles y los datos exactos de la sección 1528', () => {
    const source = years(); source[1].contests.A = { ...make(), total: 509, nominal: 671, votes: { PAN: 410, PRI: 25, PVEM: 3, MORENA: 42 } }; source[2].contests.A = { ...make(), total: 535, nominal: 669, votes: { PAN: 417, PRI: 12, PVEM: 14, MORENA: 40 } }
    const html = renderToStaticMarkup(<SectionHistoryCharts years={source} contest="A" />)
    expect((html.match(/role="img"/g) ?? []).length).toBe(3)
    expect(html).toContain('PAN: 417 votos')
    expect(html).toContain('LN:')
    expect(html).toContain('N/D no se dibuja como cero')
  })
  it('un año no celebrado conserva su explicación accesible', () => {
    const source = years(); source[1].contests.G.status = 'NOT_CONTESTED'
    const html = renderToStaticMarkup(<SectionHistoryCharts years={source} contest="G" />)
    expect(html).toContain('Elección no celebrada; no se representan ceros')
  })
})
