import socket

HOST = '127.0.0.1'
PORT = 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, client = s.accept()
    with conn:
        print(f"Conectado por {client}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)