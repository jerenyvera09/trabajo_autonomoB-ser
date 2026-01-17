/**
 * Servidor GraphQL Principal - Semana 6
 * Integra todos los resolvers modulares (10 entidades + analytics + export)
 * ✅ SOLO CONSULTAS (Query) - SIN MUTATIONS según requisito del docente
 */

import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import { GraphQLError } from "graphql";
import jwt from "jsonwebtoken";
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

const JWT_SECRET = process.env.JWT_SECRET || "please-change-this-secret";
const JWT_ALG = process.env.JWT_ALG || "HS256";
const AUTH_SERVICE_URL = (process.env.AUTH_SERVICE_URL || "http://auth-service:8001").replace(/\/$/, "");
const GRAPHQL_REQUIRE_AUTH = process.env.GRAPHQL_REQUIRE_AUTH === "1";
const REVOKED_SYNC_SECONDS = Number(process.env.REVOKED_SYNC_SECONDS || "30");

let revokedJTIs = new Set<string>();

async function syncRevokedOnce() {
  try {
    const res = await fetch(`${AUTH_SERVICE_URL}/auth/revoked`);
    if (!res.ok) return;
    const data: any = await res.json().catch(() => null);
    const jtis = Array.isArray(data?.jtis) ? data.jtis.filter((x: any) => typeof x === "string") : [];
    revokedJTIs = new Set(jtis);
  } catch {
    // silent
  }
}

function startRevokedSync() {
  void syncRevokedOnce();
  const every = Math.max(5, Number.isFinite(REVOKED_SYNC_SECONDS) ? REVOKED_SYNC_SECONDS : 30);
  setInterval(() => void syncRevokedOnce(), every * 1000).unref?.();
}

function verifyBearerOrThrow(req: any) {
  const auth = req?.headers?.authorization || req?.headers?.Authorization;
  const raw = typeof auth === "string" ? auth : "";
  if (!raw.toLowerCase().startsWith("bearer ")) {
    throw new GraphQLError("Unauthorized", { extensions: { code: "UNAUTHENTICATED" } });
  }
  const token = raw.split(" ", 2)[1];
  try {
    const decoded: any = jwt.verify(token, JWT_SECRET, { algorithms: [JWT_ALG] });
    const jti = typeof decoded?.jti === "string" ? decoded.jti : "";
    if (jti && revokedJTIs.has(jti)) {
      throw new GraphQLError("Token revocado", { extensions: { code: "UNAUTHENTICATED" } });
    }
    return decoded;
  } catch (e: any) {
    if (e instanceof GraphQLError) throw e;
    throw new GraphQLError("Token inválido", { extensions: { code: "UNAUTHENTICATED" } });
  }
}

// Iniciar servidor Apollo GraphQL
async function bootstrap() {
  const server = new ApolloServer({ typeDefs, resolvers });
  startRevokedSync();
  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
    context: async ({ req }) => {
      // Pilar 1: validación local (firma/exp) + blacklist sincronizada, sin llamar al auth-service por request.
      if (GRAPHQL_REQUIRE_AUTH) {
        const claims = verifyBearerOrThrow(req);
        return { claims };
      }
      // Si no es obligatorio, igual validamos si viene token (para no aceptar tokens rotos)
      const auth = req?.headers?.authorization || req?.headers?.Authorization;
      if (typeof auth === "string" && auth.toLowerCase().startsWith("bearer ")) {
        const claims = verifyBearerOrThrow(req);
        return { claims };
      }
      return { claims: null };
    },
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
