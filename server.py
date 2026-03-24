import socket

# 1-Server sets up a listening socket
# si se usa un string vacio el servidor va aceptar la coneccion de cualquier computadora
HOST = "127.0.0.1"

# que puerto debe escuchar, tiene que ser mayor que 1023, porque?
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
