FROM node:20-alpine

WORKDIR /app

# Install dependencies (incl. dev deps because we run tsx in dev mode)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY tsconfig.json ./
COPY src ./src
COPY tests ./tests

EXPOSE 4000

# Run GraphQL server
CMD ["npm", "run", "dev"]
