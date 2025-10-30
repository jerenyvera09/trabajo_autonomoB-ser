/**
 * Resolvers y Schema para Áreas
 * Módulo 2: Reportes de Infraestructura
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsAreas = `#graphql
  type Area {
    id: ID!
    name: String!
    location: String
    responsable: String
    description: String
  }

  extend type Query {
    areas: [Area!]!
    area(id: ID!): Area
    areasByResponsable(responsable: String!): [Area!]!
  }
`;

export const resolversAreas = {
  Query: {
    areas: async () => {
      try {
        return await restAPI.getAreas();
      } catch (error) {
        console.error("Error fetching areas:", error);
        return [];
      }
    },
    area: async (_: unknown, { id }: { id: string }) => {
      try {
        const areas = await restAPI.getAreas();
        return areas.find((a: any) => String(a.id) === id) || null;
      } catch (error) {
        console.error("Error fetching area:", error);
        return null;
      }
    },
    areasByResponsable: async (_: unknown, { responsable }: { responsable: string }) => {
      try {
        const areas = await restAPI.getAreas();
        return areas.filter((a: any) => a.responsable === responsable);
      } catch (error) {
        console.error("Error filtering areas by responsable:", error);
        return [];
      }
    },
  },
};
