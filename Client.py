import socket
import json

class ClientSocket:

    '''
    client part
    '''

    def __init__(self, host = "127.0.0.1", port = 33336):

        '''
        initialize object
        :param host: str host, default local server
        :param port: int port, default 33336
        '''

        self.host = host
        self.port = port
        self.sock = ""

    def init_socket(self):

        '''
        create socket
        '''

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):

        '''
        create connection to server
        '''

        self.sock.connect((self.host, self.port))

    def send(self, data):

        '''
        send data to server and wait answer
        :param data: data for send
        :return: answer server
        '''

        self.sock.send(json.dumps(data).encode('utf-8'))
        res = self.sock.recv(1024)
        if not res:
            return None
        return json.loads(res)



