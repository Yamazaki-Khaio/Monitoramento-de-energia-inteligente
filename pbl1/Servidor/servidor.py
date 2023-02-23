import socket


class Servidor():
    def __int__(self, host, port):
        self.__host = host
        self.__port = port

    def start(self):
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endpoint = self.__host,self.__port
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen()
            print("Servidor iniciado em %s e porta : %s",self.__host, self.__port)
            while True:
                con, client = self.__tcp.accept()
                self._service(con,client)
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)


    def _service(self, con, client):
        print("Gerar os dados do medidor")
        while True:
            msg = con.recv(1024)
            msg_s = str(msg.decode('ascii'))
