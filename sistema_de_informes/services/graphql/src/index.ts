/**
 * Servidor GraphQL Principal - Semana 6
 * Integra todos los resolvers modulares (10 entidades + analytics + export)
 * ✅ SOLO CONSULTAS (Query) - SIN MUTATIONS según requisito del docente
 */

import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import { typeDefs } from "./schema.js";

// Importar todos los resolvers modulares
import { resolversUsuarios } from "./resolvers/usuarios.js";
import { resolversRoles } from "./resolvers/roles.js";
import { resolversCategorias } from "./resolvers/categorias.js";
import { resolversAreas } from "./resolvers/areas.js";
import { resolversEstados } from "./resolvers/estados.js";
import { resolversComentarios } from "./resolvers/comentarios.js";
import { resolversPuntuaciones } from "./resolvers/puntuaciones.js";
import { resolversArchivosAdjuntos } from "./resolvers/archivosAdjuntos.js";
import { resolversEtiquetas } from "./resolvers/etiquetas.js";
import { resolversReportes } from "./resolvers/reportes.js";
import { resolversAnalytics } from "./resolvers/analytics.js";
import { resolversExport } from "./resolvers/export.js";

// Combinar todos los resolvers en un objeto unificado
const resolvers = {
  Query: {
    ...resolversUsuarios.Query,
    ...resolversRoles.Query,
    ...resolversCategorias.Query,
    ...resolversAreas.Query,
    ...resolversEstados.Query,
    ...resolversComentarios.Query,
    ...resolversPuntuaciones.Query,
    ...resolversArchivosAdjuntos.Query,
    ...resolversEtiquetas.Query,
    ...resolversReportes.Query,
    ...resolversAnalytics.Query,
    ...resolversExport.Query,
  },
};

// Iniciar servidor Apollo GraphQL
async function bootstrap() {
  const server = new ApolloServer({ typeDefs, resolvers });
  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
  });
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║  🚀 Servidor GraphQL Modular - Sistema de Informes          ║
║  📦 10 Entidades + 10 Queries Analíticas + Export PDF        ║
║  🌐 ${url}                                      ║
║  📚 GraphQL Playground: ${url}                  ║
╚══════════════════════════════════════════════════════════════╝
  `);
}

bootstrap().catch((err) => {
  console.error("❌ Error iniciando GraphQL:", err);
  process.exit(1);
});
