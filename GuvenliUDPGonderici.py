import os
import socket
import datetime
import sys
import datetime
import time

class GuvenliUDPGonderici:
    def __init__(self, fileName):
        self.host = 'localhost'
        self.bufferSize = 1024
        self.fileName = fileName
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.s.bind(('localhost', 58699))
        self.addr = (self.host, 58700)
        self.s.settimeout(0.05)
        
    # receive ack 
    def waitAck(self):
        try:
            data, addr = self.s.recvfrom(self.bufferSize)
            #print('Ack received', int.from_bytes(data, byteorder='big', signed=False))
            return int.from_bytes(data, byteorder='big', signed=False)
        except socket.timeout:
            #print('timeout')
            return -1

    def run(self):
        if os.path.exists(self.fileName):
            print('Transfer operation is started')
            
            packetNumber = 0
            fHandle = open(self.fileName, 'rb')
            
            fdata = fHandle.read(self.bufferSize)
            data = fdata + packetNumber.to_bytes(length=1, byteorder='big')

            start = datetime.datetime.now()
            self.s.sendto(data, self.addr)
            # send again
            while self.waitAck() != packetNumber:
                #print('Invalid ack', packetNumber)
                self.s.sendto(data, self.addr)
                
            packetNumber = (packetNumber + 1) % 256

            while (fdata):
                fdata = fHandle.read(self.bufferSize)
                if not data:
                    break;

                data = fdata + packetNumber.to_bytes(length=1, byteorder='big')
                self.s.sendto(data, self.addr)
                # send again
                while (self.waitAck() % 256) != packetNumber % 256:
                    #print('Invalid ack', packetNumber % 256)
                    self.s.sendto(data, self.addr)
                packetNumber = (packetNumber + 1) % 256

            for i in range(1000):
                self.s.sendto(b'STOP-CONN', self.addr)
            self.s.close()
            fHandle.close()
            print('Transfer operation is completed. {} packet sent.'.format(packetNumber))
                    
            end = datetime.datetime.now()
            print('Elapsed time {} ms'.format(int((end - start).total_seconds() * 1000)))  # milliseconds)
        else:
            print('File {} cannot be opened'.format(self.fileName))


if len(sys.argv) == 2:
    gonderici = GuvenliUDPGonderici(sys.argv[1])
    gonderici.run()
else:
    print('Incorrect argument usage. [python3 UDPGonderici.py buyuk_veri.txt]')
