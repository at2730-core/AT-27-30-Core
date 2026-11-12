import {
  type FormEvent,
  useEffect,
  useRef,
  useState,
} from 'react'
import {
  AuthClientError,
  type AuthSession,
  login,
} from '../gateway/auth.client'
import './LoginScreen.css'

interface LoginScreenProps {
  onAuthenticated: (
    session: AuthSession,
  ) => void
}

export function LoginScreen({
  onAuthenticated,
}: LoginScreenProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [pending, setPending] = useState(false)
  const [errorMessage, setErrorMessage] = (
    useState<string | null>(null)
  )

  const activeRequest = useRef<
    AbortController | null
  >(null)
  const mounted = useRef(true)

  useEffect(() => {
    mounted.current = true

    return () => {
      mounted.current = false
      activeRequest.current?.abort()
    }
  }, [])

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    const normalizedUsername = username.trim()

    if (!normalizedUsername || !password) {
      setErrorMessage(
        'Captura tu usuario y contrasena.',
      )
      return
    }

    const controller = new AbortController()
    activeRequest.current = controller
    setPending(true)
    setErrorMessage(null)

    try {
      const session = await login(
        normalizedUsername,
        password,
        controller.signal,
      )

      if (!mounted.current) {
        return
      }

      setPassword('')
      onAuthenticated(session)
    } catch (error) {
      if (
        !mounted.current
        || controller.signal.aborted
      ) {
        return
      }

      if (error instanceof AuthClientError) {
        setErrorMessage(error.message)
      } else {
        setErrorMessage(
          'No fue posible iniciar sesion.',
        )
      }
    } finally {
      if (
        mounted.current
        && activeRequest.current === controller
      ) {
        activeRequest.current = null
        setPending(false)
      }
    }
  }

  return (
    <main className="heyti-login-screen">
      <section
        className="heyti-login-card"
        aria-labelledby="heyti-login-title"
      >
        <header className="heyti-login-brand">
          <div
            className="heyti-login-mark"
            aria-hidden="true"
          >
            H
          </div>

          <div>
            <p className="heyti-login-product">
              HEYTI-CORE
            </p>
            <h1 id="heyti-login-title">
              Acceso seguro
            </h1>
            <p className="heyti-login-subtitle">
              Inteligencia territorial
            </p>
          </div>
        </header>

        <div className="heyti-login-divider" />

        <form
          className="heyti-login-form"
          onSubmit={handleSubmit}
          noValidate
        >
          <div className="heyti-login-heading">
            <h2>Inicia sesi&oacute;n</h2>
            <p>
              Utiliza las credenciales asignadas
              para HEYTI.
            </p>
          </div>

          <label className="heyti-login-field">
            <span>Usuario</span>
            <input
              type="text"
              name="username"
              autoComplete="username"
              value={username}
              disabled={pending}
              onChange={(event) => {
                setUsername(event.target.value)
              }}
              autoFocus
            />
          </label>

          <label className="heyti-login-field">
            <span>Contrase&ntilde;a</span>
            <input
              type="password"
              name="password"
              autoComplete="current-password"
              value={password}
              disabled={pending}
              onChange={(event) => {
                setPassword(event.target.value)
              }}
            />
          </label>

          {errorMessage ? (
            <div
              className="heyti-login-error"
              role="alert"
            >
              {errorMessage}
            </div>
          ) : null}

          <button
            className="heyti-login-submit"
            type="submit"
            disabled={pending}
          >
            {pending
              ? 'Validando...'
              : 'Entrar a HEYTI'}
          </button>
        </form>

        <footer className="heyti-login-footer">
          La contrase&ntilde;a se valida
          directamente en HEYTI-CORE.
        </footer>
      </section>
    </main>
  )
}
