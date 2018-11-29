'''
Writen by Li Xiao, z5139219
for COMP9331 ass1
language python3
'''

import sys
import socket
import packet
import random
import time 

try:
    receiverPort = int(sys.argv[1])
    file = sys.argv[2]
except Exception:
    print('the format of the input should be:')
    print('python[3] recevier.py receiver_port file.txt')
    sys.exit()

recevierSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recevierSocket.bind(('', receiverPort))

seq_num_begin = random.randint(0, 1024)

receiverLog = open('Receiver_log.txt', 'w')
receiverLog = open('Receiver_log.txt', 'a')
file_trans = open(file, 'w')
file_trans = open(file, 'a')

# three times handshake to establish the connection
message, address = recevierSocket.recvfrom(4096)
decode_message = packet.decodePacket(message)

start_time = time.time() * 1000

if decode_message.flags[1] and not decode_message.flags[0] and not decode_message.flags[2]:
    receiverLog.write('rcv  {:.3f} S   {} 0 {}\n'.format(packet.running_time(start_time), decode_message.seq, decode_message.ACK))
    response_packet = packet.Packet('SYNACK', seq_num_begin, decode_message.seq + 1, b'')
    recevierSocket.sendto(packet.encodePacket(response_packet), address)
    receiverLog.write('snd  {:.3f} SA  {} 0 {}\n'.format(packet.running_time(start_time), seq_num_begin, decode_message.seq + 1))

message, address = recevierSocket.recvfrom(4096)
decode_message = packet.decodePacket(message)

if decode_message.flags[0] and not decode_message.flags[1] and not decode_message.flags[2]:
    receiverLog.write('rcv  {:.3f} A   {} 0 {}\n'.format(packet.running_time(start_time), decode_message.seq, decode_message.ACK))
    latestACK = decode_message.ACK

# receive file from the sender

# some variables should write in the log file 
number_of_duplicate = 0
number_of_packet = 0

seq_exception = decode_message.seq
last_seq = -1

# buffer pool for storage the segment not in the right seqnumber order
buffer_pool = []
buffer_pool_copy = []

while True:
    buffer_pool_copy = list(buffer_pool)

    message, address = recevierSocket.recvfrom(4096)
    decode_message = packet.decodePacket(message)

    # receive FIN and file transmittion finished
    if decode_message.flags[2] and not decode_message.flags[0] and not decode_message.flags[1]:
        receiverLog.write('rcv  {:.3f} F   {} 0 {}\n'.format(packet.running_time(start_time), decode_message.seq, decode_message.ACK))
        break

    receiverLog.write('rcv  {:.3f} A   {} {} {}\n'.format(packet.running_time(start_time), decode_message.seq, len(decode_message.data), decode_message.ACK))
    # wrong order seqnumber so need to append the message to the buffer pool and response this message 
    if seq_exception != decode_message.seq: 
        if decode_message.seq == last_seq:
            number_of_duplicate += 1
        else:
            last_seq = decode_message.seq

        buffer_pool.append(decode_message)
        buffer_pool.sort(key = packet.getSeq)

        response_packet = packet.Packet('ACK', latestACK, seq_exception, b'')
        recevierSocket.sendto(packet.encodePacket(response_packet), address)
        receiverLog.write('snd  {:.3f} A   {} 0 {}\n'.format(packet.running_time(start_time), response_packet.seq, response_packet.ACK))

    # right order seqnumber then write the message into the file and response this message 
    else:
        if decode_message.seq == last_seq:
            number_of_duplicate += 1
        else:
            last_seq = decode_message.seq

        file_trans.write(decode_message.data.decode())
        number_of_packet += 1
        seq_exception += len(decode_message.data)

        for i in buffer_pool_copy:
            if i.seq == seq_exception:
                file_trans.write(i.data.decode())
                number_of_packet += 1
                seq_exception += len(i.data)
                buffer_pool.remove(i)

        response_packet = packet.Packet('ACK', latestACK, seq_exception, b'')
        recevierSocket.sendto(packet.encodePacket(response_packet), address)
        receiverLog.write('snd  {:.3f} A   {} 0 {}\n'.format(packet.running_time(start_time), response_packet.seq, response_packet.ACK))


# finish the connection
response_packet = packet.Packet('FINACK', latestACK, decode_message.seq + 1, b'')
recevierSocket.sendto(packet.encodePacket(response_packet), address)
receiverLog.write('snd  {:.3f} FA  {} 0 {}\n'.format(packet.running_time(start_time), response_packet.seq, response_packet.ACK))

message, address = recevierSocket.recvfrom(4096)
decode_message = packet.decodePacket(message)

if decode_message.flags[0] and not decode_message.flags[1] and not decode_message.flags[2]:
    receiverLog.write('rcv  {:.3f} A   {} 0 {}\n'.format(packet.running_time(start_time), decode_message.seq, decode_message.ACK))
    recevierSocket.close()

file_size = packet.get_file_size(file_trans)

receiverLog.write('Amount of (original) Data Received (in bytes): {}\n'.format(file_size))
receiverLog.write('Number of (original) Data Segments Received: {}\n'.format(number_of_packet))
receiverLog.write('Number of duplicate segments received (if any): {}\n'.format(number_of_duplicate))

file_trans.close()
receiverLog.close()
