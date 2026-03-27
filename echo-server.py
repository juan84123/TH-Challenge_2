import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost), para usar solo en esta pc
#host = socket.gethostbyname(socket.gethostname()) tener el ip privado de manera dinamica
PORT = 65432  # Port to listen on (non-privileged ports are > 1023), se usa mayor que eso porque los otro son reservados

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen() #dentro del parentesis se puede limitar la cantidad de conecciones, pasandole un int, que seria la cantidad de conecciones 
conn, addr = server.accept()

with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024) #1024 buffer del mensaje, falta decodificar is se envia un mensaje
        if not data:
            break
        conn.sendall(data)
