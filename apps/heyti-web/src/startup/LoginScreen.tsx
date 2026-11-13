import {
  type FormEvent,
  useEffect,
  useRef,
  useState,
} from 'react'

import {
  AuthClientError,
  type AuthSession,
  changePassword,
  login,
} from '../gateway/auth.client'

import './LoginScreen.css'

interface LoginScreenProps {
  onAuthenticated: (
    session: AuthSession,
  ) => void
}

type AccessStep =
  | 'LOGIN'
  | 'PASSWORD_CHANGE'

export function LoginScreen({
  onAuthenticated,
}: LoginScreenProps) {
  const [step, setStep] = useState<AccessStep>(
    'LOGIN',
  )
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [newPassword, setNewPassword] = (
    useState('')
  )
  const [confirmation, setConfirmation] = (
    useState('')
  )
  const [pending, setPending] = useState(false)
  const [errorMessage, setErrorMessage] = (
    useState<string | null>(null)
  )
  const [successMessage, setSuccessMessage] = (
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

  async function submitLogin(
    normalizedUsername: string,
    controller: AbortController,
  ) {
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

      if (
        error instanceof AuthClientError
        && error.code === (
          'PASSWORD_CHANGE_REQUIRED'
        )
      ) {
        setStep('PASSWORD_CHANGE')
        setErrorMessage(null)
        setSuccessMessage(null)
        return
      }

      setErrorMessage(
        error instanceof AuthClientError
          ? error.message
          : 'No fue posible iniciar sesion.',
      )
    }
  }

  async function submitPasswordChange(
    normalizedUsername: string,
    controller: AbortController,
  ) {
    if (!newPassword || !confirmation) {
      setErrorMessage(
        'Captura y confirma la nueva contrasena.',
      )
      return
    }

    if (newPassword !== confirmation) {
      setErrorMessage(
        'La confirmacion no coincide.',
      )
      return
    }

    try {
      await changePassword(
        normalizedUsername,
        password,
        newPassword,
        confirmation,
        controller.signal,
      )

      if (!mounted.current) {
        return
      }

      setPassword('')
      setNewPassword('')
      setConfirmation('')
      setStep('LOGIN')
      setErrorMessage(null)
      setSuccessMessage(
        'Contrasena actualizada. '
        + 'Ingresa con tu nueva contrasena.',
      )
    } catch (error) {
      if (
        !mounted.current
        || controller.signal.aborted
      ) {
        return
      }

      setErrorMessage(
        error instanceof AuthClientError
          ? error.message
          : (
            'No fue posible cambiar '
            + 'la contrasena.'
          ),
      )
    }
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    const normalizedUsername = username.trim()

    if (!normalizedUsername || !password) {
      setErrorMessage(
        step === 'LOGIN'
          ? 'Captura tu usuario y contrasena.'
          : (
            'Captura el usuario y la '
            + 'contrasena temporal.'
          ),
      )
      return
    }

    const controller = new AbortController()
    activeRequest.current = controller
    setPending(true)
    setErrorMessage(null)
    setSuccessMessage(null)

    try {
      if (step === 'LOGIN') {
        await submitLogin(
          normalizedUsername,
          controller,
        )
      } else {
        await submitPasswordChange(
          normalizedUsername,
          controller,
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

  const changingPassword = (
    step === 'PASSWORD_CHANGE'
  )

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
            <h2>
              {changingPassword
                ? 'Establece tu contraseña'
                : 'Inicia sesión'}
            </h2>
            <p>
              {changingPassword
                ? (
                  'Por seguridad debes reemplazar '
                  + 'la contraseña temporal.'
                )
                : (
                  'Utiliza las credenciales '
                  + 'asignadas para HEYTI.'
                )}
            </p>
          </div>

          <label className="heyti-login-field">
            <span>Usuario</span>
            <input
              type="text"
              name="username"
              autoComplete="username"
              value={username}
              disabled={pending || changingPassword}
              onChange={(event) => {
                setUsername(event.target.value)
              }}
              autoFocus
            />
          </label>

          <label className="heyti-login-field">
            <span>
              {changingPassword
                ? 'Contraseña temporal'
                : 'Contraseña'}
            </span>
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

          {changingPassword ? (
            <>
              <label className="heyti-login-field">
                <span>Nueva contrase&ntilde;a</span>
                <input
                  type="password"
                  name="new-password"
                  autoComplete="new-password"
                  value={newPassword}
                  disabled={pending}
                  onChange={(event) => {
                    setNewPassword(
                      event.target.value,
                    )
                  }}
                  autoFocus
                />
              </label>

              <label className="heyti-login-field">
                <span>
                  Confirma la nueva contrase&ntilde;a
                </span>
                <input
                  type="password"
                  name="confirmation"
                  autoComplete="new-password"
                  value={confirmation}
                  disabled={pending}
                  onChange={(event) => {
                    setConfirmation(
                      event.target.value,
                    )
                  }}
                />
              </label>
            </>
          ) : null}

          {errorMessage ? (
            <div
              className="heyti-login-error"
              role="alert"
            >
              {errorMessage}
            </div>
          ) : null}

          {successMessage ? (
            <div
              className="heyti-login-success"
              role="status"
            >
              {successMessage}
            </div>
          ) : null}

          <button
            className="heyti-login-submit"
            type="submit"
            disabled={pending}
          >
            {pending
              ? 'Procesando...'
              : (
                changingPassword
                  ? 'Guardar nueva contraseña'
                  : 'Entrar a HEYTI'
              )}
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
