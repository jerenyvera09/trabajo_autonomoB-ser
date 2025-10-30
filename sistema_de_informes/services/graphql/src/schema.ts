/**
 * Schema GraphQL Unificado - Semana 6
 * Combina todos los typeDefs de las entidades, analíticas y exportación
 * ✅ SOLO CONSULTAS (Query) - SIN MUTATIONS según requisito del docente
 */

import { typeDefsUsuarios } from "./resolvers/usuarios.js";
import { typeDefsRoles } from "./resolvers/roles.js";
import { typeDefsCategorias } from "./resolvers/categorias.js";
import { typeDefsAreas } from "./resolvers/areas.js";
import { typeDefsEstados } from "./resolvers/estados.js";
import { typeDefsComentarios } from "./resolvers/comentarios.js";
import { typeDefsPuntuaciones } from "./resolvers/puntuaciones.js";
import { typeDefsArchivosAdjuntos } from "./resolvers/archivosAdjuntos.js";
import { typeDefsEtiquetas } from "./resolvers/etiquetas.js";
import { typeDefsReportes } from "./resolvers/reportes.js";
import { typeDefsAnalytics } from "./resolvers/analytics.js";
import { typeDefsExport } from "./resolvers/export.js";

// Base type Query para extender (requerido por Apollo)
const baseTypeDefs = `#graphql
  type Query {
    _empty: String
  }
`;

// Exportar schema unificado modular
export const typeDefs = [
  baseTypeDefs,
  typeDefsUsuarios,
  typeDefsRoles,
  typeDefsCategorias,
  typeDefsAreas,
  typeDefsEstados,
  typeDefsComentarios,
  typeDefsPuntuaciones,
  typeDefsArchivosAdjuntos,
  typeDefsEtiquetas,
  typeDefsReportes,
  typeDefsAnalytics,
  typeDefsExport,
];