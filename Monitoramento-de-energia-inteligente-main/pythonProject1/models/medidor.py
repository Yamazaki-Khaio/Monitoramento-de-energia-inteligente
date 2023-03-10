import json
import random
import socket
import time
import uuid

from models.servidor import database, write_database, read_database

IP = "127.0.0.1"
PORTA = 5000

# ID exclusivo do cliente
client_id = uuid.uuid1()


MEDIDOR_ID = 'medidor001'
CLIENTE_ID = 'cliente001'

# Configura o sensor de energia para medir a energia em tempo real
valor_inicial = 10
incremento = 2
valor_atual = valor_inicial
CONSUMO_MIN = 1  # Consumo mínimo em kWh
CONSUMO_MAX = 10  # Consumo máximo em kWh
bool = True


while True:
    # Cria um socket e conecta ao servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORTA))

    # Obtém a data e hora atual
    data_hora_atual = time.strftime("%Y-%m-%d %H:%M:%S")
    consumo = round(random.uniform(CONSUMO_MIN, CONSUMO_MAX), 2)

    # Define o payload com os dados a serem enviados
    payload = {
        'medidor_id': MEDIDOR_ID,
        'cliente_id': CLIENTE_ID,
        'consumo kWh': consumo,
        'Data e Hora': data_hora_atual

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

    # Fecha a conexão com o servidor
    sock.close()

    # Armazena os dados do medidor no banco de dados
    storage_data = read_database()
    storage_data[str(client_id)] = payload
    write_database(storage_data)

    # Incrementa o valor atual de energia medido
    valor_atual += incremento

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)