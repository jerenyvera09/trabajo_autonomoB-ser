import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import { typeDefs } from "./schema";
import { resolvers } from "./resolvers/reportes";

// Servidor GraphQL básico para reportes
async function bootstrap() {
  const server = new ApolloServer({ typeDefs, resolvers });
  const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
  });
  console.log(`🚀 Servidor GraphQL listo en ${url}`);
}

bootstrap().catch((err) => {
  console.error("Error iniciando GraphQL:", err);
  process.exit(1);
});
