import json
import socket

IP = "127.0.0.1"
PORTA = 5000
CLIENTE_ID = "cliente001"
while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORTA))
    payload = {
        'cliente_id': CLIENTE_ID
    }

    # Converte o payload em uma string JSON
    message = json.dumps(payload)

    # Envia a mensagem para o servidor
    try:
        sock.sendall(message.encode())
    except ConnectionAbortedError as e:
        print(f"Erro ao enviar mensagem: {e}")
        sock.close()
        continue

    # Recebe a resposta do servidor
    data = sock.recv(1024)