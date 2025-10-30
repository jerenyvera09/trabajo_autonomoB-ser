/**
 * REST API DataSource
 * Cliente fetch para consumir endpoints del servicio REST (FastAPI)
 * Semana 6 - Integración GraphQL ↔ REST
 */

const REST_BASE_URL = process.env.REST_BASE_URL || "http://localhost:8000";
const REST_API_TOKEN = process.env.REST_API_TOKEN || "";

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
    return this.getWithFallback<any[]>(["/api/v1/reports", "/reportes"]);
  }

  async getCategories() {
    return this.getWithFallback<any[]>(["/api/v1/categories", "/categorias"]);
  }

  async getAreas() {
    return this.getWithFallback<any[]>(["/api/v1/areas", "/areas"]);
  }

  async getStates() {
    return this.getWithFallback<any[]>(["/api/v1/states", "/estados-reporte"]);
  }

  async getRoles() {
    return this.getWithFallback<any[]>(["/api/v1/roles", "/roles"]);
  }

  async getUsers() {
    return this.getWithFallback<any[]>(["/api/v1/users", "/usuarios"]);
  }

  async getComments() {
    return this.getWithFallback<any[]>(["/api/v1/comments", "/comentarios"]);
  }

  async getRatings() {
    return this.getWithFallback<any[]>(["/api/v1/ratings", "/puntuaciones"]);
  }

  async getFiles() {
    return this.getWithFallback<any[]>(["/api/v1/files", "/archivos"]);
  }

  async getTags() {
    return this.getWithFallback<any[]>(["/api/v1/tags", "/etiquetas"]);
  }

  async getAttachments() {
    // Intenta en orden: /attachments, /files, /archivos
    return this.getWithFallback<any[]>([
      "/api/v1/attachments",
      "/api/v1/files",
      "/archivos",
    ]);
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
