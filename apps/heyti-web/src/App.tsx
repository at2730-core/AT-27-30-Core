import { useState } from 'react'
import './App.css'
import type {
  AuthSession,
} from './gateway/auth.client'
import { ApplicationShell } from './shell/ApplicationShell'
import { DemoNoticeScreen } from './startup/DemoNoticeScreen'
import { LoginScreen } from './startup/LoginScreen'
import { SplashScreen } from './startup/SplashScreen'

function App() {
  const [entered, setEntered] = useState(false)
  const [session, setSession] = (
    useState<AuthSession | null>(null)
  )
  const [noticeAccepted, setNoticeAccepted] = (
    useState(false)
  )

  if (!entered) {
    return (
      <SplashScreen
        onEnter={() => setEntered(true)}
      />
    )
  }

  if (!session) {
    return (
      <LoginScreen
        onAuthenticated={setSession}
      />
    )
  }

  if (!noticeAccepted) {
    return (
      <DemoNoticeScreen
        onAccept={() => setNoticeAccepted(true)}
      />
    )
  }

  return <ApplicationShell />
}

export default App
