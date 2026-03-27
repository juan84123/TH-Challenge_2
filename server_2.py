import socket
import threading

# Configuración básica
HOST = '127.0.0.1'
PORT = 7632
clientes = [] # Lista de todos los sockets conectados

def broadcast(mensaje, emisor_socket):
    """Recorre la lista de clientes y les envía el mensaje (menos al que lo envió)"""
    for cliente in clientes:
        if cliente != emisor_socket:
            try:
                cliente.send(mensaje.encode())
            except:
                # Si falla, el cliente probablemente se desconectó
                if cliente in clientes:
                    clientes.remove(cliente)

def manejar_cliente(conn, addr):
    """Esta función es el 'mozo' que atiende a cada cliente por separado"""
    try:
        # Lo primero que el cliente manda es su nombre
        nombre = conn.recv(1024).decode().strip()
        print(f"{nombre} se unió desde {addr}")
        broadcast(f"{nombre} entró al chat", conn)

        while True:
            # Esperamos los mensajes del chat
            mensaje = conn.recv(1024).decode()
            
            if not mensaje or mensaje.lower() == 'bye':
                break
            
            print(f"[{nombre}]: {mensaje}")
            broadcast(f"{nombre}: {mensaje}", conn)
            
    except:
        pass
    finally:
        # Si el bucle termina, limpiamos la conexión
        if conn in clientes:
            clientes.remove(conn)
        conn.close()
        broadcast("Alguien salió del chat", None)

# --- INICIO DEL SERVIDOR ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor corriendo en {HOST}:{PORT}. Esperando valientes...")

while True:
    # El programa se queda aquí 'esperando' hasta que alguien entra
    conn, addr = server.accept()
    clientes.append(conn)
    
    # Creamos un hilo para que este cliente no trabe a los demás
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.daemon = True # Esto hace que el hilo muera si cerramos el servidor
    hilo.start()