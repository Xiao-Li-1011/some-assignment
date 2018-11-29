'''
    Writen by :
        Xiao Li (z5139219)
        Man Yi (z5045205)
    FOR COMP9331 17s2 assignment 2
    LANGUAGE: python3
'''

import sys
import random

class Link:
    def __init__(self, delay = -1, capacity = -1, hop = 1, current_capacity = 0):
        # should not be changed
        self.delay = delay
        self.hop = hop
        # could be changed 
        self.capacity = capacity
        self.current_capacity = current_capacity

try:
    if len(sys.argv) != 6:
        raise Exception

    NETWORK_SCHEME = sys.argv[1]  # CIRCUIT or PACKET
    if NETWORK_SCHEME not in ['CIRCUIT', 'PACKET']:
        raise Exception
    ROUTING_SCHEME = sys.argv[2]  # SHP, SDP or LLP
    if ROUTING_SCHEME not in ['SHP', 'SDP', 'LLP']:
        raise Exception
    TOPOLOGY_FILE = sys.argv[3]  # topology file name 
    WORKLOAD_FILE = sys.argv[4]  # workload file name
    PACKET_RATE = int(sys.argv[5])  # packets/second

except Exception:
    print('Command should be: python3 RoutingPerformance.py [NETWORK_SCHEME] [ROUTING_SCHEME] [TOPOLOGY_FILE] [WORKLOAD_FILE] [PACKET_RATE]')
    sys.exit()


graph = [[False for _ in range(26)] for _ in range(26)]
letterA = ord('A')

# topology file each line type:
# node, node, one-way propagation delay, capacity

with open(TOPOLOGY_FILE) as tf:
    for line in tf:
        nodeA, nodeB, delay, capacity = line.split()
        link = Link(delay = int(delay), capacity = int(capacity))
        graph[ord(nodeA) - letterA][ord(nodeB) - letterA] = link
        graph[ord(nodeB) - letterA][ord(nodeA) - letterA] = link

actions = []  # each element's format: [nodefrom, nodeto, starttime, endtime, duration] 

# workload file each line type:
# starttime, nodefrom, nodeto, duration

with open(WORKLOAD_FILE) as wf:
    for line in wf:
        starttime, nodeA, nodeB, duration = line.split()
        actions.append([nodeA, nodeB, float(starttime), float(starttime) + float(duration), float(duration)])

action_order = []  # each element's format: [nodefrom, nodeto, time, flag(0 is start, 1 is end), number of circuits, number of packets] 
if NETWORK_SCHEME == 'CIRCUIT':
    for i in range(len(actions)):
        action_order.append([actions[i][0], actions[i][1], actions[i][2], 0, i, int(PACKET_RATE * actions[i][-1])])
        action_order.append([actions[i][0], actions[i][1], actions[i][3], 1, i, int(PACKET_RATE * actions[i][-1])])

    # sorted by the time 

    action_order = sorted(action_order, key = lambda action_order : action_order[2])

else:  # NETWORK_SCHEME = 'PACKET'
    num = 0
    for i in range(len(actions)):
        for j in range(int(PACKET_RATE * actions[i][-1])):
            action_order.append([actions[i][0], actions[i][1], actions[i][2] + j * (1 / 3), 0, num, 1])
            action_order.append([actions[i][0], actions[i][1], actions[i][2] + (j + 1) * (1 / 3), 1, num, 1])
            num += 1

    action_order = sorted(action_order, key = lambda action_order : action_order[2])

def get_paths(pred, node):
        if not pred[node]:
            return [[node]]
        paths = []
        for pred_node in pred[node]:
            for pred_path in get_paths(pred, pred_node):
                paths.append(pred_path + [node])
        return paths


def Dijkstra(nodeFrom, nodeTo, graph, routing_scheme):
    letterA = ord('A')

    nodefrom = ord(nodeFrom) - letterA
    nodeto = ord(nodeTo) - letterA

    # two arrays to save the distance to the source and last node 
    distance = [float('inf') for _ in range(26)]
    distance[nodefrom] = 0
    last = [[] for _ in range(26)]

    record_compute_node = [nodefrom]
    queue_extend_node = [nodefrom]

    if routing_scheme == 'SHP':  # hop 
        while queue_extend_node:
            compute_node_dis = float('inf')
            for i in range(len(queue_extend_node)):
                if compute_node_dis > distance[queue_extend_node[i]]:
                    compute_node_dis = distance[queue_extend_node[i]]
                    compute_node_index = i

            compute_node = queue_extend_node.pop(compute_node_index)
            record_compute_node.append(compute_node)
            for i in range(26):
                if graph[compute_node][i]:
                    if i in record_compute_node:
                        continue
                    queue_extend_node.append(i)
                    if distance[compute_node] + graph[compute_node][i].hop <= distance[i]:
                        distance[i] = distance[compute_node] + graph[compute_node][i].hop
                        last[i].append(compute_node)
    elif routing_scheme == 'SDP':  # delay
        while queue_extend_node:
            compute_node_dis = float('inf')
            for i in range(len(queue_extend_node)):
                if compute_node_dis > distance[queue_extend_node[i]]:
                    compute_node_dis = distance[queue_extend_node[i]]
                    compute_node_index = i

            compute_node = queue_extend_node.pop(compute_node_index)
            record_compute_node.append(compute_node)
            for i in range(26):
                if graph[compute_node][i]:
                    if i in record_compute_node:
                        continue
                    queue_extend_node.append(i)
                    if distance[compute_node] + graph[compute_node][i].delay <= distance[i]:
                        distance[i] = distance[compute_node] + graph[compute_node][i].delay
                        last[i].append(compute_node)
    elif routing_scheme == 'LLP':  # capacity
        while queue_extend_node:
            compute_node_dis = float('inf')
            for i in range(len(queue_extend_node)):
                if compute_node_dis > distance[queue_extend_node[i]]:
                    compute_node_dis = distance[queue_extend_node[i]]
                    compute_node_index = i

            compute_node = queue_extend_node.pop(compute_node_index)
            record_compute_node.append(compute_node)
            for i in range(26):
                if graph[compute_node][i]:
                    if i in record_compute_node:
                        continue
                    queue_extend_node.append(i)
                    if distance[compute_node] + graph[compute_node][i].current_capacity <= distance[i]:
                        distance[i] = distance[compute_node] + graph[compute_node][i].current_capacity / graph[compute_node][i].capacity 
                        last[i].append(compute_node)


    # last[node][unknow] array to output
    paths = []

    for i in range(len(last)):
        last[i] = list(set(last[i]))
    paths = get_paths(last, nodeto)

    # return [random.choice(paths)]
    return paths

# action_order format: [nodefrom, nodeto, time, flag(0 is start, 1 is end), number of circuits, number of packets]

number_of_request = 0
total_number_of_packet = 0
successful_number_of_packet = 0
blocked_number_of_packet = 0
total_number_of_hop = 0
total_propagation_delay = 0

block_or_not = []
blocked = 0

if NETWORK_SCHEME == 'CIRCUIT':
    path_pool = [False for _ in range(len(actions))]

    for action in action_order:

        if action[3] == 0:  # start flag = 0

            number_of_request += 1
            total_number_of_packet += action[-1]

            possible_circuit = Dijkstra(action[0], action[1], graph, ROUTING_SCHEME)
            block_or_not = [0 for _ in range(len(possible_circuit))]

            for i in range(0, len(possible_circuit)):
                for j in range(len(possible_circuit[i]) - 1):
                    if graph[possible_circuit[i][j]][possible_circuit[i][j + 1]].current_capacity == graph[possible_circuit[i][j]][possible_circuit[i][j + 1]].capacity:
                        block_or_not[i] = 1


            # circuit = possible_circuit[-1]
            # blocked = block_or_not[-1]
            # for i in range(len(block_or_not) - 1, -1, -1):
            #     if block_or_not[i] == 0:
            #         circuit = possible_circuit[i]
            #         blocked = block_or_not[i]

            # if ROUTING_SCHEME == 'SDP':
            #     circuit = possible_circuit[-1]
            #     blocked = block_or_not[-1]

            index = random.randint(0, len(possible_circuit) - 1)
            circuit = possible_circuit[index]
            blocked = block_or_not[index]

            total_number_of_hop += len(circuit) - 1

            for i in range(len(circuit) - 1):
                total_propagation_delay += graph[circuit[i]][circuit[i + 1]].delay

            if not blocked:
                successful_number_of_packet += action[-1]
                for i in range(len(circuit) - 1):
                    graph[circuit[i]][circuit[i + 1]].current_capacity += 1
                path_pool[action[4]] = circuit
            else:
                blocked_number_of_packet += action[-1]
                

        elif action[3] == 1:  # stop flag = 1
            if path_pool[action[4]]:
                for i in range(len(path_pool[action[4]]) - 1):
                    graph[path_pool[action[4]][i]][path_pool[action[4]][i + 1]].current_capacity -= 1

    print('total number of virtual connection requests: {}'.format(number_of_request))
    print('total number of packets: {}'.format(total_number_of_packet))
    print('number of successfully routed packets: {}'.format(successful_number_of_packet))
    print('percentage of successfully routed packets: {:.2f}'.format(successful_number_of_packet / total_number_of_packet * 100))
    print('number of blocked packets: {}'.format(blocked_number_of_packet))
    print('percentage of blocked packets: {:.2f}'.format(blocked_number_of_packet / total_number_of_packet * 100))
    print('average number of hops per circuit: {:.2f}'.format(total_number_of_hop / number_of_request))
    print('average cumulative propagation delay per circuit: {:.2f}'.format(total_propagation_delay / number_of_request))

else:  # NETWORK_SCHEME = 'CIRCUIT'
    path_pool = [False for _ in range(num + 1)]

    number_of_request = len(actions)
    for i in range(len(actions)):
        total_number_of_packet += int(PACKET_RATE * actions[i][-1])

    for action in action_order:
        if action[3] == 0:

            possible_circuit = Dijkstra(action[0], action[1], graph, ROUTING_SCHEME)     
            block_or_not = [0 for _ in range(len(possible_circuit))]

            for i in range(0, len(possible_circuit)):
                for j in range(len(possible_circuit[i]) - 1):
                    if graph[possible_circuit[i][j]][possible_circuit[i][j + 1]].current_capacity == graph[possible_circuit[i][j]][possible_circuit[i][j + 1]].capacity:
                        block_or_not[i] = 1

            index = random.randint(0, len(possible_circuit) - 1)
            circuit = possible_circuit[index]
            blocked = block_or_not[index]

            total_number_of_hop += len(circuit) - 1

            for i in range(len(circuit) - 1):
                total_propagation_delay += graph[circuit[i]][circuit[i + 1]].delay

            if not blocked:
                successful_number_of_packet += action[-1]
                for i in range(len(circuit) - 1):
                    graph[circuit[i]][circuit[i + 1]].current_capacity += 1
                path_pool[action[4]] = circuit
            else:
                blocked_number_of_packet += action[-1]
        elif action[3] == 1:
            if path_pool[action[4]]:
                for i in range(len(path_pool[action[4]]) - 1):
                    graph[path_pool[action[4]][i]][path_pool[action[4]][i + 1]].current_capacity -= 1


    print('total number of virtual connection requests: {}'.format(number_of_request))
    print('total number of packets: {}'.format(total_number_of_packet))
    print('number of successfully routed packets: {}'.format(successful_number_of_packet))
    print('percentage of successfully routed packets: {:.2f}'.format(successful_number_of_packet / total_number_of_packet * 100))
    print('number of blocked packets: {}'.format(blocked_number_of_packet))
    print('percentage of blocked packets: {:.2f}'.format(blocked_number_of_packet / total_number_of_packet * 100))
    print('average number of hops per circuit: {:.2f}'.format(total_number_of_hop / total_number_of_packet))
    print('average cumulative propagation delay per circuit: {:.2f}'.format(total_propagation_delay / total_number_of_packet))
