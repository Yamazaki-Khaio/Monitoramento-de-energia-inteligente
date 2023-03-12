from datetime import datetime
import json
import random
import time
import uuid
import requests
import argparse

from models.servidor import write_database, read_database

IP = "127.0.0.1"
PORTA = 5000

# ID exclusivo do cliente
client_id = uuid.uuid1()


url = f"http://127.0.0.1:5000/{client_id}"
http_request = f"POST / HTTP/1.1\r\nHost: {IP}:{PORTA}\r\n\r\n".encode()

print(f"O id do Cliente é: {client_id}, para acessar os dados do medidor basta acessar:http://127.0.0.1:5000/?id={client_id}")

# Configurar a leitura dos argumentos da linha de comando
parser = argparse.ArgumentParser(description='Monitor de consumo de energia elétrica')
parser.add_argument('--limite-alerta', type=int, default=500, help='Limite de alerta em kWh')
parser.add_argument('--multiplicador', type=float, default=1.0, help='Fator de multiplicação do consumo em kWh')
args = parser.parse_args()

# Executar o monitor de energia com os argumentos fornecidos
limite_alerta = args.limite_alerta
multiplicador = args.multiplicador
while True:
    consumo_atual = random.randint(100, 1000)
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    consumo_kwh = consumo_atual * multiplicador
    consumo_total = consumo_atual + consumo_kwh
    fatura = consumo_total * 0.5  # R$ 0,50 por kWh

    with open("historico_consumo.txt", "a") as f:
        f.write(f"{data_hora_atual} - Consumo atual: {consumo_kwh:.2f} kWh\n")

    # Verificar se o consumo está acima do limite de alerta
    if consumo_atual > limite_alerta:
       alerta = f"{data_hora_atual} - ALERTA: Consumo muito alto: {consumo_kwh:.2f} kWh"
    else:
        alerta = ""

    with open('historico_consumo.txt', 'r') as f:
        historico_consumo = f.read()

    # Define o payload com os dados a serem enviados
    payload = {
        'consumo_atual_kWh': consumo_atual,
        'consumo_kwh': consumo_kwh,
        'consumo_total_kWh': consumo_total,
        'alerta': alerta,
        'historico_consumo_kWh': historico_consumo,
        'fatura_a_pagar': fatura
    }

    # Converte o payload em uma string JSON
    message = json.dumps(payload)

    # Envia a mensagem para o servidor
    response = requests.post(url, json=payload)

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


    #valor_atual += incremento

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)

