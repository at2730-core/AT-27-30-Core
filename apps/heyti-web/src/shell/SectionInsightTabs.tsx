import { useEffect, useId, useRef, useState } from 'react'
import type { ReactNode, KeyboardEvent } from 'react'

interface SectionInsightTabsProps {
  selectedIndex?: number
  onSelectedIndexChange?: (index: number) => void
  electionYear: number | null
  summary: ReactNode
  current: ReactNode
  history: ReactNode
  trace: ReactNode
}

export function SectionInsightTabs({
  electionYear, summary, current, history, trace, selectedIndex, onSelectedIndexChange,
}: SectionInsightTabsProps) {
  const prefix = useId()
  const [localActive, setLocalActive] = useState(0)
  const active = selectedIndex ?? localActive
  const containerRef = useRef<HTMLDivElement>(null)
  const setActive = (index: number) => {
    setLocalActive(index)
    onSelectedIndexChange?.(index)
  }
  useEffect(() => {
    const body = containerRef.current?.closest('.heyti-floating-body')
    if (body) body.scrollTop = 0
  }, [active])
  const tabs = [
    { label: 'Resumen', content: summary },
    { label: electionYear ? `Elección ${electionYear}` : 'Elección', content: current },
    { label: 'Historial comparativo', content: history },
    { label: 'Trazabilidad', content: trace },
  ]

  function navigate(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number
    switch (event.key) {
      case 'ArrowRight': next = (index + 1) % tabs.length; break
      case 'ArrowLeft': next = (index + tabs.length - 1) % tabs.length; break
      case 'Home': next = 0; break
      case 'End': next = tabs.length - 1; break
      default: return
    }
    event.preventDefault()
    setActive(next)
    const buttons = event.currentTarget.parentElement?.querySelectorAll<HTMLButtonElement>('[role="tab"]')
    buttons?.[next]?.focus()
  }

  return (
    <div className="heyti-section-tabs" ref={containerRef}>
      <div className="heyti-section-tablist" role="tablist" aria-label="Información de la sección">
        {tabs.map((tab, index) => (
          <button key={tab.label} type="button" role="tab"
            id={`${prefix}-tab-${index}`} aria-controls={`${prefix}-panel-${index}`}
            aria-selected={active === index} tabIndex={active === index ? 0 : -1}
            onClick={() => setActive(index)} onKeyDown={event => navigate(event, index)}>
            {tab.label}
          </button>
        ))}
      </div>
      {tabs.map((tab, index) => (
        <section key={index} role="tabpanel" className="heyti-section-tab-content"
          id={`${prefix}-panel-${index}`} aria-labelledby={`${prefix}-tab-${index}`}
          hidden={active !== index} tabIndex={0}>
          {tab.content}
        </section>
      ))}
    </div>
  )
}
