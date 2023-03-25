import json
import socket

HOST = "localhost"
PORT = 5000

class InvalidResponseError(Exception):
    pass

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())

        response = b""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

        if not response:
            raise InvalidResponseError("Empty response")

        return response.decode()

def send_get_request(referencia):
    request = f"GET /?id={referencia} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n"
    response = send_request(request)

    body = response.split("\r\n\r\n")[-1]
    try:
        json_data = json.loads(body)
    except json.JSONDecodeError as e:
        raise InvalidResponseError(f"Error decoding JSON: {e}")

    return json_data

def exibir_dados(data):
    while True:
        # exibe o menu
        print("Digite o número correspondente ao dado que deseja visualizar:")
        print("1 - Consumo atual")
        print("2 - Consumo total")
        print("3 - Fatura atual")
        print("4 - Valor da fatura")
        print("0 - Sair")

        # aguarda a entrada do usuário
        opcao = input("Opção escolhida: ")
        

    



        if opcao == "1":
            
            print(f"Consumo atual: {data[REFERENCIA]['consumo_atual_kWh']}")
        elif opcao == "2":
            print(f"Consumo total: {data[REFERENCIA]['consumo_total_kWh']}")
        elif opcao == "3":
            print(f"Fatura atual: {data[REFERENCIA]['Fatura_Atual']}")
        elif opcao == "4":
            print(f"Valor da fatura: {data[REFERENCIA]['Valor_da_Fatura']}")
        elif opcao == "0":
            # encerra o programa
            return False
        else:
            print("Opção inválida. Digite um número entre 0 e 4.")
while True:
    REFERENCIA = input("DIGITE SEU ID: ")
    data = send_get_request(REFERENCIA)
    if data:
        # exibe os dados
        print(data)
        while exibir_dados(data):
            pass
    else:
        print("Resposta inválida")
        continue