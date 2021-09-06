import os
import socket
import datetime
import sys
import datetime
import time

class UDPGonderici:
    def __init__(self, fileName):
        self.host = 'localhost'
        self.port = 58700
        self.bufferSize = 1024
        self.fileName = fileName
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        #self.s.bind((self.host, self.port))
        self.addr = (self.host, self.port)

    def run(self):
        packetNumber = 0
        
        if os.path.exists(self.fileName):
            fHandle = open(self.fileName, 'rb')
            data = fHandle.read(self.bufferSize)
            
            print('Transfer operation is started')
            start = datetime.datetime.now()
            self.s.sendto(data, self.addr)
            packetNumber += 1
            while (data):
                data = fHandle.read(self.bufferSize)
                if data:
                    self.s.sendto(data, self.addr)
                    packetNumber += 1
                    time.sleep(2/1000)
            end = datetime.datetime.now()
            for i in range(1000):
                self.s.sendto(b'STOP-CONN', self.addr)
            self.s.close()
            fHandle.close()
            
            print('Transfer operation is completed. {} packet sent.'.format(packetNumber))
            print('Elapsed time {} ms'.format(int((end - start).total_seconds() * 1000)))  # milliseconds)
        else:
            print('File {} cannot be opened'.format(self.fileName))


if len(sys.argv) == 2:
    gonderici = UDPGonderici(sys.argv[1])
    gonderici.run()
else:
    print('Incorrect argument usage. [python3 UDPGonderici.py buyuk_veri.txt]')
