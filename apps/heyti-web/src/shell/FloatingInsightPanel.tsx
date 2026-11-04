import { useEffect, useLayoutEffect, useId, useRef, useState } from 'react'
import type { ReactNode } from 'react'

let panelStack = 40

function initialPosition() {
  return {
    x: Math.max(12, window.innerWidth - 472),
    y: Math.min(100, Math.max(12, window.innerHeight - 300)),
  }
}

export function FloatingInsightPanel({
  children, title = "Lectura del módulo", onClose, comparative = false, minimizable = false, expandRequest = 0, initiallyExpanded = false,
}: {
  children: ReactNode
  title?: string
  onClose?: () => void
  comparative?: boolean
  minimizable?: boolean
  initiallyExpanded?: boolean
  expandRequest?: number
}) {
  const titleId = useId()
  const defaultPosition = () => minimizable
    ? { x: Math.max(12, window.innerWidth - 472), y: Math.max(12, window.innerHeight - Math.min(600, window.innerHeight - 120) - 12) }
    : comparative
    ? { x: Math.max(12, Math.min(280, window.innerWidth - 472)), y: Math.min(150, Math.max(12, window.innerHeight - 300)) }
    : initialPosition()
  const panelRef = useRef<HTMLElement>(null)
  const dragRef = useRef<{
    pointerId: number
    startX: number
    startY: number
    x: number
    y: number
  } | null>(null)
  const [minimized, setMinimized] = useState(minimizable && !initiallyExpanded)
  const [savedSize, setSavedSize] = useState<{ width: number; height: number } | null>(null)
  const bodyId = useId()
  const previousRequest = useRef(expandRequest)
  useEffect(() => {
    if (expandRequest !== previousRequest.current) {
      previousRequest.current = expandRequest
      if (minimizable) setMinimized(false)
      if (panelRef.current) panelRef.current.style.zIndex = String(++panelStack)
    }
  }, [expandRequest, minimizable])
  const [position, setPosition] = useState(defaultPosition)

  function moveTo(x: number, y: number) {
    const rect = panelRef.current?.getBoundingClientRect()
    const width = rect?.width ?? 460
    const height = rect?.height ?? 500
    setPosition({
      x: Math.max(12, Math.min(x, window.innerWidth - width - 12)),
      y: Math.max(12, Math.min(y, window.innerHeight - height - 12)),
    })
  }

  function toggleMinimized() {
    if (!minimized) {
      const rect = panelRef.current?.getBoundingClientRect()
      if (rect) setSavedSize({ width: rect.width, height: rect.height })
    }
    dragRef.current = null
    setMinimized(current => !current)
  }

  useLayoutEffect(() => {
    if (minimizable && !minimized) moveTo(position.x, position.y)
  }, [minimized, savedSize, minimizable])

  function resetPanel() {
    setSavedSize(null)
    const panel = panelRef.current
    if (panel) {
      panel.style.width = ''
      panel.style.height = ''
    }
    setPosition(defaultPosition())
  }

  useEffect(() => {
    function keepVisible() {
      const rect = panelRef.current?.getBoundingClientRect()
      if (!rect || minimized) return
      setPosition(current => ({
        x: Math.max(12, Math.min(current.x, window.innerWidth - rect.width - 12)),
        y: Math.max(12, Math.min(current.y, window.innerHeight - rect.height - 12)),
      }))
    }
    window.addEventListener('resize', keepVisible)
    return () => window.removeEventListener('resize', keepVisible)
  }, [minimized])

  return (
    <aside
      ref={panelRef}
      onPointerDownCapture={() => { if (panelRef.current) panelRef.current.style.zIndex = String(++panelStack) }}
      onFocusCapture={() => { if (panelRef.current) panelRef.current.style.zIndex = String(++panelStack) }}
      className="workspace-insight-panel heyti-floating-insight"
      aria-labelledby={titleId}
      style={minimized ? {
        right: 12, bottom: 12, left: 'auto', top: 'auto', height: 'auto', minHeight: 0,
        width: 'min(460px, calc(100vw - 24px))', resize: 'none',
      } : { left: position.x, top: position.y, width: savedSize?.width, height: savedSize?.height }}
    >
      <header
        className="heyti-floating-header"
        tabIndex={minimized ? -1 : 0}
        style={{ cursor: minimized ? 'default' : 'move' }}
        aria-label={minimized ? title : `Mover ${title}: arrastra o utiliza las flechas del teclado`}
        onPointerDown={event => {
          if (
            minimized || event.button !== 0 ||
            (event.target as HTMLElement).closest('button')
          ) return
          dragRef.current = {
            pointerId: event.pointerId,
            startX: event.clientX,
            startY: event.clientY,
            x: position.x,
            y: position.y,
          }
          event.currentTarget.setPointerCapture(event.pointerId)
          event.currentTarget.focus()
          event.preventDefault()
        }}
        onPointerMove={event => {
          const drag = dragRef.current
          if (!drag || drag.pointerId !== event.pointerId) return
          moveTo(
            drag.x + event.clientX - drag.startX,
            drag.y + event.clientY - drag.startY,
          )
        }}
        onPointerUp={event => {
          if (event.currentTarget.hasPointerCapture(event.pointerId)) {
            event.currentTarget.releasePointerCapture(event.pointerId)
          }
          dragRef.current = null
        }}
        onPointerCancel={() => { dragRef.current = null }}
        onLostPointerCapture={() => { dragRef.current = null }}
        onKeyDown={event => {
          if (minimized || event.target !== event.currentTarget) return
          const step = event.shiftKey ? 40 : 10
          const directions: Record<string, [number, number]> = {
            ArrowLeft: [-step, 0],
            ArrowRight: [step, 0],
            ArrowUp: [0, -step],
            ArrowDown: [0, step],
          }
          const delta = directions[event.key]
          if (!delta) return
          event.preventDefault()
          moveTo(position.x + delta[0], position.y + delta[1])
        }}
      >
        <div>
          <p hidden={minimized} style={{ display: minimized ? 'none' : undefined }}>RESPUESTA HEYTI</p>
          <h2 id={titleId}>{title}</h2>
        </div>
        {minimizable ? <button type="button" aria-expanded={!minimized} aria-controls={bodyId} onClick={toggleMinimized}>
          {minimized ? 'Expandir' : 'Minimizar'}
        </button> : null}
        <button hidden={minimized} style={{ display: minimized ? 'none' : undefined }} type="button" onClick={resetPanel}>
          Restablecer
        </button>
        {onClose ? <button type="button" onClick={onClose} aria-label={`Cerrar ${title}`}>Cerrar</button> : null}
      </header>
      <div id={bodyId} hidden={minimized} style={{ display: minimized ? 'none' : undefined }} className="heyti-floating-body">{children}</div>
      <div hidden={minimized} style={{ display: minimized ? 'none' : undefined }} className="heyti-floating-footer">
        Arrastra el encabezado · Ajusta desde la esquina inferior derecha
      </div>
    </aside>
  )
}