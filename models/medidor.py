from datetime import datetime
import json
import random
import socket
import time
import uuid
import requests
import argparse

from servidor import write_database, read_database
client_id = uuid.uuid1()
IP = "localhost"
PORTA = 5000
REFERENCIA = f"/{client_id}"

# ID exclusivo do cliente

bol = True
http_request = f"POST {REFERENCIA} HTTP/1.1\r\nHost: {IP}:{PORTA}\r\n\r\n".encode()
http_put = f"POST {REFERENCIA} HTTP/1.1\r\nHost: {IP}:{PORTA}\r\n\r\n".encode()
print(
    f"O id do seu Medidor foi criado e para acessar os dados do medidor basta acessar: http://localhost:5000/?id={client_id}")

# Configurar a leitura dos argumentos da linha de comando
parser = argparse.ArgumentParser(
    description='Monitor de consumo de energia elétrica')
parser.add_argument('--limite-alerta', type=int,
                    default=500, help='Limite de alerta em kWh')
parser.add_argument('--multiplicador', type=int, default=1,
                    help='Fator de multiplicação do consumo em kWh')
args = parser.parse_args()

def increment(consumo_atual, incremento=1):
    return consumo_atual + incremento


# Verificar se o client_id já existe no arquivo JSON
storage_data = read_database()
if client_id in storage_data:
    # Carrega o histórico de consumo a partir do arquivo JSON
    historico_consumo = storage_data[client_id]['historico']
    consumo_total = storage_data[client_id]['consumo_total']
    consumo_atual_kWh = storage_data[client_id]['consumo_atual_kWh']
else:
    # Cria uma lista vazia para o histórico de consumo
    historico_consumo = []
    consumo_total = 0
    
# Executar o monitor de energia com os argumentos fornecidos
limite_alerta = args.limite_alerta
multiplicador = args.multiplicador
while True:
    consumo_atual_kWh = random.randint(450, 500)
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    consumo_kwh = consumo_atual_kWh + increment(consumo_atual_kWh, multiplicador)
    consumo_total += consumo_kwh
    fatura = f"R$ {consumo_total * 0.5:.2f}"  # Multiplica pelo valor do kWh e arredonda para duas casas decimais
    # Adiciona o consumo atual ao histórico de consumo
    historico_consumo.append({
        'data_hora': data_hora_atual,
        'consumo_kwh': consumo_kwh
    })

    # Verificar se o consumo está acima do limite de alerta
    if consumo_kwh > limite_alerta:
        alerta = f"{data_hora_atual} - ALERTA: Consumo muito alto: {consumo_kwh:.2f} kWh"
    else:
        alerta = ""

    # Define o payload com os dados a serem enviados
    payload = {
        'consumo_atual_kWh': consumo_atual_kWh,
        'consumo_kwh': consumo_kwh,
        'consumo_total_kWh': consumo_total,
        'alerta': alerta,
        'Fatura_Atual': historico_consumo,
        'Valor_da_Fatura': fatura
    }

    # Converte o payload em uma string JSON
    message_body = json.dumps(payload).encode('utf-8')
    # Cria o socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((IP, PORTA))
        # Envia a mensagem para o servidor
        # verificar a variavel bol = true, o socket request sera um Post, se bol = false a requizição sera um Put:
        if bol:
            client_socket.send(http_request + message_body)
            bol = False
        else:
            client_socket.send(http_put + message_body)

    # Aguarda um segundo antes de medir novamente
    time.sleep(10)
