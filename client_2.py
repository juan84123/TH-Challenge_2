import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 7632

def recibir_mensajes(sock):
    """Esta función vive en un hilo aparte escuchando SIEMPRE al servidor"""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                print("\nConexión perdida con el servidor.")
                os._exit(0)
            
            # Imprimimos el mensaje y volvemos a poner el '>' para escribir
            print(f"\n{data}\n> ", end="", flush=True)
        except:
            break

# --- INICIO DEL CLIENTE ---
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

nombre = input("¿Cuál es tu nombre?: ")
cliente.send(nombre.encode()) # Mandamos el nombre apenas conectamos

# Lanzamos el hilo para recibir mensajes mientras nosotros escribimos
hilo_escucha = threading.Thread(target=recibir_mensajes, args=(cliente,))
hilo_escucha.daemon = True
hilo_escucha.start()

print(f"¡Conectado, {nombre}! (Escribí 'bye' para salir)")

while True:
    # Bucle principal: solo para enviar mensajes
    msg = input("> ")
    if msg.lower() == '/exit':
        cliente.send("/exit".encode())
        break
    cliente.send(msg.encode())

cliente.close()