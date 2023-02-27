import json
import socket
import threading
import datetime

# Cria um socket TCP/IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço do servidor e a porta
server_address = ('127.0.0.1', 5000)

s.bind(server_address)

# Define o número máximo de conexões em fila
s.listen(1)
print(f"Servidor escutando em {server_address}")


def handle_request(request):
    method, path, body = request.split('\n')
    path = path.split()[1]
    body = json.loads(body)

    if method == 'GET' and path == '/':
        return (200, {'Content-Type': 'application/json'}, json.dumps({'message': 'Hello, World!'}))
    elif method == 'POST' and path == '/echo':
        return (200, {'Content-Type': 'application/json'}, json.dumps(body))
    else:
        return (404, {'Content-Type': 'application/json'}, json.dumps({'message': 'Not Found'}))


# Função para lidar com as conexões dos clientes
def handle_client(client_socket):
    while True:
        # Recebe os dados do cliente
        data = client_socket.recv(1024)
        if data:
            # Envia uma resposta para o cliente
            message = f"Resposta: {data.decode()}"
            client_socket.sendall(message.encode())
        else:
            # Encerra a conexão com o cliente
            client_socket.close()
            break


# Loop infinito para aceitar conexões dos clientes
while True:
    # Aceita a conexão do cliente
    client_socket, client_address = s.accept()
    print(f"Conexão estabelecida com {client_address}")

    # Cria uma nova thread para lidar com a conexão do cliente
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

    # def medidor:
    """
    implmentação do medidor
    :return:
    """
