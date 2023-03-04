import socket
import sys
from threading import Thread
import json
import os

HOST = "127.0.0.1"
PORT = 5000
MAX_BUFFER_SIZE = 1024


def main():
    initialize_database()
    start_server()


# Criar arquivo json
def initialize_database():
    # Create database file
    if not os.path.exists("db.json"):
        with open("db.json", "w+") as db:
            db.write("{\n}")


# Ler conteúdo do arquivo json
def read_database():
    # Read database file
    with open("db.json", "r") as db:
        storage_file = json.load(db)

    return storage_file


# Escrever conteúdo no arquivo json
def write_database(storage_file):
    with open("db.json", "w") as file:
        json.dump(storage_file, file, indent=4, sort_keys=True)


# Criar headers
def create_headers(status_code: int, status_text: str, message_body=""):
    # headers
    response_protocol = "HTTP/1.2"
    response_status_code = status_code
    response_status_text = status_text
    response_content_type = "application/json; encoding=utf8"
    response_connection = "close"
    response_content_length = str(len(message_body.encode('utf-8')))

    # Create seções
    status_line = (
        f"{response_protocol} {response_status_code} {response_status_text}\r\n"
    )
    connection = f"Connection: {response_connection}\r\n"
    content_type = f"Content-Type: {response_content_type}\r\n"
    content_length = f"Content-Length:  {response_content_length}\r\n"
    empty_line = f"\r\n"

    #Concatenar string
    response_header = (
            status_line +
            connection +
            content_type +
            content_length +
            empty_line +
            message_body
    )

    # Encode string para utf-8 bytes
    response_header_encoded = response_header.encode("utf-8")

    return response_header_encoded


# Cria & start server socket
def start_server():
    # Cria server socket tcp
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket
    try:
        server_socket.bind((HOST, PORT))
        print(f"Ligando o server socket ao host:{HOST} e port {PORT}")
    except:
        print(f"Ligação falhou. Erro: {str(sys.exc_info())}")
        sys.exit()

    # Ativando Listen passiva sockets
    server_socket.listen(23)

    while True:

        # Aguardar e aceitar a conexão de entrada
        (client_socket, address) = server_socket.accept()
        ip, port = str(address[0]), str(address[1])
        print(f"A conexão do {ip}:{port} foi estabelecida.")

        try:
            Thread(target=client_thread, args=(client_socket, ip, port)).start()
            print(f"Client thread com o {ip}:{port} foi criado.")
        except:
            print(f"Client thread com {ip}:{port} não deu start.")


# Thread para cada cliente
def client_thread(client_socket, ip, port):
    # Listen dos dados recebidos
    data = receive_data(client_socket)
    print(data)

    if data:

        if data[0] == "GET":
            response_headers = do_GET(data)

        if data[0] == "POST":
            response_headers = do_POST(data)

        if data[0] == "PUT":
            response_headers = do_PUT(data)

        if data[0] == "DELETE":
            response_headers = do_DELETE(data)

        client_socket.send(response_headers)
        client_socket.close()
        print(f"Conexão do {ip}:{port} foi fechada.")

    print(f"Client thread do {ip}:{port} foi fechada.")


# Get entrada solicitada
def get_content(data: list):
    # verifica o tamanho da entrada
    if "Content-Length:" in data:
        con_len_index = data.index("Content-Length:")
        con_len_value = data[con_len_index + 1]


        if con_len_value == "0":
            return None
    else:
        return None


    if "Content-Type:" not in data:
        return None


    return data[-1]


# Processo de solicitação do tipo GET
def do_GET(data: list):
    content = get_content(data)
    if content == None:
        return create_headers(400, "Bad Request")

    storage_data = read_database()

    if content in storage_data:
        value = storage_data.get(content)
        return create_headers(200, "OK", value)
    else:
        return create_headers(404, "Not Found")


# Processo de solicitação do tipo Post
def do_POST(data: list):
    content = get_content(data)
    if content == None:
        return create_headers(400, "Bad Request")

    storage_data = read_database()

    if content in storage_data:
        return create_headers(409, "Conflict")
    else:
        storage_data[content] = ""
        write_database(storage_data)
        return create_headers(201, "Created")


# Processo de solicitação do tipo PUT
def do_PUT(data: list):
    content = get_content(data)
    if content == None:
        return create_headers(400, "Bad Request")

    storage_data = read_database()

    content_dict = json.loads(content)
    content_key = list(content_dict.keys())[0]

    if content_key in storage_data:
        storage_data.update(content_dict)
        write_database(storage_data)
        return create_headers(200, "OK")
    else:
        return create_headers(404, "Not Found")


# Processo de solicitação do tipo DELETE
def do_DELETE(data: list):
    content = get_content(data)
    if content == None:
        return create_headers(400, "Bad Request")

    storage_data = read_database()

    if content in storage_data:
        storage_data.pop(content)
        write_database(storage_data)
        return create_headers(200, "OK")
    else:
        return create_headers(404, "Not Found")



def receive_data(client_socket):
    client_data = client_socket.recv(MAX_BUFFER_SIZE)
    decoded_data = (
        str(client_data).strip("b'").rstrip().replace("\\n", "").replace("\\r", " ").replace("\\t", "")
    )
    data_variables = str(decoded_data).split()

    return data_variables


if __name__ == "__main__":
    main()
