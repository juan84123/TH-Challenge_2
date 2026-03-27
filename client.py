import socket
from threading import Thread
import os

class Client:
    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((HOST, PORT))
        except ConnectionRefusedError:
            print("❌ No se pudo conectar. ¿Está el servidor encendido?")
            return

        self.name = input("Enter your name: ")
        self.talk_to_server()

    def talk_to_server(self):
        # Primero enviamos el nombre para que el server nos registre
        self.socket.send(self.name.encode())
        
        # Hilo para recibir mensajes (siempre activo)
        Thread(target=self.receive_message, daemon=True).start()
        
        # Bucle principal para enviar mensajes
        self.send_message()

    def send_message(self):
        print(f"✅ ¡Conectado como {self.name}! Escribí 'bye' para salir.")
        while True:
            client_input = input("")
            if client_input.lower() == "bye":
                self.socket.send(f"{self.name}: bye".encode())
                break
            
            # Enviamos el mensaje formateado
            client_message = f"{self.name}: {client_input}"
            self.socket.send(client_message.encode())
        
        self.socket.close()
        os._exit(0)

    def receive_message(self):
        while True: # <--- AGREGADO: Bucle infinito para seguir escuchando
            try:
                server_message = self.socket.recv(1024).decode()
                if not server_message:
                    print("\n⚠️ Conexión cerrada por el servidor.")
                    os._exit(0)
                
                # Corregido el código de color \033
                print("\033[1;31;40m" + server_message + "\033[0m")
                print("> ", end="", flush=True) # Un prompt para que sepas dónde escribir
            except:
                break

if __name__ == "__main__":
    Client("127.0.0.1", 7632)