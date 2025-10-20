package main

import (
	"encoding/json"
	"io"
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

		// SEMANA 5: Detectar evento "new_report" y emitir notificación
		msgStr := string(msg)
		if msgStr == "new_report" {
			notificacion := map[string]string{
				"event":   "new_report",
				"message": "Se ha creado un nuevo reporte",
			}
			jsonData, _ := json.Marshal(notificacion)
			select {
			case broadcast <- jsonData:
				log.Println("Notificación de nuevo reporte enviada a todos los clientes")
			default:
				log.Println("broadcast buffer lleno; descartando mensaje")
			}
		} else {
			// Reenviar otros mensajes normalmente
			select {
			case broadcast <- msg:
			default:
				log.Println("broadcast buffer lleno; descartando mensaje")
			}
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

// SEMANA 5: Endpoint HTTP para simular eventos
func notifyNewReport(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	body, _ := io.ReadAll(r.Body)
	defer r.Body.Close()

	notificacion := map[string]string{
		"event":   "new_report",
		"message": "Se ha creado un nuevo reporte",
	}

	if len(body) > 0 {
		var payload map[string]interface{}
		if err := json.Unmarshal(body, &payload); err == nil {
			if msg, ok := payload["message"].(string); ok {
				notificacion["message"] = msg
			}
		}
	}

	jsonData, _ := json.Marshal(notificacion)
	select {
	case broadcast <- jsonData:
		log.Printf("Notificación enviada: %s\n", string(jsonData))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok","message":"Notificación enviada"}`))
	default:
		http.Error(w, "Broadcast channel full", http.StatusServiceUnavailable)
	}
}

func main() {
	mux := http.NewServeMux()

	// Endpoint WS
	mux.HandleFunc("/ws", manejarConexiones)

	// SEMANA 5: Endpoint para simular notificaciones
	mux.HandleFunc("/notify", notifyNewReport)

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
