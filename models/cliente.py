import random
import socket

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 5000  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b" Oi, testando")

    data = s.recv(1024)

    print("Recebido:", data.decode())
    consumo = random.random()
    s.sendall(consumo.encode(float))
