import argparse
import socket
import math
import sys
import random

from PacketMagic import errorize_packet, is_mine

class RelayServer:
    def __init__(self,maxPktSize):
        self.MAX_LEN  = maxPktSize
    def create_socket(self,ipAddr,portA,portB,isDgram,isErroneous):
        self.isDgram = isDgram
        self.isErroneous = isErroneous # This server drops and corrupts packets
        self.portA   = portA
        self.portB   = portB
        if isDgram:
            print("Create a UDP server")
            if isErroneous:
                self.sktA = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
                self.sktB = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
            else:
                self.sktA = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sktB = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sktA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sktB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sktA.bind((ipAddr,portA))
        self.sktB.bind((ipAddr,portB))
        if not isDgram:
            self.sktA.listen(1)
            self.sktB.listen(1)
    def parse_error_rates(self,fname):
        line = open(fname,"r").readline() # assumes format "p q"
        split_line = line.split(" ")
        self.error_drop = float(split_line[0]) - float(split_line[1])
        self.error_bit  = float(split_line[1])
        print("This server will cause errors -- drop: " + str(self.error_drop)\
            + " bit err: " + str(self.error_bit))
    def run(self):
        if self.isErroneous:
            while True:
                # We receive from the IP layer
                # +8 for the UDP header
                # +20 for the IP header
                recv_a_data = self.sktA.recv(self.MAX_LEN + 8 + 20)
                recv_a_data = is_mine(recv_a_data, self.portA, self.portB-1, self.portB)
                if b'NOTMINE' != recv_a_data:
                    # Either do nothing
                    # or flip a bit
                    # or drop the packet
                    rn = random.random()
                    if rn < self.error_bit:
                        print("Error A to B")
                        recv_a_data = errorize_packet(recv_a_data)
                    if rn >= self.error_drop:
                        self.sktB.sendto(recv_a_data,('localhost',self.portB-1))
                    else:
                        print("Drop A to B")
        if not self.isDgram:
            clntBSocket, addressB = self.sktB.accept()
            clntASocket, addressA = self.sktA.accept()
            recvData = "START"
            print("Begin transmission")
            while recvData != b'':
                recvData = clntASocket.recv(self.MAX_LEN)
                clntBSocket.send(recvData)
            clntBSocket.close()
            clntASocket.close()
            print("End transmission")
        else:
            recvData = "START"
            print("Begin transmission")
            packet_count = 0
            while recvData != b'STOP-CONN':
                recvData = self.sktA.recv(self.MAX_LEN)
                packet_count += 1
                self.sktB.sendto(recvData,('localhost',self.portB-1))
            for i in range(1000):
                self.sktB.sendto(b'STOP-CONN',('localhost',self.portB-1))
            print("End transmission")
            print("Transmitted " + str(packet_count) + " packets.")
    def run_stop_wait(self):
        finished = False
        print("Server Ready!")
        while not finished:
            if self.isErroneous:
                # We receive from the IP layer
                # +1 for the seq number
                # +8 for the UDP header
                # +20 for the IP header
                recv_a_data = self.sktA.recv(self.MAX_LEN + 1 + 8 + 20)
                recv_a_data = is_mine(recv_a_data, self.portA, self.portB-1, self.portB)
                if b'NOTMINE' != recv_a_data:
                    # Either do nothing
                    # or flip a bit
                    # or drop the packet
                    rn = random.random()
                    if rn < self.error_bit:
                        print("Error A to B")
                        recv_a_data = errorize_packet(recv_a_data)
                    if rn >= self.error_drop:
                        self.sktB.sendto(recv_a_data,('localhost',self.portB-1))
                    else:
                        print("Drop A to B")
            else:
                recv_a_data = self.sktA.recv(self.MAX_LEN + 1)
                self.sktB.sendto(recv_a_data,('localhost',self.portB-1))
            if self.isErroneous:
                recv_b_data = self.sktB.recv(1 + 8 + 20) # 1 because B sends only acks
                recv_b_data = is_mine(recv_b_data, self.portB, self.portA-1, self.portA)
                if b'NOTMINE' != recv_b_data:
                    rn = random.random()
                    if rn < self.error_bit:
                        print("Error B to A")
                        recv_b_data = errorize_packet(recv_b_data)
                    if rn >= self.error_drop:
                        self.sktB.sendto(recv_b_data,('localhost',self.portA-1))
                    else:
                        print("Drop B to A")
            else:
                recv_b_data = self.sktB.recv(1)
                self.sktB.sendto(recv_b_data,('localhost',self.portA-1))
    def close(self):
        self.sktA.close()
        self.sktB.close()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--datagram", help="use UDP sockets", action="store_true")
parser.add_argument("-sw", "--stopandwait", help="stop and wait over UDP", action="store_true")
parser.add_argument("-e", "--erroneous", \
        help="name of the file that has p and q values")
args = parser.parse_args()

rs = RelayServer(1024)
rs.create_socket('localhost',58700,58800 , \
    args.datagram,
    args.erroneous) # relay server is erroneous
if args.erroneous:
    rs.parse_error_rates(args.erroneous)
if args.stopandwait:
    rs.run_stop_wait()
else:
    rs.run()
rs.close()
