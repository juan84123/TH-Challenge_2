import socket

# 1-Server sets up a listening socket
# si se usa un string vacio el servidor va aceptar la coneccion de cualquier computadora
HOST = "127.0.0.1"

# que puerto debe escuchar, tiene que ser mayor que 1023, porque?
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # la b significa que el mensaje se va a enviar en unidades de 8 bits
    s.sendall(b"Hello, world")
    data = s.recv(1024)

print(f"Received {data}")
