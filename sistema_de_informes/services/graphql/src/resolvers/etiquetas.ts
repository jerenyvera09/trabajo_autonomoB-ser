/**
 * Resolvers y Schema para Etiquetas
 * Módulo 3: Interacción
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsEtiquetas = `#graphql
  type Etiqueta {
    id: ID!
    name: String!
    color: String
  }

  extend type Query {
    etiquetas: [Etiqueta!]!
    etiqueta(id: ID!): Etiqueta

    "Alias en inglés para compatibilidad con el frontend"
    tags: [Etiqueta!]!
  }
`;

export const resolversEtiquetas = {
  Query: {
    etiquetas: async () => {
      try {
        return await restAPI.getTags();
      } catch (error) {
        console.error("Error fetching etiquetas:", error);
        return [];
      }
    },
    etiqueta: async (_: unknown, { id }: { id: string }) => {
      try {
        const tags = await restAPI.getTags();
        return tags.find((t: any) => String(t.id) === id) || null;
      } catch (error) {
        console.error("Error fetching etiqueta:", error);
        return null;
      }
    },

    // Alias en inglés
    tags: async () => {
      try {
        return await restAPI.getTags();
      } catch (error) {
        console.error("Error fetching tags:", error);
        return [];
      }
    },
  },
};
