FROM golang:1.20-alpine AS build
WORKDIR /src
COPY go.mod go.sum* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/ws ./main.go

FROM alpine:3.19
WORKDIR /app
COPY --from=build /out/ws /app/ws
EXPOSE 8080
ENV WS_PORT=8080
CMD ["/app/ws"]
