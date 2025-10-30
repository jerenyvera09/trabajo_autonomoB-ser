/**
 * Resolvers y Schema para Estados de Reporte
 * Módulo 2: Reportes de Infraestructura
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsEstados = `#graphql
  type EstadoReporte {
    id: ID!
    name: String!
    description: String
    color: String
    order: Int
    final: Boolean
  }

  extend type Query {
    estados: [EstadoReporte!]!
    estado(id: ID!): EstadoReporte
    estadosFinal: [EstadoReporte!]!

    "Alias en inglés para compatibilidad con el frontend"
    states: [EstadoReporte!]!
  }
`;

export const resolversEstados = {
  Query: {
    estados: async () => {
      try {
        return await restAPI.getStates();
      } catch (error) {
        console.error("Error fetching estados:", error);
        return [];
      }
    },
    estado: async (_: unknown, { id }: { id: string }) => {
      try {
        const states = await restAPI.getStates();
        return states.find((s: any) => String(s.id) === id) || null;
      } catch (error) {
        console.error("Error fetching estado:", error);
        return null;
      }
    },
    estadosFinal: async () => {
      try {
        const states = await restAPI.getStates();
        return states.filter((s: any) => s.final === true);
      } catch (error) {
        console.error("Error filtering estados finales:", error);
        return [];
      }
    },

    // Alias en inglés
    states: async () => {
      try {
        return await restAPI.getStates();
      } catch (error) {
        console.error("Error fetching states:", error);
        return [];
      }
    },
  },
};
