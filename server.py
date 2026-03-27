import socket
from threading import Thread

class Server:
    Clientes = []

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print("Servidor esperando coneccion...")

    def listen(self):
        while True:
            client_socket, address = self.socket.accept()
            print("Coneccion de: " + str(address))

            client_name = client_socket.recv(1024).decode()
            client = {"nombre": client_name, "client_socket": client_socket}

            self.broadcast_message(client_name, client_name + "has joined the chat")

            Server.Clientes.append(client)
            Thread(target = self.handle_new_client, args=(client,)).start()