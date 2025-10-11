# Servicio GraphQL (Integrante 2 - Carlos Campuzano)

Implementación inicial para la Semana 4 (Commit 2) usando TypeScript y Apollo Server.

## Requisitos

- Node.js 18+

## Instalación

```cmd
cd sistema_de_informes\services\graphql
npm install
```

## Ejecutar en desarrollo

```cmd
npm run dev
```

Salida esperada:

```
🚀 Servidor GraphQL listo en http://localhost:4000/
```

## Pruebas rápidas (GraphQL)

- Query lista de reportes:

```graphql
query {
  reportes {
    id
    titulo
    estado
    categoria
    creadoEn
  }
}
```

- Crear reporte:

```graphql
mutation {
  crearReporte(input: { titulo: "Nueva incidencia", descripcion: "Detalle" }) {
    id
    titulo
    estado
  }
}
```

> Nota: En Semana 4 los datos están en memoria (mock). En Semanas 5-6 se integrará con el REST/DB.
