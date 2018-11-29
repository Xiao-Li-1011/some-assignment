import os.path
import sys
from collections import deque

try:
    file_name = input('Please enter the name of the file you want to get data from: ')
    input_number = []
    ceiling_heights = []
    floor_heights = []
    with open(file_name) as file :
        for line in file:
            nb = line.split()
            for i in range(0, len(nb)):
                input_number.append(int(nb[i]))
    if len(input_number) < 4 or len(input_number) % 2 != 0:
        raise ValueError

# divide the input list into two lists with the same length
    for i in range(0, len(input_number)):
        if i < len(input_number) / 2:
            ceiling_heights.append(input_number[i])
        else:
            floor_heights.append(input_number[i])
    for i in range(0,len(ceiling_heights)):
        if ceiling_heights[i] <= floor_heights[i] or ceiling_heights[i] == 0 or floor_heights[i] == 0:
            raise ValueError
except ValueError:
    print('Sorry, input file does not store valid data.')
    sys.exit()
except FileNotFoundError:
    print('Sorry, there is no such file.')
    sys.exit()

max_length = 1
max_length_list = [0]
'''
i is the position in the ceiling_heights list and same position in the floor_heights list
from west we can see the longest length is ceiling_heights's smallest element > floor_heights's
largest element in the j positon

and the second result:
i++: also from west see the longest length
then the largest elements in the longest length is the result for second question
'''
for i in range(0, len(ceiling_heights)):
    high = ceiling_heights[i]
    low = floor_heights[i]
    for j in range(i + 1, len(ceiling_heights)):
        if ceiling_heights[j] > low and high > floor_heights[j]:
            max_length += 1
            if high > ceiling_heights[j]:
                high = ceiling_heights[j]
            if low < floor_heights[j]:
                low = floor_heights[j]
        else:
            break
    if max_length > max(max_length_list):
        max_length_list.append(max_length)
    if max_length == len(ceiling_heights) - i:
        break
    max_length = 1
    

print('From the west, one can into the tunnel over a distance of {}\n'
      'Inside the tunnel, one can into the tunnel over a maximum distance of {}'
      .format(max_length_list[1], max(max_length_list)))
