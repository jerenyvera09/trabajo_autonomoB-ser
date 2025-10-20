// Esquema inicial centrado en Reportes para pruebas de Semana 4
// Semana 5: Se añade tipo Report compatible con REST API
export const typeDefs = `
  type Reporte {
    id: ID!
    titulo: String!
    descripcion: String
    estado: String!
    categoria: String
    creadoEn: String!
  }

  type Report {
    id: ID!
    title: String!
    description: String!
    status: String
    priority: String
    location: String
    created_at: String
  }

  enum ReporteSortBy {
    titulo
    creadoEn
  }

  enum SortDir {
    ASC
    DESC
  }

  type Kpi {
    clave: String!
    valor: Int!
  }

  type ResumenReportes {
    total: Int!
    porEstado: [Kpi!]!
    porCategoria: [Kpi!]!
  }

  type Query {
    # Listar reportes (mock en Semana 4) con filtros, orden y paginación
    reportes(
      estado: String
      categoria: String
      search: String
      sortBy: ReporteSortBy = creadoEn
      sortDir: SortDir = DESC
      limit: Int = 20
      offset: Int = 0
    ): [Reporte!]!
    # Obtener un reporte por ID
    reporte(id: ID!): Reporte
    # Ping de salud del servicio
    health: String!
    # Resumen/KPIs para capa de reportes
    resumenReportes: ResumenReportes!
    # Semana 5: Query que consume REST API
    reports: [Report!]!
  }

  input CrearReporteInput {
    titulo: String!
    descripcion: String
    categoria: String
  }

  type Mutation {
    # Crear un reporte (mock en Semana 4)
    crearReporte(input: CrearReporteInput!): Reporte!
  }
`;