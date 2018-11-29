'''
Writen by Li Xiao, z5139219
for COMP9331 ass1
language python3
'''

import struct
import time 

# packet type
class Packet:
    def __init__(self, flag, sequence, acknowledgement, data):
        self.seq = sequence
        self.ACK = acknowledgement
        self.flags = [False, False, False]
        # 0: ACK 1: SYN 2: FIN
        self.data = data

        if flag == 'ACK':
            self.flags[0] = True
        if flag == 'SYN':
            self.flags[1] = True
        if flag == 'FIN':
            self.flags[2] = True
        if flag == 'SYNACK':
            self.flags[0] = True
            self.flags[1] = True
        if flag == 'FINACK':
            self.flags[0] = True
            self.flags[2] = True

def encodePacket(packet):
    return struct.pack('ii???', packet.seq, packet.ACK, packet.flags[0], \
        packet.flags[1], packet.flags[2]) + packet.data

def decodePacket(packet):
    segment_list = list(struct.unpack('ii???', packet[0 : struct.calcsize('ii???')]))
    segment_list.append(packet[struct.calcsize('ii???') : ])
    flag = ''
    if segment_list[2]:
        flag = 'ACK'
    if segment_list[3]:
        flag = 'SYN'
    if segment_list[4]:
        flag = 'FIN'
    if segment_list[2] and segment_list[3]:
        flag = 'SYNACK'
    if segment_list[2] and segment_list[4]:
        flag = 'FINACK'
    decodeP = Packet(flag, segment_list[0], segment_list[1], segment_list[5])
    return decodeP

# support function

# support function for sorting the buffer pool 
def getSeq(packet):
    return packet.seq

# support function for timer
def timerUse(timeout_check):
    timeout_check[0] = True

# support function for computing the running time 
def running_time(start_time):
    return (time.time() * 1000 - start_time)

# support function for computing the file size
def get_file_size(file):
    file.seek(0, 2)
    return file.tell()








