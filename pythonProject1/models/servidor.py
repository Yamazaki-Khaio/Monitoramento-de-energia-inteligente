import socket
import sys
from threading import Thread
import json
import os
HOST = "0.0.0.0"
PORT = 5000
MAX_BUFFER_SIZE = 4092
body = None
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
    try:
        with open("db.json", "r") as db:
            storage_file = db.read()
            if storage_file.strip() == "":
                # arquivo vazio
                return {}
            else:
                storage_data = json.loads(storage_file)
                if not isinstance(storage_data, dict):
                    # conteúdo inválido
                    return {}
                else:
                    return storage_data
    except FileNotFoundError:
        # arquivo não encontrado
        return {}
# Escrever conteúdo no arquivo json
def write_database(data):
    with open('db.json', 'w') as db_file:
        json.dump(data, db_file, indent=4, sort_keys=True)



def create_headers(status_code: int, status_text: str, message_body="") -> bytes:
    global body
    # headers
    response_protocol = "HTTP/1.1"
    response_status_code = status_code
    response_status_text = status_text
    response_content_type = "application/json; encoding=utf8"
    response_connection = "close"
    message_body_bytes = message_body.encode('utf-8') if message_body else ''.join(body).encode('utf-8') if body else b''
    response_content_length = len(message_body_bytes)

    # Create seções
    status_line = f"{response_protocol} {response_status_code} {response_status_text}\r\n"
    connection = f"Connection: {response_connection}\r\n"
    content_type = f"Content-Type: {response_content_type}\r\n"
    content_length = f"Content-Length: {response_content_length}\r\n"
    empty_line = "\r\n"

    # Concatenar string
    response_header = (
        status_line +
        connection +
        content_type +
        content_length +
        empty_line
    )

    # Concatenar header e corpo da mensagem
    response = response_header.encode('utf-8') + message_body_bytes

    return response

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
    response_headers = None
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

        if response_headers is not None:
            client_socket.send(response_headers)


        client_socket.close()
        print(f"Conexão do {ip}:{port} foi fechada.")

    print(f"Client thread do {ip}:{port} foi fechada.")


# Get entrada solicitada
def get_content(data: list):
    content = None

    # procurar a entrada solicitada
    for line in data:
        if line.startswith("GET "):
            content = line.split()[1]
            break

    # verificar se a entrada foi encontrada
    if content is None:
        return None

    # verificar se a entrada está codificada em UTF-8
    try:
        content = content.decode('utf-8')
    except UnicodeDecodeError:
        return None

    return content

# Processo de solicitação do tipo GET
import urllib.parse

def do_GET(data: list):
    query = urllib.parse.urlparse(data[1]).query
    query_dict = urllib.parse.parse_qs(query)
    name = query_dict.get('id', [''])[0]

    storage_data = read_database()

    if storage_data is not None:
        if name:
            value = storage_data.get(name)
            if value:
                response_body = json.dumps({name: value})
                return create_headers(200, "OK", response_body)
            else:
                return create_headers(404, "Not Found")
        else:
            response_body = json.dumps(storage_data)
            return create_headers(200, "OK", response_body)
    else:
        return create_headers(404, "Not Found")



# Processo de solicitação do tipo Post
def do_POST(data: list):
    global body

    body = data[5:]
    id = data[1].strip('/')

    # Aqui está o novo código para armazenar o conteúdo recebido:
    storage_data = read_database()
    storage_data[id] = json.loads(' '.join(body))
    write_database(storage_data)

    # Criar e enviar a resposta
    response_body = json.dumps({"status": "ok"})
    return create_headers(200, "OK", response_body)

# Processo de solicitação do tipo PUT
def do_PUT(data: list):
    content = get_content(data)
    if content is None:
        return create_headers(400, "Bad Request")

    try:
        content_dict = json.loads(content)
    except json.JSONDecodeError:
        return create_headers(400, "Invalid JSON")

    if not isinstance(content_dict, dict):
        return create_headers(400, "Invalid Data")

    content_key = next(iter(content_dict), None)

    if not isinstance(content_key, str):
        return create_headers(400, "Invalid Data")

    storage_data = read_database()

    if content_key in storage_data:
        try:
            storage_data.append(content_dict)
            write_database(storage_data)
            return create_headers(200, "OK")
        except Exception as e:
            return create_headers(500, str(e))
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
