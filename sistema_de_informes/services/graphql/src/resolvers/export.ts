/**
 * Resolver para Consulta Compuesta: reportAnalytics
 * Agrega datos de múltiples entidades en un solo objeto
 * Exporta como JSON o PDF (base64) - PDF REAL con pdfkit
 * Semana 6 - Query compuesto
 */
import { restAPI } from "../datasources/rest.js";
import PDFDocument from "pdfkit";

type GenericRecord = Record<string, any>;
type PdfDoc = InstanceType<typeof PDFDocument>;

const toSafeString = (value: unknown): string => {
  if (value === undefined || value === null) return "";
  if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  if (value instanceof Date) return value.toISOString();
  return "";
};

const normalizeId = (value: unknown) => toSafeString(value);
const normalizeText = (value: unknown) => toSafeString(value).toLowerCase();
const displayValue = (value: unknown, fallback = "N/A") => {
  const result = toSafeString(value).trim();
  return result === "" ? fallback : result;
};

const renderHeader = (doc: PdfDoc) => {
  doc.fontSize(20).font("Helvetica-Bold").text("REPORTE ANALÍTICO COMPLETO", { align: "center" });
  doc.moveDown(0.5);
  doc.fontSize(10).font("Helvetica").text(`Generado: ${new Date().toLocaleString("es-ES")}`, { align: "center" });
  doc.moveDown(1);
};

const renderReportSection = (doc: PdfDoc, reporte: GenericRecord) => {
  doc.fontSize(14).font("Helvetica-Bold").text("📋 Información del Reporte", { underline: true });
  doc.moveDown(0.5);
  doc.fontSize(11).font("Helvetica");
  doc.text(`ID: ${displayValue(reporte.id)}`);
  doc.text(`Título: ${displayValue(reporte.title)}`);
  doc.text(`Descripción: ${displayValue(reporte.description)}`);
  doc.text(`Estado: ${displayValue(reporte.status)}`);
  doc.text(`Prioridad: ${displayValue(reporte.priority)}`);
  doc.text(`Ubicación: ${displayValue(reporte.location)}`);
  doc.text(`Creado: ${displayValue(reporte.created_at)}`);
  doc.moveDown(1);
};

const renderUsuarioSection = (doc: PdfDoc, usuario: GenericRecord | null) => {
  if (!usuario) return;
  doc.fontSize(14).font("Helvetica-Bold").text("👤 Usuario Creador", { underline: true });
  doc.moveDown(0.5);
  doc.fontSize(11).font("Helvetica");
  doc.text(`Nombre: ${displayValue(usuario.name)}`);
  doc.text(`Email: ${displayValue(usuario.email)}`);
  doc.moveDown(1);
};

const renderCategoriaSection = (doc: PdfDoc, categoria: GenericRecord | null) => {
  if (!categoria) return;
  doc.fontSize(14).font("Helvetica-Bold").text("🏷️ Categoría", { underline: true });
  doc.moveDown(0.5);
  doc.fontSize(11).font("Helvetica");
  doc.text(`Nombre: ${displayValue(categoria.name)}`);
  doc.text(`Descripción: ${displayValue(categoria.description)}`);
  doc.moveDown(1);
};

const renderEstadoSection = (doc: PdfDoc, estado: GenericRecord | null) => {
  if (!estado) return;
  doc.fontSize(14).font("Helvetica-Bold").text("🚦 Estado", { underline: true });
  doc.moveDown(0.5);
  doc.fontSize(11).font("Helvetica");
  doc.text(`Estado: ${displayValue(estado.name)}`);
  doc.moveDown(1);
};

const renderComentariosSection = (doc: PdfDoc, comentarios: GenericRecord[]) => {
  doc.fontSize(14).font("Helvetica-Bold").text(`💬 Comentarios (${comentarios.length})`, { underline: true });
  doc.moveDown(0.5);
  if (comentarios.length === 0) {
    doc.fontSize(10).font("Helvetica").text("Sin comentarios", { indent: 20 });
    doc.moveDown(1);
    return;
  }

  const listado = comentarios.slice(0, 10);
  for (let idx = 0; idx < listado.length; idx += 1) {
    const c = listado[idx];
    doc.fontSize(10).font("Helvetica");
    doc.text(`${idx + 1}. ${displayValue(c.content, "Sin contenido")}`, { indent: 20 });
    doc.fontSize(9).text(`   Fecha: ${displayValue(c.date)}`, { indent: 20 });
    doc.moveDown(0.3);
  }
  if (comentarios.length > 10) {
    doc.fontSize(9).font("Helvetica-Oblique").text(`... y ${comentarios.length - 10} comentarios más`, { indent: 20 });
  }
  doc.moveDown(1);
};

const renderPuntuacionesSection = (doc: PdfDoc, puntuaciones: GenericRecord[]) => {
  doc.fontSize(14).font("Helvetica-Bold").text(`⭐ Puntuaciones (${puntuaciones.length})`, { underline: true });
  doc.moveDown(0.5);
  if (puntuaciones.length === 0) {
    doc.fontSize(10).font("Helvetica").text("Sin puntuaciones", { indent: 20 });
    doc.moveDown(1);
    return;
  }

  const promedio = puntuaciones.reduce((sum: number, p: GenericRecord) => {
    const value = typeof p.value === "number" ? p.value : Number(p.value ?? 0);
    return sum + (Number.isNaN(value) ? 0 : value);
  }, 0) / puntuaciones.length;
  doc.fontSize(11).font("Helvetica").text(`Promedio: ${promedio.toFixed(2)} / 5.0`, { indent: 20 });

  const listado = puntuaciones.slice(0, 5);
  for (let idx = 0; idx < listado.length; idx += 1) {
    const p = listado[idx];
    const value = typeof p.value === "number" ? p.value : Number(p.value ?? 0);
    const safeValue = Number.isNaN(value) ? 0 : value;
    doc.fontSize(10).text(`${idx + 1}. Valor: ${safeValue}/5`, { indent: 20 });
  }
  if (puntuaciones.length > 5) {
    doc.fontSize(9).font("Helvetica-Oblique").text(`... y ${puntuaciones.length - 5} puntuaciones más`, { indent: 20 });
  }
  doc.moveDown(1);
};

const renderArchivosSection = (doc: PdfDoc, archivos: GenericRecord[]) => {
  doc.fontSize(14).font("Helvetica-Bold").text(`📎 Archivos Adjuntos (${archivos.length})`, { underline: true });
  doc.moveDown(0.5);
  if (archivos.length === 0) {
    doc.fontSize(10).font("Helvetica").text("Sin archivos adjuntos", { indent: 20 });
    doc.moveDown(1);
    return;
  }

  let idx = 0;
  for (const archivo of archivos) {
    idx += 1;
    doc.fontSize(10).font("Helvetica");
    doc.text(`${idx}. ${displayValue(archivo.name, "Archivo sin nombre")}`, { indent: 20 });
    const url = displayValue(archivo.url, "");
    if (url !== "") {
      doc.fontSize(8).fillColor("blue").text(`   URL: ${url}`, { indent: 20, link: url });
      doc.fillColor("black");
    }
    doc.moveDown(0.3);
  }
  doc.moveDown(1);
};

const renderFooter = (doc: PdfDoc) => {
  doc.fontSize(8).font("Helvetica").fillColor("gray");
  doc.text("Sistema de Informes - Universidad", { align: "center" });
  doc.text("Reporte generado automáticamente por GraphQL", { align: "center" });
  doc.fillColor("black");
};

const generateReportPdf = (payload: {
  reporte: GenericRecord;
  comentarios: GenericRecord[];
  puntuaciones: GenericRecord[];
  archivos: GenericRecord[];
  usuario: GenericRecord | null;
  categoria: GenericRecord | null;
  estado: GenericRecord | null;
}): Promise<Buffer> => {
  return new Promise<Buffer>((resolve, reject) => {
    const doc = new PDFDocument({ size: "A4", margin: 50 });
    const chunks: Buffer[] = [];

    doc.on("data", (chunk) => chunks.push(chunk));
    doc.on("end", () => resolve(Buffer.concat(chunks)));
    doc.on("error", reject);

    renderHeader(doc);
    renderReportSection(doc, payload.reporte);
    renderUsuarioSection(doc, payload.usuario);
    renderCategoriaSection(doc, payload.categoria);
    renderEstadoSection(doc, payload.estado);
    renderComentariosSection(doc, payload.comentarios);
    renderPuntuacionesSection(doc, payload.puntuaciones);
    renderArchivosSection(doc, payload.archivos);
    renderFooter(doc);

    doc.end();
  });
};

export const typeDefsExport = `#graphql
  type ReportAnalytics {
    "Datos del reporte principal"
    reporte: Report
    
    "Comentarios del reporte"
    comentarios: [Comentario!]!
    
    "Puntuaciones del reporte"
    puntuaciones: [Puntuacion!]!
    
    "Archivos adjuntos"
    archivos: [ArchivoAdjunto!]!
    
    "Usuario que creó el reporte"
    usuario: Usuario
    
    "Categoría del reporte"
    categoria: Categoria
    
    "Estado del reporte"
    estado: EstadoReporte
    
    "Formato de exportación (JSON por defecto)"
    formato: String!
    
    "Si formato=pdf, contiene el PDF en base64"
    pdfBase64: String
  }

  extend type Query {
    "📊 Analytics completo de un reporte con todos sus datos relacionados"
    reportAnalytics(
      reporteId: ID!
      formato: String = "json"
    ): ReportAnalytics!
  }
`;

export const resolversExport = {
  Query: {
    reportAnalytics: async (
      _: unknown,
      { reporteId, formato = "json" }: { reporteId: string; formato?: string }
    ) => {
      try {
        // 1️⃣ Obtener todas las entidades
        const [reports, comments, ratings, attachments, users, categories, states] = await Promise.all([
          restAPI.getReports(),
          restAPI.getComments(),
          restAPI.getRatings(),
          restAPI.getAttachments(),
          restAPI.getUsers(),
          restAPI.getCategories(),
          restAPI.getStates(),
        ]);

        // 2️⃣ Filtrar datos del reporte específico
        const reporte = reports.find((r: any) => String(r.id) === reporteId);
        if (!reporte) {
          throw new Error(`Reporte ${reporteId} no encontrado`);
        }

    const comentarios = comments.filter((c: any) => String(c.report_id) === reporteId);
    const puntuaciones = ratings.filter((p: any) => String(p.report_id) === reporteId);
    const archivos = attachments.filter((a: any) => String(a.report_id) === reporteId);
    const usuario = users.find((u: any) => normalizeId(u.id) === normalizeId(reporte.user_id));
    const categoria = categories.find((c: any) => normalizeId(c.id) === normalizeId(reporte.category_id));
    const estado = states.find((e: any) => normalizeText(e.name) === normalizeText(reporte.status));

        // 3️⃣ Construir objeto agregado
        const analytics = {
          reporte,
          comentarios,
          puntuaciones,
          archivos,
          usuario,
          categoria,
          estado,
          formato,
          pdfBase64: null as string | null,
        };

        // 4️⃣ Si formato=pdf, generar PDF REAL con pdfkit
        if (formato.toLowerCase() === "pdf") {
          const pdfBuffer = await generateReportPdf({
            reporte,
            comentarios,
            puntuaciones,
            archivos,
            usuario: usuario ?? null,
            categoria: categoria ?? null,
            estado: estado ?? null,
          });

          analytics.pdfBase64 = pdfBuffer.toString("base64");
        }

        return analytics;
      } catch (error) {
        console.error("Error en reportAnalytics:", error);
        throw error;
      }
    },
  },
};
