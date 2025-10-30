/**
 * Resolvers y Schema para Puntuaciones
 * Módulo 3: Interacción
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsPuntuaciones = `#graphql
  type Puntuacion {
    id: ID!
    report_id: Int!
    user_id: Int!
    value: Int!
    date: String!
  }

  extend type Query {
    puntuaciones: [Puntuacion!]!
    puntuacion(id: ID!): Puntuacion
    puntuacionesByReporte(report_id: Int!): [Puntuacion!]!

    "Alias en inglés para compatibilidad con el frontend"
    ratings: [Puntuacion!]!
  }
`;

export const resolversPuntuaciones = {
  Query: {
    puntuaciones: async () => {
      try {
        return await restAPI.getRatings();
      } catch (error) {
        console.error("Error fetching puntuaciones:", error);
        return [];
      }
    },
    puntuacion: async (_: unknown, { id }: { id: string }) => {
      try {
        const ratings = await restAPI.getRatings();
        return ratings.find((r: any) => String(r.id) === id) || null;
      } catch (error) {
        console.error("Error fetching puntuacion:", error);
        return null;
      }
    },
    puntuacionesByReporte: async (_: unknown, { report_id }: { report_id: number }) => {
      try {
        const ratings = await restAPI.getRatings();
        return ratings.filter((r: any) => r.report_id === report_id);
      } catch (error) {
        console.error("Error filtering puntuaciones by reporte:", error);
        return [];
      }
    },

    // Alias en inglés
    ratings: async () => {
      try {
        return await restAPI.getRatings();
      } catch (error) {
        console.error("Error fetching ratings:", error);
        return [];
      }
    },
  },
};
