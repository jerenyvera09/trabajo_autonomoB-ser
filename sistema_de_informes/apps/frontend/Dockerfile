FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 3000

# Vite dev server para demo local (docker-compose)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
