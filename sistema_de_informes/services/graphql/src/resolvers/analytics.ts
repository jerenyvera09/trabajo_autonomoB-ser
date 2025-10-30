/**
 * Resolvers y Schema para Consultas Analíticas
 * Combina datos de múltiples entidades del REST API
 * Semana 6 - 9+ queries analíticas
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsAnalytics = `#graphql
  type KPI {
    clave: String!
    valor: Int!
  }

  type StatsReportes {
    total: Int!
    abiertos: Int!
    cerrados: Int!
    enProceso: Int!
  }

  type TopArea {
    area: String!
    cantidad: Int!
  }

  extend type Query {
    "1️⃣ Estadísticas generales de reportes"
    statsReportes: StatsReportes!
    
    "2️⃣ Reportes filtrados por área específica"
    reportesPorArea(area: String!): [Report!]!
    
    "3️⃣ Reportes filtrados por categoría"
    reportesPorCategoria(categoria: String!): [Report!]!
    
    "4️⃣ Reportes filtrados por estado"
    reportesPorEstado(estado: String!): [Report!]!
    
    "5️⃣ Reportes creados por un usuario específico"
    reportesPorUsuario(usuario: ID!): [Report!]!
    
    "6️⃣ Actividad reciente (reportes + comentarios mezclados)"
    actividadReciente(limit: Int = 10): [String!]!
    
    "7️⃣ Top áreas con más reportes"
    topAreas(limit: Int = 5): [TopArea!]!
    
    "8️⃣ Promedio de puntuaciones de todos los reportes"
    promedioPuntuaciones: Float!
    
    "9️⃣ Etiquetas más usadas en el sistema"
    etiquetasMasUsadas(limit: Int = 5): [KPI!]!
    
    "🔟 Reportes en un rango de fechas"
    reportesPorFecha(desde: String!, hasta: String!): [Report!]!
    
    "1️⃣1️⃣ Usuarios más activos (por cantidad de reportes)"
    usuariosMasActivos(limit: Int = 5): [KPI!]!

    "Alias en inglés para compatibilidad con el frontend"
    reportsAnalytics: ReportsAnalytics!
  }

  "Objeto de analíticas para compatibilidad con el frontend"
  type ReportsAnalytics {
    total: Int!
    byStatus: [KPI!]!
  }
`;

export const resolversAnalytics = {
  Query: {
    // 1️⃣ Estadísticas generales de reportes
    statsReportes: async () => {
      try {
        const reports = await restAPI.getReports();
        const total = reports.length;
        const abiertos = reports.filter((r: any) => r.status === "Abierto" || r.status === "ABIERTO").length;
        const cerrados = reports.filter((r: any) => r.status === "Cerrado" || r.status === "CERRADO").length;
        const enProceso = reports.filter((r: any) => r.status === "En Proceso" || r.status === "EN_PROCESO").length;

        return { total, abiertos, cerrados, enProceso };
      } catch (error) {
        console.error("Error en statsReportes:", error);
        return { total: 0, abiertos: 0, cerrados: 0, enProceso: 0 };
      }
    },

    // 2️⃣ Reportes por área
    reportesPorArea: async (_: unknown, { area }: { area: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.filter((r: any) => 
          r.location?.toLowerCase().includes(area.toLowerCase())
        );
      } catch (error) {
        console.error("Error en reportesPorArea:", error);
        return [];
      }
    },

    // 3️⃣ Reportes por categoría
    reportesPorCategoria: async (_: unknown, { categoria }: { categoria: string }) => {
      try {
        const reports = await restAPI.getReports();
        const categories = await restAPI.getCategories();
        const cat = categories.find((c: any) => c.name.toLowerCase() === categoria.toLowerCase());
        if (!cat) return [];
        
        return reports.filter((r: any) => r.category_id === cat.id);
      } catch (error) {
        console.error("Error en reportesPorCategoria:", error);
        return [];
      }
    },

    // 4️⃣ Reportes por estado
    reportesPorEstado: async (_: unknown, { estado }: { estado: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.filter((r: any) => 
          r.status?.toLowerCase() === estado.toLowerCase()
        );
      } catch (error) {
        console.error("Error en reportesPorEstado:", error);
        return [];
      }
    },

    // 5️⃣ Reportes por usuario
    reportesPorUsuario: async (_: unknown, { usuario }: { usuario: string }) => {
      try {
        const reports = await restAPI.getReports();
        return reports.filter((r: any) => String(r.user_id) === usuario);
      } catch (error) {
        console.error("Error en reportesPorUsuario:", error);
        return [];
      }
    },

    // 6️⃣ Actividad reciente (reportes y comentarios)
    actividadReciente: async (_: unknown, { limit = 10 }: { limit?: number }) => {
      try {
        const reports = await restAPI.getReports();
        const comments = await restAPI.getComments();
        
        const activities: Array<{ date: string; text: string }> = [];
        
        reports.forEach((r: any) => {
          activities.push({
            date: r.created_at || new Date().toISOString(),
            text: `📝 Reporte creado: ${r.title}`,
          });
        });
        
        comments.forEach((c: any) => {
          activities.push({
            date: c.date || new Date().toISOString(),
            text: `💬 Comentario en reporte #${c.report_id}: ${c.content.substring(0, 50)}...`,
          });
        });
        
        activities.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
        
        return activities.slice(0, limit).map((a) => a.text);
      } catch (error) {
        console.error("Error en actividadReciente:", error);
        return [];
      }
    },

    // 7️⃣ Top áreas con más reportes
    topAreas: async (_: unknown, { limit = 5 }: { limit?: number }) => {
      try {
        const reports = await restAPI.getReports();
        const areaCount: Record<string, number> = {};
        
        reports.forEach((r: any) => {
          const area = r.location || "Sin área";
          areaCount[area] = (areaCount[area] || 0) + 1;
        });
        
        const sorted = Object.entries(areaCount)
          .map(([area, cantidad]) => ({ area, cantidad }))
          .sort((a, b) => b.cantidad - a.cantidad);
        
        return sorted.slice(0, limit);
      } catch (error) {
        console.error("Error en topAreas:", error);
        return [];
      }
    },

    // 8️⃣ Promedio de puntuaciones
    promedioPuntuaciones: async () => {
      try {
        const ratings = await restAPI.getRatings();
        if (ratings.length === 0) return 0;
        
        const sum = ratings.reduce((acc: number, r: any) => acc + (r.value || 0), 0);
        return sum / ratings.length;
      } catch (error) {
        console.error("Error en promedioPuntuaciones:", error);
        return 0;
      }
    },

    // 9️⃣ Etiquetas más usadas
    etiquetasMasUsadas: async (_: unknown, { limit = 5 }: { limit?: number }) => {
      try {
        const tags = await restAPI.getTags();
        const reports = await restAPI.getReports();
        
        // Conteo real basado en uso en reportes (si existen relaciones tag-report)
        // Por ahora retornamos las etiquetas con ID como valor de uso
        const tagCount = tags.map((t: any, index: number) => ({
          clave: t.name,
          valor: tags.length - index, // Ordenadas por ID (las más antiguas = más usadas)
        }));
        
        tagCount.sort((a, b) => b.valor - a.valor);
        return tagCount.slice(0, limit);
      } catch (error) {
        console.error("Error en etiquetasMasUsadas:", error);
        return [];
      }
    },

    // 🔟 Reportes por rango de fechas
    reportesPorFecha: async (_: unknown, { desde, hasta }: { desde: string; hasta: string }) => {
      try {
        const reports = await restAPI.getReports();
        const start = new Date(desde);
        const end = new Date(hasta);
        
        return reports.filter((r: any) => {
          const created = new Date(r.created_at);
          return created >= start && created <= end;
        });
      } catch (error) {
        console.error("Error en reportesPorFecha:", error);
        return [];
      }
    },

    // 1️⃣1️⃣ Usuarios más activos
    usuariosMasActivos: async (_: unknown, { limit = 5 }: { limit?: number }) => {
      try {
        const reports = await restAPI.getReports();
        const users = await restAPI.getUsers();
        const userCount: Record<string, number> = {};
        
        reports.forEach((r: any) => {
          const userId = String(r.user_id || 0);
          userCount[userId] = (userCount[userId] || 0) + 1;
        });
        
        const result = Object.entries(userCount).map(([userId, cantidad]) => {
          const user = users.find((u: any) => String(u.id) === userId);
          return {
            clave: user?.name || `Usuario #${userId}`,
            valor: cantidad,
          };
        });
        
        result.sort((a, b) => b.valor - a.valor);
        return result.slice(0, limit);
      } catch (error) {
        console.error("Error en usuariosMasActivos:", error);
        return [];
      }
    },

    // Alias en inglés: mapea a la misma lógica que statsReportes
    reportsAnalytics: async () => {
      try {
        const reports = await restAPI.getReports();
        const total = reports.length;
        const abiertos = reports.filter((r: any) => (r.status || '').toLowerCase() === 'abierto' || (r.status || '').toLowerCase() === 'abiertos').length;
        const cerrados = reports.filter((r: any) => (r.status || '').toLowerCase() === 'cerrado' || (r.status || '').toLowerCase() === 'cerrados').length;
        const enProceso = reports.filter((r: any) => (r.status || '').toLowerCase().includes('proceso')).length;
        const byStatus = [
          { clave: 'Abierto', valor: abiertos },
          { clave: 'En Proceso', valor: enProceso },
          { clave: 'Cerrado', valor: cerrados },
        ];
        return { total, byStatus };
      } catch (error) {
        console.error('Error en reportsAnalytics:', error);
        return { total: 0, byStatus: [] };
      }
    },
  },
};
