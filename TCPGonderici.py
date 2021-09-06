import os
import socket
import datetime
import sys
import datetime


class TCPGonderici:
    def __init__(self, fileName):
        self.host = 'localhost'
        self.port = 58700
        self.bufferSize = 1024
        self.fileName = fileName
        self.s = socket.socket()
        self.s.connect((self.host, self.port))

    def run(self):
        if os.path.exists(self.fileName):
            fHandle = open(self.fileName, 'rb')
            data = fHandle.read(self.bufferSize)
            
            print('Transfer operation is started')
            start = datetime.datetime.now()
            self.s.send(data)
            while (data):
                data = fHandle.read(self.bufferSize)
                self.s.send(data)
                
            print('Transfer operation is completed')
            end = datetime.datetime.now()
            print('Elapsed time {} ms'.format(int((end - start).total_seconds() * 1000)))  # milliseconds)
            
            self.s.close()
            fHandle.close()
        else:
            print('File {} cannot be opened'.format(self.fileName))


if len(sys.argv) == 2:
    gonderici = TCPGonderici(sys.argv[1])
    gonderici.run()
else:
    print('Incorrect argument usage. [python3 TCPGonderici.py buyuk_veri.txt]')
