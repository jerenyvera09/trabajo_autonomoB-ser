package main

import (
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gorilla/websocket"
)

var clientes = make(map[*websocket.Conn]bool)
var broadcast = make(chan []byte, 256)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	// Para demo: abierto. En producción restringir dominios.
	CheckOrigin: func(r *http.Request) bool { return true },
}

func manejarConexiones(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("upgrade error:", err)
		return
	}
	defer conn.Close()

	clientes[conn] = true
	log.Printf("cliente conectado (%d)\n", len(clientes))

	// Higiene: límites y keepalive
	conn.SetReadLimit(1 << 20)
	conn.SetReadDeadline(time.Now().Add(60 * time.Second))
	conn.SetPongHandler(func(string) error {
		conn.SetReadDeadline(time.Now().Add(60 * time.Second))
		return nil
	})

	for {
		msgType, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("read error:", err)
			break
		}
		if msgType != websocket.TextMessage && msgType != websocket.BinaryMessage {
			continue
		}
		select {
		case broadcast <- msg:
		default:
			log.Println("broadcast buffer lleno; descartando mensaje")
		}
	}

	delete(clientes, conn)
	log.Printf("cliente desconectado (%d)\n", len(clientes))
}

func manejarMensajes() {
	for msg := range broadcast {
		for c := range clientes {
			c.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if err := c.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Println("write error:", err)
				c.Close()
				delete(clientes, c)
			}
		}
	}
}

func main() {
	mux := http.NewServeMux()

	// Endpoint WS
	mux.HandleFunc("/ws", manejarConexiones)

	// Healthcheck
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status":"ok","service":"ws"}`))
	})

	// CORS simple para handshake
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}
		mux.ServeHTTP(w, r)
	})

	srv := &http.Server{
		Addr:         ":8080",
		Handler:      handler,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	go manejarMensajes()

	go func() {
		log.Println("Servidor WebSocket en :8080")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %v", err)
		}
	}()

	// Apagado
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	<-stop
	log.Println("apagando servidor...")
	_ = srv.Close()
}
