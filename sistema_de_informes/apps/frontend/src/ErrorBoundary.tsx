import React from 'react'

type Props = {
  children: React.ReactNode
}

type State = {
  hasError: boolean
  error?: unknown
}

export default class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false }

  static getDerivedStateFromError(error: unknown): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: unknown) {
    // Mantenerlo simple: al menos lo vemos en consola.
    console.error('Frontend render error:', error)
  }

  render() {
    if (this.state.hasError) {
      const msg =
        this.state.error instanceof Error
          ? this.state.error.message
          : String(this.state.error)

      return (
        <div style={{ padding: 16, fontFamily: 'system-ui, sans-serif' }}>
          <h2 style={{ color: '#f44336' }}>Se produjo un error al renderizar el frontend</h2>
          <p style={{ color: '#999' }}>
            Abre la consola del navegador (F12) para ver más detalles.
          </p>
          <pre style={{ whiteSpace: 'pre-wrap', color: '#fff' }}>{msg}</pre>
        </div>
      )
    }

    return this.props.children
  }
}
