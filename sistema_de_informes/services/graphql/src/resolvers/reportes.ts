/**
 * Resolvers y Schema para Reportes (entidad principal)
 * Consulta datos del REST API
 * Módulo 2: Reportes
 * Semana 6
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsReportes = `#graphql
  type Report {
    id: ID!
    title: String!
    description: String
    location: String
    status: String!
    priority: String
    category_id: Int
    user_id: Int
    created_at: String
    updated_at: String
  }

  "Conexión de reportes para compatibilidad con el frontend (items + total)"
  type ReportConnection {
    items: [Report!]!
    total: Int!
    limit: Int
    offset: Int
  }

  extend type Query {
    "Lista todos los reportes"
    reportes: [Report!]!
    
    "Busca un reporte por ID"
    reporte(id: ID!): Report
    
    "Filtra reportes por estado"
    reportesByStatus(status: String!): [Report!]!
    
    "Filtra reportes por prioridad"
    reportesByPriority(priority: String!): [Report!]!

    "Alias en inglés para compatibilidad con el frontend (ReportConnection)"
    reports: ReportConnection!
  }
`;

export const resolversReportes = {
  Query: {
    reportes: async () => {
      try {
        return await restAPI.getReports();
      } catch (error) {
        console.error("Error obteniendo reportes:", error);
        return [];
      }
    },
    
    reporte: async (_: unknown, { id }: { id: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.find((r: any) => String(r.id) === id) || null;
      } catch (error) {
        console.error("Error obteniendo reporte por ID:", error);
        return null;
      }
    },
    
    reportesByStatus: async (_: unknown, { status }: { status: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.filter((r: any) => r.status?.toLowerCase() === status.toLowerCase());
      } catch (error) {
        console.error("Error filtrando reportes por status:", error);
        return [];
      }
    },
    
    reportesByPriority: async (_: unknown, { priority }: { priority: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.filter((r: any) => r.priority?.toLowerCase() === priority.toLowerCase());
      } catch (error) {
        console.error("Error filtrando reportes por priority:", error);
        return [];
      }
    },

    // Alias 'reports' devolviendo un objeto tipo conexión
    reports: async () => {
      try {
        const items = await restAPI.getReports();
        return {
          items,
          total: Array.isArray(items) ? items.length : 0,
          limit: Array.isArray(items) ? items.length : 0,
          offset: 0,
        };
      } catch (error) {
        console.error("Error en Query.reports:", error);
        return { items: [], total: 0, limit: 0, offset: 0 };
      }
    },
  },
};
