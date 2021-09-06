import socket


class UDPAlici:
    def __init__(self):
        self.host = 'localhost'
        self.port = 58799
        self.bufferSize = 1024
        self.fileName = 'alici.txt'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.s.bind((self.host, self.port))

    def run(self):
        packetNumber = 0
        
        data, addr = self.s.recvfrom(self.bufferSize)
        print('Receive operation is started')
        packetNumber += 1
        
        fHandle = open(self.fileName, 'wb')
        while (data != b'STOP-CONN'):
            fHandle.write(data)
            data, addr = self.s.recvfrom(self.bufferSize)
            packetNumber += 1

        print('Receive operation is completed {} packet received'.format(packetNumber))
        self.s.close()
        fHandle.close()

alici = UDPAlici()
alici.run()
