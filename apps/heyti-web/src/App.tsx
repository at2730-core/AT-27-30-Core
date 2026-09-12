import { useState } from 'react'
import './App.css'
import { SplashScreen } from './startup/SplashScreen'

function App() {
  const [entered, setEntered] = useState(false)

  if (!entered) {
    return (
      <SplashScreen
        onEnter={() => setEntered(true)}
      />
    )
  }

  return (
    <main className="app-foundation">
      <section
        className="foundation-card"
        aria-labelledby="heyti-title"
      >
        <p className="foundation-eyebrow">HEYTI-CORE</p>

        <h1 id="heyti-title">Espacio de trabajo</h1>

        <p className="foundation-message">
          El Workspace unificado será el siguiente corte
          vertical de HEYTI V2.0.
        </p>
      </section>
    </main>
  )
}

export default App
