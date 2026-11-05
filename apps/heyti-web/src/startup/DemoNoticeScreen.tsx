import { useEffect, useRef } from 'react'
import './SplashScreen.css'

export function DemoNoticeScreen({ onAccept }: { onAccept: () => void }) {
  const acceptRef = useRef<HTMLButtonElement>(null)
  useEffect(() => { acceptRef.current?.focus() }, [])
  return (
    <main className="splash" aria-labelledby="demo-notice-title">
      <section className="splash-card" style={{ width: 'min(100%, 42rem)' }}>
        <header className="splash-header">
          <div className="splash-mark" aria-hidden="true">H</div>
          <div>
            <p className="splash-eyebrow">HEYTI V2 · DEMOSTRACIÓN</p>
            <h1 id="demo-notice-title" style={{ fontSize: 'clamp(1.5rem, 4vw, 2rem)', lineHeight: 1.2 }}>Fuentes y geografía en auditoría</h1>
          </div>
        </header>
        <div style={{ marginTop: 24, color: '#43585d', lineHeight: 1.7 }}>
          <p>HEYTI utiliza fuentes electorales oficiales del INE y del IEEG. Estamos auditando las fuentes de datos, su integración y trazabilidad para verificar que lo mostrado corresponda a la fuente y al corte identificado.</p>
          <p>Esta versión es una demostración y puede contener datos pendientes de validación, señalados en pantalla.</p>
          <p>La geografía mostrada corresponde a la referencia actualmente disponible en HEYTI y todavía no constituye el Marco Geográfico Electoral 2026–2027. El INE anunció la publicación de los productos cartográficos correspondientes para el 12 de noviembre de 2026; serán incorporados después de su descarga y conciliación.</p>
          <p>Los datos de Campo y los escenarios indicarán su propia procedencia y estado de validación.</p>
        </div>
        <button ref={acceptRef} className="splash-button" type="button" onClick={onAccept}>ACEPTAR</button>
      </section>
    </main>
  )
}
