import socket
from threading import Thread

class Server:
    # Usamos una lista de clase
    Clientes = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Agregamos REUSEADDR para que puedas reiniciar el server sin drama
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Conexión de: " + str(address))
            
            # Lanzamos el manejo del cliente de una vez para no bloquear el accept
            Thread(target=self.initial_setup, args=(client_socket,)).start()

    def initial_setup(self, client_socket):
        # Primero pedimos el nombre
        try:
            client_name = client_socket.recv(1024).decode().strip()
            # Usamos 'nombre' consistentemente
            client = {"nombre": client_name, "client_socket": client_socket}
            
            Server.Clientes.append(client)
            self.broadcast_message(client_name, f"{client_name} has joined the chat")
            
            # Ahora sí, manejamos sus mensajes
            self.handle_new_client(client)
        except:
            client_socket.close()

    def handle_new_client(self, client):
        client_name = client['nombre']
        client_socket = client['client_socket']
        while True:
            try:
                client_message = client_socket.recv(1024).decode()
                
                # Verificamos si se desconectó o mandó 'bye'
                if not client_message or "bye" in client_message.lower():
                    raise Exception("Client disconnected")
                
                self.broadcast_message(client_name, f"{client_name}: {client_message}")
            except:
                self.broadcast_message(client_name, f"{client_name} has left the chat")
                if client in Server.Clientes:
                    Server.Clientes.remove(client)
                client_socket.close()
                break

    def broadcast_message(self, sender_name, message):
        print(f"DEBUG: Broadcasting -> {message}")
        for client in Server.Clientes:
            # No se lo mandamos al que lo escribió
            if client["nombre"] != sender_name:
                try:
                    client["client_socket"].send(message.encode())
                except:
                    # Si falla el envío, el socket está muerto
                    client["client_socket"].close()
                    if client in Server.Clientes:
                        Server.Clientes.remove(client)

if __name__ == "__main__":
    # Usamos el puerto que elegiste
    server = Server("127.0.0.1", 7632)
    server.listen()