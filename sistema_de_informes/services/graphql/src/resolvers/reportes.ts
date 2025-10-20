// Datos en memoria para la Semana 4 (mock)
const reportes = [
  {
    id: "1",
    titulo: "Fuga de agua en laboratorio",
    descripcion: "Se detecta fuga en el lavadero del laboratorio A2",
    estado: "ABIERTO",
    categoria: "MANTENIMIENTO",
    creadoEn: new Date().toISOString(),
  },
  {
    id: "2",
    titulo: "Falla eléctrica en pasillo",
    descripcion: "Luces intermitentes en pasillo del bloque B",
    estado: "EN_PROCESO",
    categoria: "ELECTRICIDAD",
    creadoEn: new Date().toISOString(),
  },
];

let idCounter = reportes.length + 1;

export const resolvers = {
  Query: {
    reportes: (
      _: unknown,
      args: {
        estado?: string;
        categoria?: string;
        search?: string;
        sortBy?: "titulo" | "creadoEn";
        sortDir?: "ASC" | "DESC";
        limit?: number;
        offset?: number;
      }
    ) => {
      const {
        estado,
        categoria,
        search,
        sortBy = "creadoEn",
        sortDir = "DESC",
        limit = 20,
        offset = 0,
      } = args || {};

      let data = [...reportes];

      if (estado) data = data.filter((r) => r.estado === estado);
      if (categoria) data = data.filter((r) => r.categoria === categoria);
      if (search) {
        const q = search.toLowerCase();
        data = data.filter(
          (r) =>
            r.titulo.toLowerCase().includes(q) ||
            (r.descripcion ?? "").toLowerCase().includes(q)
        );
      }

      data.sort((a, b) => {
        const dir = sortDir === "ASC" ? 1 : -1;
        if (sortBy === "titulo") {
          return a.titulo.localeCompare(b.titulo) * dir;
        }
        // por defecto creadoEn
        return (a.creadoEn.localeCompare(b.creadoEn)) * dir;
      });

      return data.slice(offset, offset + limit);
    },
    reporte: (_: unknown, args: { id: string }) =>
      reportes.find((r) => r.id === args.id) || null,
    health: () => "ok",
    resumenReportes: () => {
      const total = reportes.length;
      const porEstado: Record<string, number> = {};
      const porCategoria: Record<string, number> = {};
      for (const r of reportes) {
        porEstado[r.estado] = (porEstado[r.estado] ?? 0) + 1;
        if (r.categoria)
          porCategoria[r.categoria] = (porCategoria[r.categoria] ?? 0) + 1;
      }
      const mapToKpi = (obj: Record<string, number>) =>
        Object.entries(obj).map(([clave, valor]) => ({ clave, valor }));
      return {
        total,
        porEstado: mapToKpi(porEstado),
        porCategoria: mapToKpi(porCategoria),
      };
    },
    // SEMANA 5: Integración con REST API
    reports: async () => {
      try {
        const response = await fetch("http://localhost:8000/api/v1/reports");
        if (!response.ok) {
          throw new Error(`REST API error: ${response.status}`);
        }
        const data = await response.json();
        return data;
      } catch (error) {
        console.error("Error fetching from REST API:", error);
        // Fallback a datos vacíos si el REST no está disponible
        return [];
      }
    },
  },
  Mutation: {
    crearReporte: (
      _: unknown,
      args: { input: { titulo: string; descripcion?: string; categoria?: string } },
      __context: unknown,
      __info: unknown
    ) => {
      // Validación básica de entrada
      const titulo = (args.input.titulo ?? "").trim();
      if (!titulo || titulo.length < 3) {
        throw new Error("Título requerido (mínimo 3 caracteres)");
      }

      const nuevo = {
        id: String(idCounter++),
        titulo,
        descripcion: args.input.descripcion ?? null,
        estado: "ABIERTO",
        categoria: args.input.categoria ?? null,
        creadoEn: new Date().toISOString(),
      };
      reportes.push(nuevo as any);
      return nuevo;
    },
  },
};