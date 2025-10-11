package main

import (
	"fmt"
	"net/http"
	"github.com/gorilla/websocket"
)

// Estructura para gestionar clientes conectados
var clientes = make(map[*websocket.Conn]bool)

// Canal para mensajes entrantes
var broadcast = make(chan string)

// Configuración del upgrader para WebSocket
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Permite conexiones desde cualquier origen
	},
}

// Función principal
func main() {
	// Ruta para manejar conexiones WebSocket
	http.HandleFunc("/ws", manejarConexiones)

	// Goroutine para manejar mensajes entrantes
	go manejarMensajes()

	fmt.Println("Servidor WebSocket iniciado en :8080")
	// Inicia el servidor HTTP
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("Error al iniciar el servidor:", err)
	}
}

// manejarConexiones gestiona nuevas conexiones WebSocket
func manejarConexiones(w http.ResponseWriter, r *http.Request) {
	// Actualiza la conexión HTTP a WebSocket
	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Println("Error al actualizar a WebSocket:", err)
		return
	}
	// Agrega el cliente al mapa
	clientes[ws] = true
	fmt.Println("Cliente conectado:", ws.RemoteAddr())

	// Maneja la desconexión limpia
	defer func() {
		ws.Close()
		delete(clientes, ws)
		fmt.Println("Cliente desconectado:", ws.RemoteAddr())
	}()

	// Lee mensajes del cliente
	for {
		_, msg, err := ws.ReadMessage()
		if err != nil {
			break // Sale del bucle si hay error (desconexión)
		}
		// Envía el mensaje al canal broadcast
		broadcast <- string(msg)
	}
}

// manejarMensajes reenvía los mensajes a todos los clientes conectados
func manejarMensajes() {
	for {
		msg := <-broadcast
		for cliente := range clientes {
			err := cliente.WriteMessage(websocket.TextMessage, []byte(msg))
			if err != nil {
				fmt.Println("Error al enviar mensaje:", err)
				cliente.Close()
				delete(clientes, cliente)
			}
		}
	}
}
