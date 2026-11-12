import { useState } from 'react'
import './App.css'
import {
  AuthClientError,
  type AuthSession,
  logout,
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
  const [logoutPending, setLogoutPending] = (
    useState(false)
  )
  const [logoutError, setLogoutError] = (
    useState<string | null>(null)
  )

  async function handleLogout() {
    if (!session || logoutPending) {
      return
    }

    setLogoutPending(true)
    setLogoutError(null)

    try {
      await logout(session.sessionToken)
      setNoticeAccepted(false)
      setSession(null)
    } catch (error) {
      if (
        error instanceof AuthClientError
        && error.status === 401
      ) {
        setNoticeAccepted(false)
        setSession(null)
        return
      }

      setLogoutError(
        error instanceof AuthClientError
          ? error.message
          : 'No fue posible cerrar la sesion.',
      )
    } finally {
      setLogoutPending(false)
    }
  }

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
        onAuthenticated={(authenticatedSession) => {
          setLogoutError(null)
          setSession(authenticatedSession)
        }}
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

  return (
    <ApplicationShell
      user={session.user}
      logoutPending={logoutPending}
      logoutError={logoutError}
      onLogout={handleLogout}
    />
  )
}

export default App
