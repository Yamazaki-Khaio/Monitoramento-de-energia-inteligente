"""import socket


def insert_energy_meter_value(id, value, timestamp):


def get_energy_meter_value(id):



import time

def update_energy_meter_value(id, value):
    timestamp = int(time.time())
    insert_energy_meter_value(id, value, timestamp)

def handle_client_connection(client_socket, id):
    request = client_socket.recv(1024)
    value = get_energy_meter_value(id)
    client_socket.send(str(value).encode())
    update_energy_meter_value(id, value)

def main():
    host = '0.0.0.0'
    port = 5000
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)
        handle_client_connection(c, id)
        c.close()

if __name__ == '__main__':
    main()
    """