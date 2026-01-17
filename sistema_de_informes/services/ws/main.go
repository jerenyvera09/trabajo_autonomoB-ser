package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
)

// --- Semana 6: Salas/Canales, auth opcional y notificaciones por sala ---

type Broadcast struct {
	Room string
	Data []byte
}

var (
	rooms   = make(map[string]map[*websocket.Conn]bool)
	roomsMu sync.RWMutex
	// Canal de broadcast por sala
	broadcast = make(chan Broadcast, 256)

	// Config
	allowedOrigins = parseAllowedOrigins(os.Getenv("ALLOWED_ORIGINS")) // CSV o vacío para permitir todos (dev)
	requireAuth    = os.Getenv("WS_REQUIRE_AUTH") == "1"
	jwtSecret      = os.Getenv("WS_JWT_SECRET")
	authServiceURL = strings.TrimRight(os.Getenv("AUTH_SERVICE_URL"), "/")

	revokedMu   sync.RWMutex
	revokedJTIs = make(map[string]struct{})
)

func setRevoked(jtis []string) {
	revokedMu.Lock()
	defer revokedMu.Unlock()
	newMap := make(map[string]struct{}, len(jtis))
	for _, j := range jtis {
		j = strings.TrimSpace(j)
		if j != "" {
			newMap[j] = struct{}{}
		}
	}
	revokedJTIs = newMap
}

func isRevoked(jti string) bool {
	if strings.TrimSpace(jti) == "" {
		return false
	}
	revokedMu.RLock()
	_, ok := revokedJTIs[jti]
	revokedMu.RUnlock()
	return ok
}

func startRevokedSync() {
	if authServiceURL == "" {
		authServiceURL = "http://auth-service:8001"
	}
	interval := 30 * time.Second
	if v := os.Getenv("REVOKED_SYNC_SECONDS"); strings.TrimSpace(v) != "" {
		if n, err := time.ParseDuration(v + "s"); err == nil {
			if n < 5*time.Second {
				n = 5 * time.Second
			}
			interval = n
		}
	}

	go func() {
		for {
			func() {
				resp, err := http.Get(authServiceURL + "/auth/revoked")
				if err != nil {
					return
				}
				defer resp.Body.Close()
				if resp.StatusCode >= 400 {
					return
				}
				b, _ := ioutil.ReadAll(resp.Body)
				var decoded map[string]interface{}
				if err := json.Unmarshal(b, &decoded); err != nil {
					return
				}
				raw, ok := decoded["jtis"].([]interface{})
				if !ok {
					return
				}
				var jtis []string
				for _, it := range raw {
					if s, ok := it.(string); ok {
						jtis = append(jtis, s)
					}
				}
				setRevoked(jtis)
			}()
			time.Sleep(interval)
		}
	}()
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		if len(allowedOrigins) == 0 {
			return true // demo/dev
		}
		origin := r.Header.Get("Origin")
		for _, o := range allowedOrigins {
			if strings.EqualFold(o, origin) {
				return true
			}
		}
		return false
	},
}

func parseAllowedOrigins(csv string) []string {
	if strings.TrimSpace(csv) == "" {
		return nil
	}
	parts := strings.Split(csv, ",")
	var out []string
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p != "" {
			out = append(out, p)
		}
	}
	return out
}

func getRoom(r *http.Request) string {
	room := r.URL.Query().Get("room")
	if room == "" {
		room = "general"
	}
	return room
}

func authOK(r *http.Request) bool {
	if !requireAuth {
		return true
	}
	token := ""
	auth := r.Header.Get("Authorization")
	if strings.HasPrefix(strings.ToLower(auth), "bearer ") {
		token = strings.TrimSpace(auth[7:])
	}
	if token == "" {
		token = r.URL.Query().Get("token")
	}
	if token == "" || jwtSecret == "" {
		return false
	}
	parsed, err := jwt.Parse(token, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return []byte(jwtSecret), nil
	})
	if err != nil || parsed == nil || !parsed.Valid {
		return false
	}
	if claims, ok := parsed.Claims.(jwt.MapClaims); ok {
		if jtiVal, ok := claims["jti"].(string); ok {
			if isRevoked(jtiVal) {
				return false
			}
		}
	}
	return true
}

func addToRoom(room string, c *websocket.Conn) {
	roomsMu.Lock()
	if rooms[room] == nil {
		rooms[room] = make(map[*websocket.Conn]bool)
	}
	rooms[room][c] = true
	roomsMu.Unlock()
}

func removeFromRoom(room string, c *websocket.Conn) {
	roomsMu.Lock()
	if conns, ok := rooms[room]; ok {
		delete(conns, c)
		if len(conns) == 0 {
			delete(rooms, room)
		}
	}
	roomsMu.Unlock()
}

func manejarConexiones(w http.ResponseWriter, r *http.Request) {
	if !authOK(r) {
		http.Error(w, "unauthorized", http.StatusUnauthorized)
		return
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("upgrade error:", err)
		return
	}

	room := getRoom(r)
	addToRoom(room, conn)
	log.Printf("cliente conectado en sala '%s' (total salas: %d)\n", room, len(rooms))

	// Higiene: límites y keepalive (lectura)
	conn.SetReadLimit(1 << 20)
	conn.SetReadDeadline(time.Now().Add(60 * time.Second))
	conn.SetPongHandler(func(string) error {
		conn.SetReadDeadline(time.Now().Add(60 * time.Second))
		return nil
	})

	// Ping periódico (escritura) para mantener la conexión viva
	done := make(chan struct{})
	go func() {
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				deadline := time.Now().Add(5 * time.Second)
				_ = conn.WriteControl(websocket.PingMessage, []byte{}, deadline)
			case <-done:
				return
			}
		}
	}()

	// Bucle de lectura de mensajes del cliente
	for {
		msgType, msg, err := conn.ReadMessage()
		if err != nil {
			log.Println("read error:", err)
			break
		}
		if msgType != websocket.TextMessage && msgType != websocket.BinaryMessage {
			continue
		}

		// Detectar eventos estándar y emitir a la sala actual
		msgStr := string(msg)

		// Eventos soportados: new_report, update_report, comment_added
		var eventType string
		var eventMessage string

		switch msgStr {
		case "new_report":
			eventType = "new_report"
			eventMessage = "Se ha creado un nuevo reporte"
		case "update_report":
			eventType = "update_report"
			eventMessage = "Se ha actualizado un reporte"
		case "comment_added":
			eventType = "comment_added"
			eventMessage = "Se agregó un comentario al reporte"
		default:
			// Reenviar mensaje original si no es un evento estándar
			select {
			case broadcast <- Broadcast{Room: room, Data: msg}:
			default:
				log.Println("broadcast buffer lleno; descartando mensaje")
			}
			continue
		}

		// Emitir evento estandarizado
		if eventType != "" {
			notificacion := map[string]string{
				"event":   eventType,
				"message": eventMessage,
			}
			jsonData, _ := json.Marshal(notificacion)
			select {
			case broadcast <- Broadcast{Room: room, Data: jsonData}:
				log.Printf("Notificación '%s' enviada a sala '%s'\n", eventType, room)
			default:
				log.Println("broadcast buffer lleno; descartando mensaje")
			}
		}
	}

	close(done)
	conn.Close()
	removeFromRoom(room, conn)
	log.Printf("cliente desconectado de sala '%s'\n", room)
}

func manejarMensajes() {
	for msg := range broadcast {
		// Snapshot de conexiones de la sala
		roomsMu.RLock()
		var targets []*websocket.Conn
		if conns, ok := rooms[msg.Room]; ok {
			for c := range conns {
				targets = append(targets, c)
			}
		}
		roomsMu.RUnlock()

		// Enviar a cada conexión
		for _, c := range targets {
			c.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if err := c.WriteMessage(websocket.TextMessage, msg.Data); err != nil {
				log.Println("write error:", err)
				// Remover conexión con error
				go func(cc *websocket.Conn) {
					cc.Close()
					// Buscar y eliminar de cualquier sala
					roomsMu.Lock()
					for room, conns := range rooms {
						if _, ok := conns[cc]; ok {
							delete(conns, cc)
							if len(conns) == 0 {
								delete(rooms, room)
							}
						}
					}
					roomsMu.Unlock()
				}(c)
			}
		}
	}
}

// Endpoint HTTP para simular eventos por sala
func notifyNewReport(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Sala desde la ruta /notify/{room} o query ?room=
	path := r.URL.Path
	room := "general"
	if strings.HasPrefix(path, "/notify/") {
		rest := strings.TrimPrefix(path, "/notify/")
		if rest != "" {
			if i := strings.Index(rest, "/"); i >= 0 {
				room = rest[:i]
			} else {
				room = rest
			}
		}
	} else {
		// compatibilidad con /notify
		q := r.URL.Query().Get("room")
		if q != "" {
			room = q
		}
	}

	body, _ := io.ReadAll(r.Body)
	defer r.Body.Close()

	// Estructura base; permitimos adjuntar payload/data sin romper compatibilidad
	notificacion := map[string]interface{}{
		"event":   "new_report",
		"message": "Se ha creado un nuevo reporte",
	}

	if len(body) > 0 {
		var payload map[string]interface{}
		if err := json.Unmarshal(body, &payload); err == nil {
			if msg, ok := payload["message"].(string); ok {
				notificacion["message"] = msg
			}
			if ev, ok := payload["event"].(string); ok && strings.TrimSpace(ev) != "" {
				notificacion["event"] = ev
			}
			// Permitir incluir datos adicionales bajo la clave "data" o "payload"
			if data, ok := payload["data"]; ok {
				notificacion["data"] = data
			} else if pl, ok := payload["payload"]; ok {
				notificacion["data"] = pl
			}
		}
	}

	jsonData, _ := json.Marshal(notificacion)
	select {
	case broadcast <- Broadcast{Room: room, Data: jsonData}:
		log.Printf("Notificación enviada a sala '%s': %s\n", room, string(jsonData))
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`{"status":"ok","room":"` + room + `"}`))
	default:
		http.Error(w, "Broadcast channel full", http.StatusServiceUnavailable)
	}
}

func main() {
	mux := http.NewServeMux()

	// Sincronización periódica de blacklist (sin consultar auth-service en cada request)
	startRevokedSync()

	// Endpoint WS (handshake: ws://host:port/ws?room=reports[&token=...])
	mux.HandleFunc("/ws", manejarConexiones)

	// Endpoints para notificar por sala: /notify (query room) o /notify/{room}
	mux.HandleFunc("/notify", notifyNewReport)
	mux.HandleFunc("/notify/", notifyNewReport)

	// Healthcheck
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status":"ok","service":"ws"}`))
	})

	// CORS simple para handshake y endpoints HTTP
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

	port := os.Getenv("WS_PORT")
	if strings.TrimSpace(port) == "" {
		port = "8080"
	}

	srv := &http.Server{
		Addr:         ":" + port,
		Handler:      handler,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	go manejarMensajes()

	go func() {
		log.Printf("Servidor WebSocket en :%s\n", port)
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
