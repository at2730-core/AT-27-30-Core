import { useState } from 'react'
import './App.css'
import { ApplicationShell } from './shell/ApplicationShell'
import { DemoNoticeScreen } from './startup/DemoNoticeScreen'
import { SplashScreen } from './startup/SplashScreen'

function App() {
  const [entered, setEntered] = useState(false)
  const [noticeAccepted, setNoticeAccepted] = useState(false)

  if (!entered) {
    return (
      <SplashScreen
        onEnter={() => setEntered(true)}
      />
    )
  }

  if (!noticeAccepted) {
    return <DemoNoticeScreen onAccept={() => setNoticeAccepted(true)} />
  }

  return <ApplicationShell />
}

export default App
