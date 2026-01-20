import { useEffect, useState, useRef } from 'react'
import PdfUploader from './components/PdfUploader'
import ImageUploader from './components/ImageUploader'
import ChatUI from './components/ChatUI'
import Payments from './components/Payments'
import './App.css'

// Configuración de URLs desde variables de entorno.
// Segundo Parcial: por defecto todo pasa por el API Gateway (P1 integración).
const API_REST = import.meta.env.VITE_API_REST || 'http://localhost:9000'
// GraphQL recomendado vía gateway (proxy HTTP)
const API_GRAPHQL = import.meta.env.VITE_API_GRAPHQL || 'http://localhost:9000/graphql'
// WebSocket recomendado vía gateway (proxy WS)
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:9000/ws?room=reports'

interface Report {
  id: string
  title: string
  description: string
  status: string
  priority?: string
  location?: string
  created_at?: string
}

interface Category { id: string | number; name: string; description?: string; priority?: string; status?: string }
interface Area { id: string | number; name: string; location?: string; responsable?: string; description?: string }
interface State { id: string | number; name: string; description?: string; color?: string; order?: number; final?: boolean }
interface Role { id: string | number; name: string; description?: string; permissions?: string }
interface User { id: string | number; name: string; email: string; status?: string; role_id?: number }
interface Comment { id: string | number; report_id: number; user_id: number; content: string; date: string }
interface Rating { id: string | number; report_id: number; user_id: number; value: number; date: string }
interface FileItem { id: string | number; report_id: number; name: string; type?: string; url: string }
interface Tag { id: string | number; name: string; color?: string }

function App() {
  // Estado para texto extraído del PDF
  const [pdfText, setPdfText] = useState<string | null>(null)
  // Estado para imagen en base64 (DataURL)
  const [imageBase64, setImageBase64] = useState<string | null>(null)

  // AI Orchestrator recomendado vía gateway (/ai -> proxy)
  const API_AI = import.meta.env.VITE_AI_ORCHESTRATOR || 'http://localhost:9000/ai'

  // Handler para enviar mensaje al AI Orchestrator
  const handleChatSend = async (message: string) => {
    // Si hay texto PDF, lo pasamos como argumento a una tool real que consume texto
    const body: any = { message }
    if (imageBase64) {
      body.toolName = 'image_inspect'
      body.toolArgs = { image_base64: imageBase64 }
    } else if (pdfText) {
      body.toolName = 'pdf_inspect'
      body.toolArgs = { text: pdfText }
    }

    const res = await fetch(`${API_AI}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    if (!res.ok) return 'Error en AI Orchestrator'
    const data = await res.json()
    return data.reply
  }
  const [reportsREST, setReportsREST] = useState<Report[]>([])
  const [reportsGraphQL, setReportsGraphQL] = useState<Report[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notification, setNotification] = useState<string | null>(null)
  const [wsConnected, setWsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  // Otras entidades
  const [categoriesREST, setCategoriesREST] = useState<Category[]>([])
  const [areasREST, setAreasREST] = useState<Area[]>([])
  const [statesREST, setStatesREST] = useState<State[]>([])
  const [categoriesGraphQL, setCategoriesGraphQL] = useState<Category[]>([])
  const [areasGraphQL, setAreasGraphQL] = useState<Area[]>([])
  const [statesGraphQL, setStatesGraphQL] = useState<State[]>([])
  const [rolesREST, setRolesREST] = useState<Role[]>([])
  const [usersREST, setUsersREST] = useState<User[]>([])
  const [commentsREST, setCommentsREST] = useState<Comment[]>([])
  const [ratingsREST, setRatingsREST] = useState<Rating[]>([])
  const [filesREST, setFilesREST] = useState<FileItem[]>([])
  const [tagsREST, setTagsREST] = useState<Tag[]>([])
  const [rolesGraphQL, setRolesGraphQL] = useState<Role[]>([])
  const [usersGraphQL, setUsersGraphQL] = useState<User[]>([])
  const [commentsGraphQL, setCommentsGraphQL] = useState<Comment[]>([])
  const [ratingsGraphQL, setRatingsGraphQL] = useState<Rating[]>([])
  const [filesGraphQL, setFilesGraphQL] = useState<FileItem[]>([])
  const [tagsGraphQL, setTagsGraphQL] = useState<Tag[]>([])
  // KPIs (GraphQL → Queries Analíticas)
  const [analyticsTotal, setAnalyticsTotal] = useState<number>(0)
  const [analyticsByStatus, setAnalyticsByStatus] = useState<Array<{ clave: string; valor: number }>>([])
  const [statsReportes, setStatsReportes] = useState<{ total: number; abiertos: number; cerrados: number; enProceso: number }>({ total: 0, abiertos: 0, cerrados: 0, enProceso: 0 })
  const [topAreas, setTopAreas] = useState<Array<{ area: string; cantidad: number }>>([])
  const [promedioPuntuaciones, setPromedioPuntuaciones] = useState<number>(0)

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
      // cargar demás entidades REST
      const [cats, ars, sts, rls, usrs, cmt, rts, fls, tgs] = await Promise.all([
        fetch(`${API_REST}/api/v1/categories`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/areas`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/states`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/roles`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/users`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/comments`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/ratings`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/files`).then(r=>r.ok?r.json():[]).catch(()=>[]),
        fetch(`${API_REST}/api/v1/tags`).then(r=>r.ok?r.json():[]).catch(()=>[]),
      ])
      setCategoriesREST(cats)
      setAreasREST(ars)
      setStatesREST(sts)
      setRolesREST(rls)
      setUsersREST(usrs)
      setCommentsREST(cmt)
      setRatingsREST(rts)
      setFilesREST(fls)
      setTagsREST(tgs)
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
      // Importante: en el esquema GraphQL `reports` devuelve un objeto
      // de tipo ReportConnection con la forma { items, total, limit, offset }.
      // Por eso hay que pedir `items { ... }` y no directamente una lista.
      const query = `
        query {
          reports {
            total
            items {
              id
              title
              description
              status
              priority
            }
          }
          reportsAnalytics {
            total
            byStatus { clave valor }
          }
          categories { id name description priority status }
          areas { id name location responsable description }
          states { id name description color order final }
          roles { id name description permissions }
          users { id name email status role_id }
          comments { id report_id user_id content date }
          ratings { id report_id user_id value date }
          files { id report_id name type url }
          tags { id name color }
        }
      `
      
      // Helper para ejecutar una petición GraphQL
      const doFetch = async (endpoint: string) =>
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        })

      // 1er intento con el endpoint configurado (por defecto la raíz)
      let response = await doFetch(API_GRAPHQL)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  let result: any = null
      try {
        result = await response.json()
      } catch {
        result = null
      }

      // Si falla, probamos automáticamente la ruta alterna "/graphql" o la raíz
      if (!response.ok || result?.errors) {
        const alt = API_GRAPHQL.replace(/\/$/, '').endsWith('/graphql')
          ? API_GRAPHQL.replace(/\/graphql\/?$/, '')
          : `${API_GRAPHQL.replace(/\/$/, '')}/graphql`

        response = await doFetch(alt)
        try {
          result = await response.json()
        } catch {
          result = null
        }

        if (!response.ok || result?.errors) {
          const msg = result?.errors?.[0]?.message || `HTTP error! status: ${response.status}`
          throw new Error(msg)
        }
      }

      /*
      const response = await fetch(API_GRAPHQL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      // Algunos errores de GraphQL devuelven 400 con un cuerpo JSON con "errors".
      // Intentamos parsear siempre la respuesta para mostrar mejor el mensaje.
      const result = await response.json().catch(() => null)

      if (!response.ok) {
        const msg = result?.errors?.[0]?.message || `HTTP error! status: ${response.status}`
        throw new Error(msg)
      }
      */
      
      if (result.errors) {
        throw new Error(result.errors[0].message)
      }
  const items = result?.data?.reports?.items ?? []
  setReportsGraphQL(items)
  setAnalyticsTotal(result?.data?.reportsAnalytics?.total ?? 0)
  setAnalyticsByStatus(result?.data?.reportsAnalytics?.byStatus ?? [])
  setCategoriesGraphQL(result?.data?.categories ?? [])
  setAreasGraphQL(result?.data?.areas ?? [])
  setStatesGraphQL(result?.data?.states ?? [])
  setRolesGraphQL(result?.data?.roles ?? [])
  setUsersGraphQL(result?.data?.users ?? [])
  setCommentsGraphQL(result?.data?.comments ?? [])
  setRatingsGraphQL(result?.data?.ratings ?? [])
  setFilesGraphQL(result?.data?.files ?? [])
  setTagsGraphQL(result?.data?.tags ?? [])
    } catch (err) {
      setError(`Error al cargar reportes desde GraphQL: ${err}`)
      console.error('Error fetching GraphQL:', err)
    } finally {
      setLoading(false)
    }
  }

  // 🆕 Función para cargar queries analíticas de GraphQL
  const fetchAnalyticsGraphQL = async () => {
    try {
      const query = `
        query {
          statsReportes {
            total
            abiertos
            cerrados
            enProceso
          }
          topAreas(limit: 3) {
            area
            cantidad
          }
          promedioPuntuaciones
        }
      `
      
      const doFetch = async (endpoint: string) =>
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        })

      let response = await doFetch(API_GRAPHQL)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let result: any = null
      try {
        result = await response.json()
      } catch {
        result = null
      }

      // Fallback a /graphql si falla
      if (!response.ok || result?.errors) {
        const alt = API_GRAPHQL.replace(/\/$/, '').endsWith('/graphql')
          ? API_GRAPHQL.replace(/\/graphql\/?$/, '')
          : `${API_GRAPHQL.replace(/\/$/, '')}/graphql`

        response = await doFetch(alt)
        try {
          result = await response.json()
        } catch {
          result = null
        }
      }

      if (result?.data) {
        setStatsReportes(result.data.statsReportes || { total: 0, abiertos: 0, cerrados: 0, enProceso: 0 })
        setTopAreas(result.data.topAreas || [])
        setPromedioPuntuaciones(result.data.promedioPuntuaciones || 0)
      }
    } catch (err) {
      console.error('Error al cargar analytics desde GraphQL:', err)
    }
  }

  // 🆕 Función para descargar reporte PDF desde GraphQL
  const downloadReportPDF = async (reporteId: string) => {
    try {
      const query = `
        query {
          reportAnalytics(reporteId: "${reporteId}", formato: "pdf") {
            pdfBase64
            reporte {
              title
            }
          }
        }
      `
      
      const doFetch = async (endpoint: string) =>
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        })

      let response = await doFetch(API_GRAPHQL)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      let result: any = null
      try {
        result = await response.json()
      } catch {
        result = null
      }

      // Fallback a /graphql si falla
      if (!response.ok || result?.errors) {
        const alt = API_GRAPHQL.replace(/\/$/, '').endsWith('/graphql')
          ? API_GRAPHQL.replace(/\/graphql\/?$/, '')
          : `${API_GRAPHQL.replace(/\/$/, '')}/graphql`

        response = await doFetch(alt)
        try {
          result = await response.json()
        } catch {
          result = null
        }
      }

      if (result?.data?.reportAnalytics?.pdfBase64) {
        const pdfBase64 = result.data.reportAnalytics.pdfBase64
        const reportTitle = result.data.reportAnalytics.reporte?.title || 'reporte'
        
        // Crear link de descarga
        const link = document.createElement('a')
        link.href = 'data:application/pdf;base64,' + pdfBase64
        link.download = `${reportTitle.replace(/[^a-zA-Z0-9]/g, '_')}_analytics.pdf`
        link.click()
        
        setNotification(`PDF descargado: ${reportTitle}`)
        setTimeout(() => setNotification(null), 3000)
      } else {
        throw new Error('No se pudo generar el PDF')
      }
    } catch (err) {
      setError(`Error al descargar PDF: ${err}`)
      console.error('Error downloading PDF:', err)
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
            // Para cualquier evento, refrescamos todo
            setNotification(data.message || 'Actualización recibida')
            fetchReportsREST()
            fetchReportsGraphQL()
            fetchAnalyticsGraphQL() // 🆕 Actualizar analytics también
            setTimeout(() => setNotification(null), 5000)
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
    fetchAnalyticsGraphQL() // 🆕 Cargar queries analíticas
  }, [])

  const safeText = (value: unknown, fallback: string) => {
    if (typeof value !== 'string') return fallback
    const trimmed = value.trim()
    return trimmed ? trimmed : fallback
  }

  const toSlug = (value: unknown, fallback: string) =>
    safeText(value, fallback).toLowerCase().replace(/\s+/g, '-')

  return (
    <div className="container">
      {/* =====================
           SEMANA 4: PDF + CHAT + PAGOS
         ===================== */}
      <section>
        <h2>Semana 4 - Integración Multimodal y Pagos</h2>
        <PdfUploader onExtractedText={setPdfText} />
        <ImageUploader onImageBase64={setImageBase64} />
        <ChatUI onSend={handleChatSend} pdfText={pdfText || undefined} />
        <Payments />
      </section>
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
            <button onClick={fetchAnalyticsGraphQL}>
              📊 Actualizar Analytics
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

      {/* =====================
           DASHBOARD ANALÍTICO
           (Queries GraphQL)
          ===================== */}
      <section style={{ marginBottom: '3rem' }}>
        <h2 className="section-title">📊 Dashboard Analítico (GraphQL)</h2>
        
        {/* KPIs Principales */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '1rem', 
          marginBottom: '2rem' 
        }}>
          <div className="kpi-card" style={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
            color: 'white', 
            padding: '1.5rem', 
            borderRadius: '12px', 
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>{statsReportes.total}</div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total Reportes</div>
          </div>
          
          <div className="kpi-card" style={{ 
            background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', 
            color: 'white', 
            padding: '1.5rem', 
            borderRadius: '12px', 
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>{statsReportes.abiertos}</div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Abiertos</div>
          </div>
          
          <div className="kpi-card" style={{ 
            background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', 
            color: 'white', 
            padding: '1.5rem', 
            borderRadius: '12px', 
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>{statsReportes.enProceso}</div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>En Proceso</div>
          </div>
          
          <div className="kpi-card" style={{ 
            background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', 
            color: 'white', 
            padding: '1.5rem', 
            borderRadius: '12px', 
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>{statsReportes.cerrados}</div>
            <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Cerrados</div>
          </div>
        </div>

        {/* Top Áreas */}
        <div style={{ 
          background: 'white', 
          padding: '1.5rem', 
          borderRadius: '12px', 
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          marginBottom: '1.5rem'
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.2rem' }}>🏆 Top 3 Áreas con Más Reportes</h3>
          {topAreas.length === 0 ? (
            <p style={{ color: '#999' }}>No hay datos disponibles</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {topAreas.map((area, index) => (
                <div key={area.area} style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '1rem',
                  padding: '0.75rem',
                  background: index === 0 ? '#fff3cd' : index === 1 ? '#d1ecf1' : '#f8d7da',
                  borderRadius: '8px'
                }}>
                  <div style={{ 
                    fontSize: '1.5rem', 
                    fontWeight: 'bold',
                    width: '40px',
                    textAlign: 'center'
                  }}>
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 'bold' }}>{area.area}</div>
                    <div style={{ fontSize: '0.9rem', color: '#666' }}>{area.cantidad} reportes</div>
                  </div>
                  <div style={{ 
                    background: 'rgba(0,0,0,0.1)', 
                    padding: '0.5rem 1rem', 
                    borderRadius: '20px',
                    fontWeight: 'bold'
                  }}>
                    {area.cantidad}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Promedio Puntuaciones */}
        <div style={{ 
          background: 'white', 
          padding: '1.5rem', 
          borderRadius: '12px', 
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)' 
        }}>
          <h3 style={{ marginBottom: '1rem', fontSize: '1.2rem' }}>⭐ Promedio de Puntuaciones</h3>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '1rem',
            fontSize: '3rem',
            fontWeight: 'bold',
            color: promedioPuntuaciones >= 4 ? '#28a745' : promedioPuntuaciones >= 3 ? '#ffc107' : '#dc3545'
          }}>
            <span>{promedioPuntuaciones.toFixed(2)}</span>
            <span style={{ fontSize: '2rem', opacity: 0.5 }}>/ 5.0</span>
          </div>
          <div style={{ 
            marginTop: '1rem',
            padding: '0.5rem',
            background: promedioPuntuaciones >= 4 ? '#d4edda' : promedioPuntuaciones >= 3 ? '#fff3cd' : '#f8d7da',
            borderRadius: '8px',
            fontSize: '0.9rem'
          }}>
            {promedioPuntuaciones >= 4 ? '✅ Excelente calificación' : 
             promedioPuntuaciones >= 3 ? '⚠️ Calificación aceptable' : 
             '❌ Requiere mejoras'}
          </div>
        </div>
      </section>

      {/* =====================
           BLOQUE: REST
          (10 entidades)
          ===================== */}
      <section>
        <h2 className="section-title">📡 Datos desde REST API</h2>
      </section>
      {/* 1) Reportes (REST) */}
      <section>
        <h3 className="section-title">
          � Reportes desde REST ({reportsREST.length})
        </h3>
        {reportsREST.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay reportes disponibles</p>
        )}
        {reportsREST.map((report) => (
          <div key={`rest-${report.id}`} className="report-card">
            <h3 className="report-title">{report.title}</h3>
            <p className="report-description">{report.description}</p>
            <div className="report-meta">
              <span className={`status-badge status-${toSlug((report as any)?.status, 'abierto')}`}>
                {safeText((report as any)?.status, 'abierto')}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
              {report.location && <span>📍 {report.location}</span>}
            </div>
            {/* 🆕 Botón para descargar PDF del reporte */}
            <button 
              onClick={() => downloadReportPDF(report.id)}
              style={{ 
                marginTop: '1rem',
                padding: '0.5rem 1rem',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '0.9rem'
              }}
            >
              📄 Descargar Reporte PDF
            </button>
          </div>
        ))}
      </section>

      {/* 2) Categorías (REST) */}
      <section>
        <h3 className="section-title">🏷️ Categorías desde REST ({categoriesREST.length})</h3>
        {categoriesREST.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay categorías</p>
        )}
        {categoriesREST.map((c) => (
          <div key={`rest-cat-${c.id}`} className="report-card">
            <h3 className="report-title">{c.name}</h3>
            <p className="report-description">{c.description}</p>
            <div className="report-meta">
              {c.priority && <span>Prioridad: {c.priority}</span>}
              {c.status && <span>Estado: {c.status}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 3) Áreas (REST) */}
      <section>
        <h3 className="section-title">🧭 Áreas desde REST ({areasREST.length})</h3>
        {areasREST.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay áreas</p>
        )}
        {areasREST.map((a) => (
          <div key={`rest-area-${a.id}`} className="report-card">
            <h3 className="report-title">{a.name}</h3>
            <p className="report-description">{a.description}</p>
            <div className="report-meta">
              {a.location && <span>📍 {a.location}</span>}
              {a.responsable && <span>Resp.: {a.responsable}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 4) Estados (REST) */}
      <section>
        <h3 className="section-title">📊 Estados desde REST ({statesREST.length})</h3>
        {statesREST.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay estados</p>
        )}
        {statesREST.map((s) => (
          <div key={`rest-state-${s.id}`} className="report-card">
            <h3 className="report-title">{s.name}</h3>
            <p className="report-description">{s.description}</p>
            <div className="report-meta">
              {s.color && <span style={{ color: s.color }}>●</span>}
              {typeof s.order === 'number' && <span>Orden: {s.order}</span>}
              {typeof s.final === 'boolean' && <span>Final: {s.final ? 'Sí' : 'No'}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 5) Usuarios (REST) */}
      <section>
        <h3 className="section-title">� Usuarios desde REST ({usersREST.length})</h3>
        {usersREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay usuarios</p>}
        {usersREST.map(u => (
          <div key={`rest-user-${u.id}`} className="report-card">
            <h3 className="report-title">{u.name}</h3>
            <div className="report-meta"><span>{u.email}</span> {u.status && <span>Estado: {u.status}</span>}</div>
          </div>
        ))}
      </section>
      {/* 6) Roles (REST) */}
      <section>
        <h3 className="section-title">🛡️ Roles desde REST ({rolesREST.length})</h3>
        {rolesREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay roles</p>}
        {rolesREST.map(r => (
          <div key={`rest-role-${r.id}`} className="report-card">
            <h3 className="report-title">{r.name}</h3>
            <p className="report-description">{r.description}</p>
          </div>
        ))}
      </section>
      {/* 7) Comentarios (REST) */}
      <section>
        <h3 className="section-title">💬 Comentarios desde REST ({commentsREST.length})</h3>
        {commentsREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay comentarios</p>}
        {commentsREST.map(c => (
          <div key={`rest-comment-${c.id}`} className="report-card">
            <h3 className="report-title">#{c.id} en reporte {c.report_id}</h3>
            <p className="report-description">{c.content}</p>
          </div>
        ))}
      </section>
      {/* 8) Puntuaciones (REST) */}
      <section>
        <h3 className="section-title">⭐ Puntuaciones desde REST ({ratingsREST.length})</h3>
        {ratingsREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay puntuaciones</p>}
        {ratingsREST.map(p => (
          <div key={`rest-rating-${p.id}`} className="report-card">
            <h3 className="report-title">Reporte {p.report_id}</h3>
            <div className="report-meta"><span>Valor: {p.value}</span></div>
          </div>
        ))}
      </section>
      {/* 9) Archivos (REST) */}
      <section>
        <h3 className="section-title">� Archivos desde REST ({filesREST.length})</h3>
        {filesREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay archivos</p>}
        {filesREST.map(f => (
          <div key={`rest-file-${f.id}`} className="report-card">
            <h3 className="report-title">{f.name}</h3>
            <div className="report-meta"><a href={f.url} target="_blank" rel="noreferrer">Abrir</a></div>
          </div>
        ))}
      </section>
      {/* 10) Etiquetas (REST) */}
      <section>
        <h3 className="section-title">🏷️ Etiquetas desde REST ({tagsREST.length})</h3>
        {tagsREST.length === 0 && !loading && <p style={{ color: '#999' }}>No hay etiquetas</p>}
        {tagsREST.map(t => (
          <div key={`rest-tag-${t.id}`} className="report-card">
            <h3 className="report-title">{t.name}</h3>
            <div className="report-meta">{t.color && <span style={{ color: t.color }}>●</span>}</div>
          </div>
        ))}
      </section>

      {/* =====================
           BLOQUE: GraphQL
          (10 entidades)
          ===================== */}
      <section>
        <h2 className="section-title">� Datos desde GraphQL</h2>
      </section>
      {/* KPIs desde GraphQL (reportsAnalytics) */}
      <section>
        <h3 className="section-title">📈 Estadísticas (GraphQL → reportsAnalytics)</h3>
        <div className="report-card">
          <div className="report-meta" style={{ gap: '1rem', display: 'flex', flexWrap: 'wrap' }}>
            <span><strong>Total reportes:</strong> {analyticsTotal}</span>
            {analyticsByStatus?.map(k => (
              <span key={`kpi-${String((k as any)?.clave ?? 'unknown')}`} className={`status-badge status-${toSlug((k as any)?.clave, 'otro')}`}>
                {safeText((k as any)?.clave, 'Otro')}: {k.valor}
              </span>
            ))}
          </div>
        </div>
      </section>
      {/* 1) Reportes (GraphQL) */}
      <section>
        <h3 className="section-title">
          📄 Reportes desde GraphQL ({reportsGraphQL.length})
        </h3>
        {reportsGraphQL.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay reportes disponibles</p>
        )}
        {reportsGraphQL.map((report) => (
          <div key={`graphql-${report.id}`} className="report-card">
            <h3 className="report-title">{report.title}</h3>
            <p className="report-description">{report.description}</p>
            <div className="report-meta">
              <span className={`status-badge status-${toSlug((report as any)?.status, 'abierto')}`}>
                {safeText((report as any)?.status, 'N/A')}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
            </div>
            {/* 🆕 Botón para descargar PDF del reporte */}
            <button 
              onClick={() => downloadReportPDF(report.id)}
              style={{ 
                marginTop: '1rem',
                padding: '0.5rem 1rem',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: 'bold',
                fontSize: '0.9rem'
              }}
            >
              📄 Descargar Reporte PDF
            </button>
          </div>
        ))}
      </section>

      {/* 2) Categorías (GraphQL) */}
      <section>
        <h3 className="section-title">🏷️ Categorías desde GraphQL ({categoriesGraphQL.length})</h3>
        {categoriesGraphQL.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay categorías</p>
        )}
        {categoriesGraphQL.map((c) => (
          <div key={`gql-cat-${c.id}`} className="report-card">
            <h3 className="report-title">{c.name}</h3>
            <p className="report-description">{c.description}</p>
            <div className="report-meta">
              {c.priority && <span>Prioridad: {c.priority}</span>}
              {c.status && <span>Estado: {c.status}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 3) Áreas (GraphQL) */}
      <section>
        <h3 className="section-title">🧭 Áreas desde GraphQL ({areasGraphQL.length})</h3>
        {areasGraphQL.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay áreas</p>
        )}
        {areasGraphQL.map((a) => (
          <div key={`gql-area-${a.id}`} className="report-card">
            <h3 className="report-title">{a.name}</h3>
            <p className="report-description">{a.description}</p>
            <div className="report-meta">
              {a.location && <span>📍 {a.location}</span>}
              {a.responsable && <span>Resp.: {a.responsable}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 4) Estados (GraphQL) */}
      <section>
        <h3 className="section-title">📊 Estados desde GraphQL ({statesGraphQL.length})</h3>
        {statesGraphQL.length === 0 && !loading && (
          <p style={{ color: '#999' }}>No hay estados</p>
        )}
        {statesGraphQL.map((s) => (
          <div key={`gql-state-${s.id}`} className="report-card">
            <h3 className="report-title">{s.name}</h3>
            <p className="report-description">{s.description}</p>
            <div className="report-meta">
              {s.color && <span style={{ color: s.color }}>●</span>}
              {typeof s.order === 'number' && <span>Orden: {s.order}</span>}
              {typeof s.final === 'boolean' && <span>Final: {s.final ? 'Sí' : 'No'}</span>}
            </div>
          </div>
        ))}
      </section>

      {/* 5) Usuarios (GraphQL) */}
      <section>
        <h3 className="section-title">👤 Usuarios desde GraphQL ({usersGraphQL.length})</h3>
        {usersGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay usuarios</p>}
        {usersGraphQL.map(u => (
          <div key={`gql-user-${u.id}`} className="report-card">
            <h3 className="report-title">{u.name}</h3>
            <div className="report-meta"><span>{u.email}</span> {u.status && <span>Estado: {u.status}</span>}</div>
          </div>
        ))}
      </section>
      {/* 6) Roles (GraphQL) */}
      <section>
        <h3 className="section-title">🛡️ Roles desde GraphQL ({rolesGraphQL.length})</h3>
        {rolesGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay roles</p>}
        {rolesGraphQL.map(r => (
          <div key={`gql-role-${r.id}`} className="report-card">
            <h3 className="report-title">{r.name}</h3>
            <p className="report-description">{r.description}</p>
          </div>
        ))}
      </section>
      {/* 7) Comentarios (GraphQL) */}
      <section>
        <h3 className="section-title">💬 Comentarios desde GraphQL ({commentsGraphQL.length})</h3>
        {commentsGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay comentarios</p>}
        {commentsGraphQL.map(c => (
          <div key={`gql-comment-${c.id}`} className="report-card">
            <h3 className="report-title">#{c.id} en reporte {c.report_id}</h3>
            <p className="report-description">{c.content}</p>
          </div>
        ))}
      </section>
      {/* 8) Puntuaciones (GraphQL) */}
      <section>
        <h3 className="section-title">⭐ Puntuaciones desde GraphQL ({ratingsGraphQL.length})</h3>
        {ratingsGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay puntuaciones</p>}
        {ratingsGraphQL.map(p => (
          <div key={`gql-rating-${p.id}`} className="report-card">
            <h3 className="report-title">Reporte {p.report_id}</h3>
            <div className="report-meta"><span>Valor: {p.value}</span></div>
          </div>
        ))}
      </section>
      {/* 9) Archivos (GraphQL) */}
      <section>
        <h3 className="section-title">📎 Archivos desde GraphQL ({filesGraphQL.length})</h3>
        {filesGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay archivos</p>}
        {filesGraphQL.map(f => (
          <div key={`gql-file-${f.id}`} className="report-card">
            <h3 className="report-title">{f.name}</h3>
            <div className="report-meta"><a href={f.url} target="_blank" rel="noreferrer">Abrir</a></div>
          </div>
        ))}
      </section>
      {/* 10) Etiquetas (GraphQL) */}
      <section>
        <h3 className="section-title">🏷️ Etiquetas desde GraphQL ({tagsGraphQL.length})</h3>
        {tagsGraphQL.length === 0 && !loading && <p style={{ color: '#999' }}>No hay etiquetas</p>}
        {tagsGraphQL.map(t => (
          <div key={`gql-tag-${t.id}`} className="report-card">
            <h3 className="report-title">{t.name}</h3>
            <div className="report-meta">{t.color && <span style={{ color: t.color }}>●</span>}</div>
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
