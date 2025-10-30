/**
 * Resolvers y Schema para Comentarios
 * Módulo 3: Interacción
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsComentarios = `#graphql
  type Comentario {
    id: ID!
    report_id: Int!
    user_id: Int!
    content: String!
    date: String!
  }

  extend type Query {
    comentarios: [Comentario!]!
    comentario(id: ID!): Comentario
    comentariosByReporte(report_id: Int!): [Comentario!]!
    comentariosByUsuario(user_id: Int!): [Comentario!]!

    "Alias en inglés para compatibilidad con el frontend"
    comments: [Comentario!]!
  }
`;

export const resolversComentarios = {
  Query: {
    comentarios: async () => {
      try {
        return await restAPI.getComments();
      } catch (error) {
        console.error("Error fetching comentarios:", error);
        return [];
      }
    },
    comentario: async (_: unknown, { id }: { id: string }) => {
      try {
        const comments = await restAPI.getComments();
        return comments.find((c: any) => String(c.id) === id) || null;
      } catch (error) {
        console.error("Error fetching comentario:", error);
        return null;
      }
    },
    comentariosByReporte: async (_: unknown, { report_id }: { report_id: number }) => {
      try {
        const comments = await restAPI.getComments();
        return comments.filter((c: any) => c.report_id === report_id);
      } catch (error) {
        console.error("Error filtering comentarios by reporte:", error);
        return [];
      }
    },
    comentariosByUsuario: async (_: unknown, { user_id }: { user_id: number }) => {
      try {
        const comments = await restAPI.getComments();
        return comments.filter((c: any) => c.user_id === user_id);
      } catch (error) {
        console.error("Error filtering comentarios by usuario:", error);
        return [];
      }
    },

    // Alias en inglés
    comments: async () => {
      try {
        return await restAPI.getComments();
      } catch (error) {
        console.error("Error fetching comments:", error);
        return [];
      }
    },
  },
};
