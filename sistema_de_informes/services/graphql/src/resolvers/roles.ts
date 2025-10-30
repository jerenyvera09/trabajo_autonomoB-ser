/**
 * Resolvers y Schema para Roles
 * Módulo 1: Autenticación y Usuarios
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsRoles = `#graphql
  type Rol {
    id: ID!
    name: String!
    description: String
    permissions: String
  }

  extend type Query {
    roles: [Rol!]!
    rol(id: ID!): Rol
  }
`;

export const resolversRoles = {
  Query: {
    roles: async () => {
      try {
        return await restAPI.getRoles();
      } catch (error) {
        console.error("Error fetching roles:", error);
        return [];
      }
    },
    rol: async (_: unknown, { id }: { id: string }) => {
      try {
        const roles = await restAPI.getRoles();
        return roles.find((r: any) => String(r.id) === id) || null;
      } catch (error) {
        console.error("Error fetching rol:", error);
        return null;
      }
    },
  },
};
