import { useEffect, useState, useRef } from 'react'
import './App.css'

// Configuración de URLs desde variables de entorno
const API_REST = import.meta.env.VITE_API_REST || 'http://localhost:8000'
// Por defecto apuntamos a la raíz. Si el servidor usa "/graphql",
// más abajo hacemos un intento de respaldo (fallback) automático.
const API_GRAPHQL = import.meta.env.VITE_API_GRAPHQL || 'http://localhost:4000'
// Importante: por defecto nos suscribimos a la sala 'reports' para que coincida con WS_NOTIFY_URL=/notify/reports
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8080/ws?room=reports'

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
  // KPIs (GraphQL → reportsAnalytics)
  const [analyticsTotal, setAnalyticsTotal] = useState<number>(0)
  const [analyticsByStatus, setAnalyticsByStatus] = useState<Array<{ clave: string; valor: number }>>([])

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
              <span className={`status-badge status-${report.status.toLowerCase().replace(' ', '-')}`}>
                {report.status}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
              {report.location && <span>📍 {report.location}</span>}
            </div>
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
              <span key={`kpi-${k.clave}`} className={`status-badge status-${k.clave.toLowerCase().replace(/\s+/g,'-')}`}>
                {k.clave}: {k.valor}
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
              <span className={`status-badge status-${report.status?.toLowerCase().replace(' ', '-') || 'abierto'}`}>
                {report.status || 'N/A'}
              </span>
              {report.priority && <span>Prioridad: {report.priority}</span>}
            </div>
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
