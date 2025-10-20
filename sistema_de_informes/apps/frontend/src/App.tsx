import { useEffect, useState, useRef } from 'react'
import './App.css'

// Configuración de URLs desde variables de entorno
const API_REST = import.meta.env.VITE_API_REST || 'http://localhost:8000'
const API_GRAPHQL = import.meta.env.VITE_API_GRAPHQL || 'http://localhost:4000/graphql'
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8080/ws'

interface Report {
  id: string
  title: string
  description: string
  status: string
  priority?: string
  location?: string
  created_at?: string
}

function App() {
  const [reportsREST, setReportsREST] = useState<Report[]>([])
  const [reportsGraphQL, setReportsGraphQL] = useState<Report[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notification, setNotification] = useState<string | null>(null)
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  // Función para cargar reportes desde REST API
  const fetchReportsREST = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_REST}/api/v1/reports`)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      const data = await response.json()
      setReportsREST(data)
    } catch (err) {
      setError(`Error al cargar reportes desde REST: ${err}`)
      console.error('Error fetching REST:', err)
    } finally {
      setLoading(false)
    }
  }

  // Función para cargar reportes desde GraphQL
  const fetchReportsGraphQL = async () => {
    setLoading(true)
    setError(null)
    try {
      const query = `
        query {
          reports {
            id
            title
            description
            status
            priority
          }
        }
      `
      
      const response = await fetch(API_GRAPHQL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      
      if (result.errors) {
        throw new Error(result.errors[0].message)
      }

      setReportsGraphQL(result.data.reports)
    } catch (err) {
      setError(`Error al cargar reportes desde GraphQL: ${err}`)
      console.error('Error fetching GraphQL:', err)
    } finally {
      setLoading(false)
    }
  }

  // Configurar conexión WebSocket
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        const ws = new WebSocket(WS_URL)
        
        ws.onopen = () => {
          console.log('WebSocket conectado')
          setWsConnected(true)
        }

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            if (data.event === 'new_report') {
              setNotification(data.message)
              // Recargar reportes automáticamente
              fetchReportsREST()
              fetchReportsGraphQL()
              // Ocultar notificación después de 5 segundos
              setTimeout(() => setNotification(null), 5000)
            }
          } catch (err) {
            console.error('Error parsing WebSocket message:', err)
          }
        }

        ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          setWsConnected(false)
        }

        ws.onclose = () => {
          console.log('WebSocket desconectado')
          setWsConnected(false)
          // Intentar reconectar después de 5 segundos
          setTimeout(connectWebSocket, 5000)
        }

        wsRef.current = ws
      } catch (err) {
        console.error('Error creating WebSocket:', err)
        setWsConnected(false)
      }
    }

    connectWebSocket()

    // Cleanup
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  // Cargar datos iniciales
  useEffect(() => {
    fetchReportsREST()
    fetchReportsGraphQL()
  }, [])

  return (
    <div className="container">
      <header>
        <h1>🏛️ Sistema de Reportes - ULEAM</h1>
        <p style={{ color: '#999', marginBottom: '2rem' }}>
          Integración completa: REST API + GraphQL + WebSocket
        </p>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <div className="btn-group">
            <button onClick={fetchReportsREST}>
              🔄 Actualizar REST
            </button>
            <button onClick={fetchReportsGraphQL}>
              🔄 Actualizar GraphQL
            </button>
          </div>
          
          <div className="ws-status">
            <div className={`ws-indicator ${!wsConnected ? 'disconnected' : ''}`}></div>
            <span>{wsConnected ? 'WebSocket Conectado' : 'WebSocket Desconectado'}</span>
          </div>
        </div>
      </header>

      {/* Notificación de WebSocket */}
      {notification && (
        <div className="notification">
          🔔 {notification}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="error">
          ❌ {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="loading">
          ⏳ Cargando reportes...
        </div>
      )}

      {/* Reportes desde REST API */}
      <section>
        <h2 className="section-title">
          📡 Reportes desde REST API ({reportsREST.length})
        </h2>
        {reportsREST.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay reportes disponibles</p>
        )}
        {reportsREST.map((report) => (
          <div key={`rest-${report.id}`} className="report-card">
            <h3 className="report-title">{report.title}</h3>
            <p className="report-description">{report.description}</p>
            <div className="report-meta">
              <span className={`status-badge status-${report.status.toLowerCase().replace(' ', '-')}`}>
                {report.status}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
              {report.location && <span>📍 {report.location}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* Reportes desde GraphQL */}
      <section>
        <h2 className="section-title">
          🔮 Reportes desde GraphQL ({reportsGraphQL.length})
        </h2>
        {reportsGraphQL.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay reportes disponibles</p>
        )}
        {reportsGraphQL.map((report) => (
          <div key={`graphql-${report.id}`} className="report-card">
            <h3 className="report-title">{report.title}</h3>
            <p className="report-description">{report.description}</p>
            <div className="report-meta">
              <span className={`status-badge status-${report.status?.toLowerCase().replace(' ', '-') || 'abierto'}`}>
                {report.status || 'N/A'}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
            </div>
          </div>
        ))}
      </section>

      <footer style={{ marginTop: '3rem', padding: '2rem 0', borderTop: '1px solid #333', color: '#666', textAlign: 'center' }}>
        <p>Sistema de Reportes de Infraestructura Universitaria - Semana 5</p>
        <p>Integrantes: Cinthia Zambrano (REST) | Carlos Campuzano (GraphQL) | Jereny Vera (WebSocket)</p>
      </footer>
    </div>
  )
}

export default App
