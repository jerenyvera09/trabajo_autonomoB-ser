# Servicio GraphQL (Integrante 2 - Carlos  Delgado Campuzano)

Implementación para las *Semanas 4 y 5* usando TypeScript y Apollo Server.  
*Semana 5*: Integración con el servicio REST para consultar reportes reales.

## Requisitos

- Node.js 18+
- Servicio REST ejecutándose en http://localhost:8000

## Instalación

cmd
cd sistema_de_informes\services\graphql
npm install


## Ejecutar en desarrollo

cmd
npm run dev


Salida esperada:


🚀 Servidor GraphQL listo en http://localhost:4000/


El playground de GraphQL estará disponible en: *http://localhost:4000/graphql*

---

## 🔗 Integración con REST (Semana 5)

El resolver reports consume el endpoint del servicio REST:

graphql
query GetReports {
  reports {
    id
    title
    description
    status
    priority
  }
}


Este query realiza internamente:


GET http://localhost:8000/api/v1/reports


*Requisito*: El servicio REST debe estar ejecutándose antes de hacer esta consulta.

---

## Pruebas rápidas (GraphQL)

### 1. Query de reportes desde REST API:

graphql
query {
  reports {
    id
    title
    description
    status
    priority
  }
}


### 2. Query lista de reportes (mock local):

`graphql

graphql
query {
  reportes {
    id
    titulo
    estado
    categoria
    creadoEn
  }
}
`

- Crear reporte:

graphql
mutation {
  crearReporte(input: { titulo: "Nueva incidencia", descripcion: "Detalle" }) {
    id
    titulo
    estado
  }
}
```
> Nota: En Semana 4 los datos están en memoria (mock). En Semanas 5-6 se integrará con el REST/DB.