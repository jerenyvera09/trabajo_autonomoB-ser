/**
 * Resolvers y Schema para Categorías
 * Módulo 2: Reportes de Infraestructura
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsCategorias = `#graphql
  type Categoria {
    id: ID!
    name: String!
    description: String
    priority: String
    status: String
  }

  extend type Query {
    categorias: [Categoria!]!
    categoria(id: ID!): Categoria
    categoriasByPriority(priority: String!): [Categoria!]!

    "Alias en inglés para compatibilidad con el frontend"
    categories: [Categoria!]!
  }
`;

export const resolversCategorias = {
  Query: {
    categorias: async () => {
      try {
        return await restAPI.getCategories();
      } catch (error) {
        console.error("Error fetching categorias:", error);
        return [];
      }
    },
    categoria: async (_: unknown, { id }: { id: string }) => {
      try {
        const cats = await restAPI.getCategories();
        return cats.find((c: any) => String(c.id) === id) || null;
      } catch (error) {
        console.error("Error fetching categoria:", error);
        return null;
      }
    },
    categoriasByPriority: async (_: unknown, { priority }: { priority: string }) => {
      try {
        const cats = await restAPI.getCategories();
        return cats.filter((c: any) => c.priority === priority);
      } catch (error) {
        console.error("Error filtering categorias by priority:", error);
        return [];
      }
    },

    // Alias en inglés
    categories: async () => {
      try {
        return await restAPI.getCategories();
      } catch (error) {
        console.error("Error fetching categories:", error);
        return [];
      }
    },
  },
};
