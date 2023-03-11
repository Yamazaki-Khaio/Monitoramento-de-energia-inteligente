import json
import random
import socket
import time
import uuid

import requests

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
url = f"http://127.0.0.1:5000/medidor/{client_id}"
http_request = f"POST / HTTP/1.1\r\nHost: {IP}:{PORTA}\r\n\r\n".encode()
while True:
    # Obtém a data e hora atual
    data_hora_atual = time.strftime("%Y-%m-%d %H:%M:%S")
    consumo = round(random.uniform(CONSUMO_MIN, CONSUMO_MAX), 2)

    # Define o payload com os dados a serem enviados
    payload = {
        'medidor_id': MEDIDOR_ID,
        'cliente_id': CLIENTE_ID,
        'consumo_kWh': consumo,
        'data_hora': data_hora_atual
    }

    # Converte o payload em uma string JSON
    #message = json.dumps(payload)
    response = requests.post(url, json=payload)


        # Recebe a resposta do servidor
    #data = sock.recv(1024)

    storage_data = read_database()
    # Verifica se o client_id já existe no arquivo JSON
    if client_id in storage_data:
        # Adiciona as informações do medidor às informações existentes do cliente
        storage_data[str(client_id)]['medidores'].append(payload)
    else:
        # Cria um novo registro para o cliente com as informações do medidor
        storage_data[str(client_id)] = {
            'medidores': [payload]
        }

    # Salva as informações atualizadas no arquivo JSON
    write_database(storage_data)

    # Incrementa o valor atual de energia medido


    valor_atual += incremento

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)
