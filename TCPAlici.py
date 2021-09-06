import socket


class TCPAlici:
    def __init__(self):
        self.host = 'localhost'
        self.port = 58800
        self.bufferSize = 1024
        self.fileName = 'alici.txt'
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    def run(self):
        fHandle = open(self.fileName, 'wb')
        
        l = self.s.recv(self.bufferSize)
        print('Receive operation is started')
        while (l):
            fHandle.write(l)
            l = self.s.recv(self.bufferSize)

        print('Receive operation is completed')
        self.s.close()
        fHandle.close()

alici = TCPAlici()
alici.run()
