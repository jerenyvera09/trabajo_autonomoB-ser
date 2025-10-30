/**
 * Resolver para Consulta Compuesta: reportAnalytics
 * Agrega datos de múltiples entidades en un solo objeto
 * Exporta como JSON o PDF (base64) - PDF REAL con pdfkit
 * Semana 6 - Query compuesto
 */
import { restAPI } from "../datasources/rest.js";
import PDFDocument from "pdfkit";

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
        const usuario = users.find((u: any) => u.id === reporte.user_id);
        const categoria = categories.find((c: any) => c.id === reporte.category_id);
        const estado = states.find((e: any) => e.name === reporte.status);

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
          const pdfBuffer = await new Promise<Buffer>((resolve, reject) => {
            const doc = new PDFDocument({ size: 'A4', margin: 50 });
            const chunks: Buffer[] = [];

            doc.on('data', (chunk) => chunks.push(chunk));
            doc.on('end', () => resolve(Buffer.concat(chunks)));
            doc.on('error', reject);

            // 📄 Encabezado del PDF
            doc.fontSize(20).font('Helvetica-Bold').text('REPORTE ANALÍTICO COMPLETO', { align: 'center' });
            doc.moveDown(0.5);
            doc.fontSize(10).font('Helvetica').text(`Generado: ${new Date().toLocaleString('es-ES')}`, { align: 'center' });
            doc.moveDown(1);

            // 📊 Datos del Reporte
            doc.fontSize(14).font('Helvetica-Bold').text('📋 Información del Reporte', { underline: true });
            doc.moveDown(0.5);
            doc.fontSize(11).font('Helvetica');
            doc.text(`ID: ${reporte.id}`);
            doc.text(`Título: ${reporte.title || 'N/A'}`);
            doc.text(`Descripción: ${reporte.description || 'N/A'}`);
            doc.text(`Estado: ${reporte.status || 'N/A'}`);
            doc.text(`Prioridad: ${reporte.priority || 'N/A'}`);
            doc.text(`Ubicación: ${reporte.location || 'N/A'}`);
            doc.text(`Creado: ${reporte.created_at || 'N/A'}`);
            doc.moveDown(1);

            // 👤 Usuario Creador
            if (usuario) {
              doc.fontSize(14).font('Helvetica-Bold').text('👤 Usuario Creador', { underline: true });
              doc.moveDown(0.5);
              doc.fontSize(11).font('Helvetica');
              doc.text(`Nombre: ${usuario.name || 'N/A'}`);
              doc.text(`Email: ${usuario.email || 'N/A'}`);
              doc.moveDown(1);
            }

            // 🏷️ Categoría
            if (categoria) {
              doc.fontSize(14).font('Helvetica-Bold').text('🏷️ Categoría', { underline: true });
              doc.moveDown(0.5);
              doc.fontSize(11).font('Helvetica');
              doc.text(`Nombre: ${categoria.name || 'N/A'}`);
              doc.text(`Descripción: ${categoria.description || 'N/A'}`);
              doc.moveDown(1);
            }

            // 🚦 Estado
            if (estado) {
              doc.fontSize(14).font('Helvetica-Bold').text('🚦 Estado', { underline: true });
              doc.moveDown(0.5);
              doc.fontSize(11).font('Helvetica');
              doc.text(`Estado: ${estado.name || 'N/A'}`);
              doc.moveDown(1);
            }

            // 💬 Comentarios
            doc.fontSize(14).font('Helvetica-Bold').text(`💬 Comentarios (${comentarios.length})`, { underline: true });
            doc.moveDown(0.5);
            if (comentarios.length > 0) {
              comentarios.slice(0, 10).forEach((c: any, idx: number) => {
                doc.fontSize(10).font('Helvetica');
                doc.text(`${idx + 1}. ${c.content || 'Sin contenido'}`, { indent: 20 });
                doc.fontSize(9).text(`   Fecha: ${c.date || 'N/A'}`, { indent: 20 });
                doc.moveDown(0.3);
              });
              if (comentarios.length > 10) {
                doc.fontSize(9).font('Helvetica-Oblique').text(`... y ${comentarios.length - 10} comentarios más`, { indent: 20 });
              }
            } else {
              doc.fontSize(10).font('Helvetica').text('Sin comentarios', { indent: 20 });
            }
            doc.moveDown(1);

            // ⭐ Puntuaciones
            doc.fontSize(14).font('Helvetica-Bold').text(`⭐ Puntuaciones (${puntuaciones.length})`, { underline: true });
            doc.moveDown(0.5);
            if (puntuaciones.length > 0) {
              const promedio = puntuaciones.reduce((sum: number, p: any) => sum + (p.value || 0), 0) / puntuaciones.length;
              doc.fontSize(11).font('Helvetica');
              doc.text(`Promedio: ${promedio.toFixed(2)} / 5.0`, { indent: 20 });
              puntuaciones.slice(0, 5).forEach((p: any, idx: number) => {
                doc.fontSize(10).text(`${idx + 1}. Valor: ${p.value || 0}/5`, { indent: 20 });
              });
              if (puntuaciones.length > 5) {
                doc.fontSize(9).font('Helvetica-Oblique').text(`... y ${puntuaciones.length - 5} puntuaciones más`, { indent: 20 });
              }
            } else {
              doc.fontSize(10).font('Helvetica').text('Sin puntuaciones', { indent: 20 });
            }
            doc.moveDown(1);

            // 📎 Archivos Adjuntos
            doc.fontSize(14).font('Helvetica-Bold').text(`📎 Archivos Adjuntos (${archivos.length})`, { underline: true });
            doc.moveDown(0.5);
            if (archivos.length > 0) {
              archivos.forEach((a: any, idx: number) => {
                doc.fontSize(10).font('Helvetica');
                doc.text(`${idx + 1}. ${a.filename || 'Archivo sin nombre'}`, { indent: 20 });
                if (a.url) {
                  doc.fontSize(8).fillColor('blue').text(`   URL: ${a.url}`, { indent: 20, link: a.url });
                  doc.fillColor('black');
                }
                doc.moveDown(0.3);
              });
            } else {
              doc.fontSize(10).font('Helvetica').text('Sin archivos adjuntos', { indent: 20 });
            }
            doc.moveDown(1);

            // 📌 Pie de página
            doc.fontSize(8).font('Helvetica').fillColor('gray');
            doc.text('Sistema de Informes - Universidad', { align: 'center' });
            doc.text('Reporte generado automáticamente por GraphQL', { align: 'center' });

            doc.end();
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
