'''
Writen by Li Xiao, z5139219
for COMP9331 ass1
language python3
'''

import sys
import random
import socket
import packet
import time 
import threading

try:
    receiverIP = sys.argv[1]
    receiverPort = int(sys.argv[2])
    file = sys.argv[3]
    MWS = int(sys.argv[4])
    MSS = int(sys.argv[5])
    timeout = float(sys.argv[6])
    pdrop = float(sys.argv[7])
    seed = int(sys.argv[8])
    if len(sys.argv) != 9:
        raise Exception
except Exception:
    print('the format of the input should be:')
    print('python3 sender.py receiver_host_ip receiver_port file.txt MWS MSS timeout pdrop(between 0 ~ 1) seed')
    sys.exit()

# start time for the transmission
startTime = time.time() * 1000

# set up the connection depend on UDP
senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
senderSocket.bind(('', senderSocket.getsockname()[1]))

# file named Sender_log.txt to record the log information
senderLog = open('Sender_log.txt', 'w')
senderLog = open('Sender_log.txt', 'a')

seq_num_begin = random.randint(0, 1024)

# this function simulate the PLD model
random.seed(seed)
def PLD(ratio):
    num = random.random()
    if num > ratio:
        return True
    else:
        return False

# packtype (flag, sequence_num, ack, data)

# three times handshake to establish the connection
# send SYN
conn_packet = packet.Packet('SYN', seq_num_begin, 0, b'')
senderSocket.sendto(packet.encodePacket(conn_packet), (receiverIP, receiverPort))
senderLog.write('snd  {:.3f} S   {} 0  0\n'.format(packet.running_time(startTime), seq_num_begin))

# receive SYNACK
message, address = senderSocket.recvfrom(4096)
packetReceived_decode = packet.decodePacket(message)

# send ACK
if packetReceived_decode.flags[0] and packetReceived_decode.flags[1] and not packetReceived_decode.flags[2]:
    senderLog.write('rcv  {:.3f} SA  {} 0 {}\n'.format(packet.running_time(startTime), packetReceived_decode.seq, packetReceived_decode.ACK))
    
    packet_ACK = packetReceived_decode.seq + 1

    conn_packet = packet.Packet('ACK', seq_num_begin + 1, packetReceived_decode.seq + 1, b'')
    senderSocket.sendto(packet.encodePacket(conn_packet), (receiverIP, receiverPort))
    senderLog.write('snd  {:.3f} A   {} 0  {}\n'.format(packet.running_time(startTime), conn_packet.seq, conn_packet.ACK))

# transmit file

# Using this function to know the length of the file which should be transmitted
file_trans = open(file, 'rb')
size_of_file = packet.get_file_size(file_trans)

# bound a timer to caculate the timeout function 
# get this method from the tutor
timeout_check = [False]
timeout_check_start_or_not = False
timer = threading.Timer(float(timeout / 1000), packet.timerUse, args = [timeout_check])

# define some variables to support caculate
current_window_size = 0
end_of_file = False
start_read = seq_num_begin + 1
next_read = start_read
record_read = start_read
latestACK = start_read


# some variables should write in the log file 
number_of_packet_sent = 0
number_of_packet_droped = 0
number_of_retransmit = 0
number_of_duplicate = 0
current_duplicate_num = 0

while True:

    # read the file and then send this part of file until the windows is full 
    while current_window_size < MWS and end_of_file == False:
        file_trans.seek(next_read - start_read)
        contents = file_trans.read(MSS)

        if current_window_size + len(contents) > MWS or contents == b'':
            if contents == b'':
                end_of_file = True
            break

        contents_packet = packet.Packet('ACK', next_read, packet_ACK, contents)
        encode_contents_packet = packet.encodePacket(contents_packet)

        # when want to send a packer start the timer to caculate the runing time
        if not timeout_check_start_or_not:
            timer.start()
            timeout_check_start_or_not = True

        if PLD(pdrop):
            senderSocket.sendto(encode_contents_packet, (receiverIP, receiverPort))
            senderLog.write('snd  {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
            number_of_packet_sent += 1
        else:
            senderLog.write('drop {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
            number_of_packet_droped += 1
            number_of_packet_sent += 1

            current_window_size += len(contents)
        next_read += len(contents)
        

    # terminal condition for the transmittion loop
    if end_of_file and (record_read - start_read == size_of_file):
        break

    # if timeout occurs
    if timeout_check[0]:
        file_trans.seek(record_read - start_read)

        if PLD(pdrop):
            contents_packet = packet.Packet('ACK', record_read, packet_ACK, file_trans.read(MSS))
            senderSocket.sendto(packet.encodePacket(contents_packet), (receiverIP, receiverPort))
            senderLog.write('snd  {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
            number_of_retransmit += 1
        else:
            senderLog.write('drop {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
            number_of_packet_droped += 1
            number_of_retransmit += 1

        # because of the retransmission, restart the timer
        timer.cancel()
        timer = threading.Timer(float(timeout / 1000), packet.timerUse, args = [timeout_check])
        timer.start()
        timeout_check_start_or_not = True
        timeout_check[0] = False

    try:
        message, address = senderSocket.recvfrom(4096)
        decodePacket = packet.decodePacket(message)

        # receive ACK packet
        if decodePacket.flags[0] and not decodePacket.flags[1] and not decodePacket.flags[2]:
            senderLog.write('rcv  {:.3f} A   {} {} {}\n'.format(packet.running_time(startTime), decodePacket.seq, len(decodePacket.data), decodePacket.ACK))
            if decodePacket.ACK > record_read:
                record_read = decodePacket.ACK
                current_window_size = next_read - record_read
                current_duplicate_num = 0

                if record_read != next_read:
                    timer.cancel()
                    timer = threading.Timer(float(timeout / 1000), packet.timerUse, args = [timeout_check])
                    timer.start()
                    timeout_check_start_or_not = True
                    timeout_check[0] = False

            else:
                if decodePacket.ACK == latestACK:
                    current_duplicate_num += 1
                    number_of_duplicate += 1

                    # implement the fast retransmit 
                    if current_duplicate_num == 3:
                        current_duplicate_num = 0
                        file_trans.seek(decodePacket.ACK - start_read)

                        if PLD(pdrop):
                            contents_packet = packet.Packet('ACK', decodePacket.ACK, packet_ACK, file_trans.read(MSS))
                            senderSocket.sendto(packet.encodePacket(contents_packet), (receiverIP, receiverPort))
                            senderLog.write('snd  {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
                            number_of_retransmit += 1
                        else:
                            senderLog.write('drop {:.3f} D   {} {} {}\n'.format(packet.running_time(startTime), contents_packet.seq, len(contents_packet.data), contents_packet.ACK))
                            number_of_packet_droped += 1
                            number_of_retransmit += 1
                else:
                    current_duplicate_num = 0

            latestACK = decodePacket.ACK
    except Exception:
        pass

# finish the connection
closePacket = packet.Packet('FIN', next_read, packet_ACK, b'')
senderSocket.sendto(packet.encodePacket(closePacket), (receiverIP, receiverPort))
senderLog.write('snd  {:.3f} F   {} 0 {}\n'.format(packet.running_time(startTime), closePacket.seq, closePacket.ACK))

message, address = senderSocket.recvfrom(4096)
closePacket_received = packet.decodePacket(message)

if closePacket_received.flags[0] and closePacket_received.flags[2]:
    senderLog.write('rcv  {:.3f} FA  {} 0 {}\n'.format(packet.running_time(startTime), closePacket_received.seq, closePacket_received.ACK))
    
    finalAckPacket = packet.Packet('ACK', closePacket_received.ACK, packet_ACK + 1, b'')
    senderSocket.sendto(packet.encodePacket(finalAckPacket), (receiverIP, receiverPort))

    senderLog.write('snd  {:.3f} A   {} 0 {}\n'.format(packet.running_time(startTime), finalAckPacket.seq, finalAckPacket.ACK))

senderSocket.close()
file_trans.close()

senderLog.write('Amount of (original) Data Transferred (in bytes): {}\n'.format(size_of_file))
senderLog.write('Number of Data Segments Sent (excluding retransmissions): {}\n'.format(number_of_packet_sent))
senderLog.write('Number of (all) Packets Dropped (by the PLD module): {}\n'.format(number_of_packet_droped))
senderLog.write('Number of Retransmitted Segments: {}\n'.format(number_of_retransmit))
senderLog.write('Number of Duplicate Acknowledgements received: {}\n'.format(number_of_duplicate))

senderLog.close()
