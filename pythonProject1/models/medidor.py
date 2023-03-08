import socket
import time

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
while True:
    energy_actual = next(energia)
    print("kWh: {}".format(energy_actual))

    # Envia os dados de energia medidos para o servidor
    cliente.send(str(energy_actual).encode())

    # Aguarda um segundo antes de medir novamente
    time.sleep(1)

# Fecha a conexão
cliente.close()