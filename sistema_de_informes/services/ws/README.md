# WebSocket Server (Integrante 3 (Vera Mero Jereny Jhonnayker) - Go/Gorilla)

## Requisitos

- Go 1.20+

## Ejecutar

go mod tidy
go run main.go

# Servidor en :8080

## Probar

- Health: curl http://localhost:8080/
- WS (dos terminales):
  wscat -c ws://localhost:8080/ws
  wscat -c ws://localhost:8080/ws
  # Escribe en una y observa broadcast en la otra.

## Seguridad

CheckOrigin abierto solo para demo; restringe dominios en producción.
