import socket

"""
host can be a hostname, IP address, or empty string. 
If an IP address is used, host should be an IPv4-formatted address string. 
The IP address 127.0.0.1 is the standard IPv4 address for the loopback interface, so only processes 
on the host will be able to connect to the server. If you pass an empty string, 
the server will accept connections on all available IPv4 interfaces.
"""
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
"""
When using the loopback interface (IPv4 address 127.0.0.1 or IPv6 address ::1), 
data never leaves the host or touches the external network. In the diagram above, 
the loopback interface is contained inside the host. This represents the internal 
nature of the loopback interface and shows that connections and data that transit 
it are local to the host.
"""

"""
port represents the TCP port number to accept connections on from clients. 
It should be an integer from 1 to 65535, as 0 is reserved. Some systems may require superuser 
privileges if the port number is less than 1024.
"""

PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
conn, addr = server.accept()
"""
El método server.accept() en la programación de sockets (Python) bloquea la ejecución del servidor 
hasta que un cliente intenta conectarse. Una vez establecida la conexión, devuelve un nuevo 
objeto socket (conn) para enviar/recibir datos con ese cliente, y una tupla (addr) con la dirección IP 
y puerto del cliente.
One thing that’s imperative to understand is that you now have a new socket object from .accept(). 
This is important because it’s the socket that you’ll use to communicate with the client. 
It’s distinct from the listening socket that the server is using to accept new connections
"""

"""
Usar with statement con un objeto socket lo trata como un gestor de contexto. 
Esto significa que, automáticamente, cuando la ejecución sale del bloque with, 
el socket de conexión (conn) se cerrará, incluso si ocurren errores (manejo seguro de recursos).
""" 
with conn:
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)
