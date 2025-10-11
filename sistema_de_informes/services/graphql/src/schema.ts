// Esquema inicial centrado en Reportes para pruebas de Semana 4
export const typeDefs = `
  type Reporte {
    id: ID!
    titulo: String!
    descripcion: String
    estado: String!
    categoria: String
    creadoEn: String!
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
