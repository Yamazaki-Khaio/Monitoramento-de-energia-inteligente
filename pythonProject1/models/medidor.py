from datetime import datetime
import json
import random
import socket
import time
import uuid
import requests
import argparse

from servidor import write_database, read_database

IP = "0.0.0.0"
PORTA = 5900

# ID exclusivo do cliente
client_id = uuid.uuid1()
bol = True

url = f"http://localhost:5000/{client_id}"
http_request = f"POST / HTTP/1.1\r\nHost: {IP}:{PORTA}\r\n\r\n".encode()

print(f"O id do Cliente é: {client_id}, para acessar os dados do medidor basta acessar: http://0.0.0.0:5000/?id={client_id}")

# Configurar a leitura dos argumentos da linha de comando
parser = argparse.ArgumentParser(description='Monitor de consumo de energia elétrica')
parser.add_argument('--limite-alerta', type=int, default=500, help='Limite de alerta em kWh')
parser.add_argument('--multiplicador', type=float, default=1.0, help='Fator de multiplicação do consumo em kWh')
args = parser.parse_args()

# Verificar se o client_id já existe no arquivo JSON
storage_data = read_database()
if client_id in storage_data:
    # Carrega o histórico de consumo a partir do arquivo JSON
    historico_consumo = storage_data[client_id]['historico']
else:
    # Cria uma lista vazia para o histórico de consumo
    historico_consumo = []
# Executar o monitor de energia com os argumentos fornecidos
limite_alerta = args.limite_alerta
multiplicador = args.multiplicador
while True:
    consumo_atual = random.randint(100, 1000)
    data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    consumo_kwh = consumo_atual * multiplicador
    consumo_total = consumo_atual + consumo_kwh
    fatura = consumo_total * 0.5  # R$ 0,50 por kWh

    # Adiciona o consumo atual ao histórico de consumo
    historico_consumo.append({
        'data_hora': data_hora_atual,
        'consumo_kwh': consumo_kwh
    })

    # Verificar se o consumo está acima do limite de alerta
    if consumo_atual > limite_alerta:
       alerta = f"{data_hora_atual} - ALERTA: Consumo muito alto: {consumo_kwh:.2f} kWh"
    else:
        alerta = ""


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
    # Cria o socket
      # Verifica se o client_id já existe no arquivo JSON
    if bool:
        # Adiciona as informações do medidor às informações existentes do cliente
        requests.post(url, json=payload)
        bol = False
    else:
        # Cria um novo registro para o cliente com as informações do medidor
        requests.put(url, json=payload)
        

    # Envia a mensagem para o servidor
    
    

    storage_data = read_database()

    # Salva as informações atualizadas no arquivo JSON
    write_database(storage_data)

    # Incrementa o valor atual de energia medido


    #valor_atual += incremento

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)

