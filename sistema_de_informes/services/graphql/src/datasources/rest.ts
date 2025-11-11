/**
 * REST API DataSource
 * Cliente fetch para consumir endpoints del servicio REST (FastAPI)
 * Semana 6 - Integración GraphQL ↔ REST
 */

const REST_BASE_URL = process.env.REST_BASE_URL || "http://localhost:8000";
const REST_API_TOKEN = process.env.REST_API_TOKEN || "";

type AnyObject = Record<string, unknown>;

const pick = <T>(...values: Array<T | null | undefined>): T | undefined => {
  for (const value of values) {
    if (value !== undefined && value !== null) {
      return value;
    }
  }
  return undefined;
};

const toNumber = (value: unknown): number | undefined => {
  if (value === undefined || value === null || value === "") return undefined;
  const parsed = Number(value);
  return Number.isNaN(parsed) ? undefined : parsed;
};

const toBoolean = (value: unknown): boolean | undefined => {
  if (value === undefined || value === null) return undefined;
  if (typeof value === "boolean") return value;
  if (typeof value === "number") return value !== 0;
  if (typeof value === "string") {
    const normalized = value.trim().toLowerCase();
    if (["true", "1", "t", "yes", "y"].includes(normalized)) return true;
    if (["false", "0", "f", "no", "n"].includes(normalized)) return false;
  }
  return undefined;
};

const toStringValue = (value: unknown): string | undefined => {
  if (value === undefined || value === null) return undefined;
  if (value instanceof Date) return value.toISOString();
  return String(value);
};

const mapReport = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_reporte, raw.report_id);
  const categoryId = pick(raw.category_id, raw.id_categoria);
  const userId = pick(raw.user_id, raw.id_usuario);
  const areaId = pick(raw.area_id, raw.id_area);
  const stateId = pick(raw.state_id, raw.id_estado);
  const title = toStringValue(pick(raw.title, raw.titulo, raw.name)) ?? "Sin título";
  const status = toStringValue(pick(raw.status, raw.estado, raw.status_name, raw.nombre_estado)) ?? "Sin estado";
  return {
    id: toNumber(id) ?? id ?? null,
    title,
    description: pick(raw.description, raw.descripcion) ?? "",
    location: pick(raw.location, raw.ubicacion) ?? null,
    status,
    priority: pick(raw.priority, raw.prioridad) ?? null,
    category_id: toNumber(categoryId) ?? categoryId ?? null,
    user_id: toNumber(userId) ?? userId ?? null,
    area_id: toNumber(areaId) ?? areaId ?? null,
    state_id: toNumber(stateId) ?? stateId ?? null,
    created_at: toStringValue(pick(raw.created_at, raw.creado_en)),
    updated_at: toStringValue(pick(raw.updated_at, raw.actualizado_en)),
  };
};

const mapCategory = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_categoria);
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre) ?? "",
    description: pick(raw.description, raw.descripcion) ?? null,
    priority: pick(raw.priority, raw.prioridad) ?? null,
    status: pick(raw.status, raw.estado) ?? null,
  };
};

const mapArea = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_area);
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre, raw.nombre_area) ?? "",
    location: pick(raw.location, raw.ubicacion) ?? null,
    responsable: pick(raw.responsable, raw.responsable_area, raw.encargado) ?? null,
    description: pick(raw.description, raw.descripcion) ?? null,
  };
};

const mapState = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_estado);
  const finalValue = toBoolean(pick(raw.final, raw.es_final, raw.esFinal));
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre) ?? "",
    description: pick(raw.description, raw.descripcion) ?? null,
    color: pick(raw.color, raw.color_hex) ?? null,
    order: toNumber(pick(raw.order, raw.orden)) ?? null,
    final: finalValue ?? false,
  };
};

const mapRole = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_rol);
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre, raw.nombre_rol) ?? "",
    description: pick(raw.description, raw.descripcion) ?? null,
    permissions: pick(raw.permissions, raw.permisos) ?? null,
  };
};

const mapUser = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_usuario);
  const roleId = pick(raw.role_id, raw.id_rol);
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre) ?? "",
    email: pick(raw.email, raw.correo) ?? "",
    status: pick(raw.status, raw.estado) ?? null,
    role_id: toNumber(roleId) ?? roleId ?? null,
  };
};

const mapComment = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_comentario);
  const reportId = pick(raw.report_id, raw.id_reporte);
  const userId = pick(raw.user_id, raw.id_usuario);
  const date = toStringValue(pick(raw.date, raw.fecha)) ?? new Date().toISOString();
  return {
    id: toNumber(id) ?? id ?? null,
    report_id: toNumber(reportId) ?? reportId ?? null,
    user_id: toNumber(userId) ?? userId ?? null,
    content: pick(raw.content, raw.contenido) ?? "",
    date,
  };
};

const mapRating = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_puntuacion);
  const reportId = pick(raw.report_id, raw.id_reporte);
  const userId = pick(raw.user_id, raw.id_usuario);
  const date = toStringValue(pick(raw.date, raw.fecha)) ?? new Date().toISOString();
  return {
    id: toNumber(id) ?? id ?? null,
    report_id: toNumber(reportId) ?? reportId ?? null,
    user_id: toNumber(userId) ?? userId ?? null,
    value: toNumber(pick(raw.value, raw.valor)) ?? 0,
    date,
  };
};

const mapFile = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_archivo);
  const reportId = pick(raw.report_id, raw.id_reporte);
  return {
    id: toNumber(id) ?? id ?? null,
    report_id: toNumber(reportId) ?? reportId ?? null,
    name: pick(raw.name, raw.nombre_archivo, raw.filename) ?? "",
    type: pick(raw.type, raw.tipo) ?? null,
    url: pick(raw.url, raw.link, raw.path) ?? "",
  };
};

const mapTag = (raw: AnyObject) => {
  const id = pick(raw.id, raw.id_etiqueta);
  return {
    id: toNumber(id) ?? id ?? null,
    name: pick(raw.name, raw.nombre) ?? "",
    color: pick(raw.color, raw.hex) ?? null,
  };
};

export class RestDataSource {
  private readonly baseURL: string;
  private readonly bearerToken?: string;

  constructor(baseURL: string = REST_BASE_URL) {
    this.baseURL = baseURL;
    this.bearerToken = REST_API_TOKEN || undefined;
  }

  /**
   * GET genérico a cualquier endpoint del REST
   */
  async get<T>(path: string): Promise<T> {
    const url = `${this.baseURL}${path}`;
    try {
      const headers: Record<string, string> = { Accept: "application/json" };
      if (this.bearerToken) headers["Authorization"] = `Bearer ${this.bearerToken}`;
      const response = await fetch(url, { headers });
      if (!response.ok) {
        throw new Error(`REST API error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error(`Error fetching ${url}:`, error);
      throw error;
    }
  }

  /**
   * Intenta obtener desde múltiples rutas en orden y devuelve el primer resultado exitoso.
   * Si todas fallan, retorna [] para colecciones o relanza el último error para objetos.
   */
  private async getWithFallback<T>(paths: string[], emptyOnFail: boolean = true): Promise<T> {
    let lastError: unknown;
    for (const p of paths) {
      try {
        // eslint-disable-next-line no-await-in-loop
        return await this.get<T>(p);
      } catch (e) {
        lastError = e;
      }
    }
    if (emptyOnFail) {
      return [] as unknown as T;
    }
    throw lastError instanceof Error ? lastError : new Error("Unknown REST error");
  }

  /**
   * Endpoints de integración (públicos, sin auth)
   */
  async getReports() {
    const data = await this.getWithFallback<any[]>(["/api/v1/reports", "/reportes"]);
    return Array.isArray(data) ? data.map(mapReport) : [];
  }

  async getCategories() {
    const data = await this.getWithFallback<any[]>(["/api/v1/categories", "/categorias"]);
    return Array.isArray(data) ? data.map(mapCategory) : [];
  }

  async getAreas() {
    const data = await this.getWithFallback<any[]>(["/api/v1/areas", "/areas"]);
    return Array.isArray(data) ? data.map(mapArea) : [];
  }

  async getStates() {
    const data = await this.getWithFallback<any[]>(["/api/v1/states", "/estados-reporte"]);
    return Array.isArray(data) ? data.map(mapState) : [];
  }

  async getRoles() {
    const data = await this.getWithFallback<any[]>(["/api/v1/roles", "/roles"]);
    return Array.isArray(data) ? data.map(mapRole) : [];
  }

  async getUsers() {
    const data = await this.getWithFallback<any[]>(["/api/v1/users", "/usuarios"]);
    return Array.isArray(data) ? data.map(mapUser) : [];
  }

  async getComments() {
    const data = await this.getWithFallback<any[]>(["/api/v1/comments", "/comentarios"]);
    return Array.isArray(data) ? data.map(mapComment) : [];
  }

  async getRatings() {
    const data = await this.getWithFallback<any[]>(["/api/v1/ratings", "/puntuaciones"]);
    return Array.isArray(data) ? data.map(mapRating) : [];
  }

  async getFiles() {
    const data = await this.getWithFallback<any[]>(["/api/v1/files", "/archivos"]);
    return Array.isArray(data) ? data.map(mapFile) : [];
  }

  async getTags() {
    const data = await this.getWithFallback<any[]>(["/api/v1/tags", "/etiquetas"]);
    return Array.isArray(data) ? data.map(mapTag) : [];
  }

  async getAttachments() {
    // Intenta en orden: /attachments, /files, /archivos
    const data = await this.getWithFallback<any[]>([
      "/api/v1/attachments",
      "/api/v1/files",
      "/archivos",
    ]);
    return Array.isArray(data) ? data.map(mapFile) : [];
  }
}

// Instancia singleton
export const restAPI = new RestDataSource();

/**
 * Helper function alternativo para consultas simples GET
 * Uso: const data = await getJSON<User[]>("/api/v1/users");
 */
export async function getJSON<T = any>(path: string): Promise<T> {
  const headers: Record<string, string> = { Accept: "application/json" };
  if (REST_API_TOKEN) headers["Authorization"] = `Bearer ${REST_API_TOKEN}`;
  const res = await fetch(`${REST_BASE_URL}${path}`, { headers });
  if (!res.ok) throw new Error(`REST ${path} → ${res.status}`);
  return res.json() as Promise<T>;
}
