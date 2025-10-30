/**
 * Resolvers y Schema para Archivos Adjuntos
 * Módulo 2: Reportes de Infraestructura
 */
import { restAPI } from "../datasources/rest.js";

export const typeDefsArchivosAdjuntos = `#graphql
  type ArchivoAdjunto {
    id: ID!
    report_id: Int!
    name: String!
    type: String
    url: String!
  }

  extend type Query {
    archivosAdjuntos: [ArchivoAdjunto!]!
    archivoAdjunto(id: ID!): ArchivoAdjunto
    archivosByReporte(report_id: Int!): [ArchivoAdjunto!]!

    "Alias en inglés para compatibilidad con el frontend"
    files: [ArchivoAdjunto!]!
  }
`;

export const resolversArchivosAdjuntos = {
  Query: {
    archivosAdjuntos: async () => {
      try {
        return await restAPI.getFiles();
      } catch (error) {
        console.error("Error fetching archivos adjuntos:", error);
        return [];
      }
    },
    archivoAdjunto: async (_: unknown, { id }: { id: string }) => {
      try {
        const files = await restAPI.getFiles();
        return files.find((f: any) => String(f.id) === id) || null;
      } catch (error) {
        console.error("Error fetching archivo adjunto:", error);
        return null;
      }
    },
    archivosByReporte: async (_: unknown, { report_id }: { report_id: number }) => {
      try {
        const files = await restAPI.getFiles();
        return files.filter((f: any) => f.report_id === report_id);
      } catch (error) {
        console.error("Error filtering archivos by reporte:", error);
        return [];
      }
    },

    // Alias en inglés
    files: async () => {
      try {
        return await restAPI.getFiles();
      } catch (error) {
        console.error("Error fetching files:", error);
        return [];
      }
    },
  },
};
