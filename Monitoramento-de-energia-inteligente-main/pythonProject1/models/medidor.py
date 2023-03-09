import socket
import time
import requests

# Endereço IP e porta do servidor
IP = "127.0.0.1"
PORTA = 5000

# Cria o objeto socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta ao servidor
cliente.connect((IP, PORTA))

def incrementar_automatico(valor_inicial, incremento=1):
    valor = valor_inicial

    while True:
        yield valor
        valor += incremento


# Configura o sensor de energia para medir a energia em tempo real
energia = incrementar_automatico(10, 2)
id = incrementar_automatico(0,1)
while True:
    energy_actual = next(energia)
    medidor_id = next(id)

    url = (f"http://127.0.0.1:5000/medidor/123")
    payload = {"kWh": "energy_actual"}

    
    http_request = b"POST / HTTP/1.1\r\n\r\nHost: 127.0.0.1:5000\r\n\r\n"
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        response = response.json()
        print(response)

    else:
        print(response.text)

    cliente.sendall(http_request)
    print(http_request.decode)
    
    print("kWh: {}".format(energy_actual))
   
    # Envia os dados de energia medidos para o servidor
   
    cliente.sendall(str(energy_actual).encode())

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)

# Fecha a conexão
cliente.close()