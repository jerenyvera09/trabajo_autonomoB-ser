import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import { ApolloServer } from '@apollo/server';
import { typeDefs } from '../src/schema';
import { resolvers } from '../src/resolvers/reportes';

let server: ApolloServer;

beforeAll(() => {
  server = new ApolloServer({ typeDefs, resolvers });
});

afterAll(async () => {
  await server.stop();
});

describe('GraphQL reports (Semana 6)', () => {
  it('reports returns paginated items with total', async () => {
    const fakeData = [
      { id: '1', title: 'A', description: '', status: 'Abierto', priority: 'Media', location: '', created_at: '2025-10-19T00:00:00Z' },
      { id: '2', title: 'B', description: '', status: 'Cerrado', priority: 'Alta', location: '', created_at: '2025-10-20T00:00:00Z' },
      { id: '3', title: 'C', description: '', status: 'Abierto', priority: 'Baja', location: '', created_at: '2025-10-21T00:00:00Z' },
    ];

    const fetchMock = vi.fn(async () => ({ ok: true, json: async () => fakeData } as any));
    // @ts-ignore
    global.fetch = fetchMock;

    const res = await server.executeOperation({
      query: /* GraphQL */ `
        query($limit: Int, $offset: Int, $status: String, $sortBy: ReportSortBy, $sortDir: SortDir) {
          reports(limit: $limit, offset: $offset, status: $status, sortBy: $sortBy, sortDir: $sortDir) {
            total
            limit
            offset
            items { id title status created_at }
          }
        }
      `,
      variables: { limit: 2, offset: 0, status: 'Abierto', sortBy: 'created_at', sortDir: 'DESC' },
    });

    expect(res.body.kind).toBe('single');
    const payload: any = (res.body as any).singleResult.data.reports;
    expect(payload.total).toBe(2);
    expect(payload.items.length).toBe(2);
    expect(payload.items[0].id).toBe('3');
  });

  it('reportsAnalytics returns totals by status', async () => {
    const fakeData = [
      { id: '1', title: 'A', description: '', status: 'Abierto', priority: 'Media', location: '', created_at: '2025-10-19T00:00:00Z' },
      { id: '2', title: 'B', description: '', status: 'Cerrado', priority: 'Alta', location: '', created_at: '2025-10-20T00:00:00Z' },
      { id: '3', title: 'C', description: '', status: 'Abierto', priority: 'Baja', location: '', created_at: '2025-10-21T00:00:00Z' },
    ];

    const fetchMock = vi.fn(async () => ({ ok: true, json: async () => fakeData } as any));
    // @ts-ignore
    global.fetch = fetchMock;

    const res = await server.executeOperation({
      query: /* GraphQL */ `
        query { reportsAnalytics { total byStatus { clave valor } } }
      `,
    });

    expect(res.body.kind).toBe('single');
    const data: any = (res.body as any).singleResult.data;
    expect(data.reportsAnalytics.total).toBe(3);
    const abierto = data.reportsAnalytics.byStatus.find((k: any) => k.clave === 'Abierto');
    expect(abierto.valor).toBe(2);
  });
});
