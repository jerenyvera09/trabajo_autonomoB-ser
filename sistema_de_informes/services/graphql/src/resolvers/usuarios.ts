/**
 * Resolvers y Schema para Usuarios
 * Módulo 1: Autenticación y Usuarios
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsUsuarios = `#graphql
  type Usuario {
    id: ID!
    name: String!
    email: String!
    status: String
    role_id: Int
  }

  extend type Query {
    usuarios: [Usuario!]!
    usuario(id: ID!): Usuario
    usuariosByStatus(status: String!): [Usuario!]!

    "Alias en inglés para compatibilidad con el frontend"
    users: [Usuario!]!
  }
`;

export const resolversUsuarios = {
  Query: {
    usuarios: async () => {
      try {
        return await restAPI.getUsers();
      } catch (error) {
        console.error("Error fetching usuarios:", error);
        return [];
      }
    },
    usuario: async (_: unknown, { id }: { id: string }) => {
      try {
        const users = await restAPI.getUsers();
        return users.find((u: any) => String(u.id) === id) || null;
      } catch (error) {
        console.error("Error fetching usuario:", error);
        return null;
      }
    },
    usuariosByStatus: async (_: unknown, { status }: { status: string }) => {
      try {
        const users = await restAPI.getUsers();
        return users.filter((u: any) => u.status === status);
      } catch (error) {
        console.error("Error filtering usuarios by status:", error);
        return [];
      }
    },

    // Alias en inglés
    users: async () => {
      try {
        return await restAPI.getUsers();
      } catch (error) {
        console.error("Error fetching users:", error);
        return [];
      }
    },
  },
};
