import socket
import threading

nombre_usuario = input("Cual es tu nombre: ")

HOST = "127.0.0.1" #localhost ver que es especificacmente 
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

def mensaje_recibido():
    while True:
        try:
            mensaje = client.recv(1024).decode("utf-8")
            if mensaje == "nombre":
                client.send(nombre_usuario.encode("utf-8"))
            else:
                print(f"\r{mensaje}") # \r vuelve al inicio de la línea
                print("> ", end="", flush=True) # Redibuja el cursor               
        except:
            print("\nOcurrio un error")
            client.close()
            break

def escribir_mensaje():
    while True:
        mensaje_a_enviar = f"{nombre_usuario}: {input("")}"
        client.send(mensaje_a_enviar.encode("utf-8"))

thread_recibido = threading.Thread(target=mensaje_recibido)
thread_recibido.start()
thread_escribir = threading.Thread(target=escribir_mensaje)
thread_escribir.start()
