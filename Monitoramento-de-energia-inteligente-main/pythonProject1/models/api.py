import socket
import threading

# Cria um socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define o endereço do servidor e a porta
server_address = ('127.0.0.1', 5000)
sock.bind(server_address)

# Define o número máximo de conexões em fila
sock.listen(1)
print(f"Servidor escutando em {server_address}")

# Função para lidar com as conexões dos clientes
