import socket


class GuvenliUDPAlici:
    def __init__(self):
        self.host = 'localhost'
        self.bufferSize = 1025
        self.fileName = 'alici.txt'
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.s.bind(('localhost', 58799))
        self.packetNumber = 0
        self.totalPacketNumber = 0

    # send ack
    def sendACK(self, seqNumber):
        self.s.sendto(seqNumber.to_bytes(length=1, byteorder='big'), (self.host, 58800))
        
    def run(self):
        print('Receive operation is started')
        
        fHandle = open(self.fileName, 'wb')
        
        rcvData, addr = self.s.recvfrom(self.bufferSize)
        seqNumber = int.from_bytes(rcvData[1024:], byteorder='big', signed=False)
        data = rcvData[:1024]
        self.totalPacketNumber += 1
        
        while (rcvData != b'STOP-CONN'):
            while ((seqNumber % 256) != (self.packetNumber) % 256):
                rcvData, addr = self.s.recvfrom(self.bufferSize)
                seqNumber = int.from_bytes(rcvData[1024:], byteorder='big', signed=False)
                data = rcvData[:1024]
                #print('---', self.packetNumber, seqNumber)
                self.sendACK(seqNumber % 256)
                
            self.sendACK((self.packetNumber) % 256)
            self.packetNumber = (self.packetNumber + 1) % 256
            fHandle.write(rcvData)
            self.totalPacketNumber += 1
        

        print('Receive operation is completed {} packet received'.format(self.totalPacketNumber))
        self.s.close()
        fHandle.close()

alici = GuvenliUDPAlici()
alici.run()
