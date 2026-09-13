import { useState } from 'react'
import './App.css'
import { ApplicationShell } from './shell/ApplicationShell'
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

  return <ApplicationShell />
}

export default App
