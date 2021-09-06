from scapy.all import IP, UDP
from random import randint

def is_mine(pkt,port,newdest,newsrc):
    whole_packet = IP(pkt) # Generate the IP pkt to decode
    # See if this one came to our port
    if whole_packet[UDP].dport == port:
        # Modify s&d ports to ensure safe arrival to B
        whole_packet[UDP].dport = newdest
        whole_packet[UDP].sport = newsrc
        # Regenerate the chksum
        del whole_packet[UDP].chksum
        whole_packet = IP(bytes(whole_packet))
        return bytes(whole_packet[UDP])
    else:
        return b'NOTMINE'

def errorize_packet(pkt):
    bad_packet = bytearray(pkt)
    len_pkt = len(pkt)
    # select a random byte in range (0,packet's length)
    corrupt_byte = randint(0,len_pkt-1)
    corrupt_bit  = randint(0,7)
    corrupt_bit  = 1 << corrupt_bit
    # invert the bit at [corrupt_byte][corrupt_bit]
    bad_packet[corrupt_byte] ^= corrupt_bit
    return bytes(bad_packet)
