import os.path
import sys

from collections import defaultdict

def is_ap(input_list):
    '''
    judge the input list whether is ap or not
    >>> is_ap([1,2,3,4,5])
    True
    >>> is_ap([1,3,4,5])
    False
    '''
    compute_list = [i for i in input_list]
    for i in range(0, len(compute_list) - 2):
        if compute_list[i + 1] - compute_list[i] != compute_list[i + 2] - compute_list[i + 1]:
            return False
    return True

try:
    file_name = input('Please enter the name of the file you want to get data from: ')
    input_number = []
    with open(file_name) as file :
        for line in file:
            nb = line.split()
            for i in range(0, len(nb)):
                input_number.append(int(nb[i]))
    if len(input_number) < 2:
        raise ValueError
    for i in range(1, len(input_number)):
        if input_number[i] <= input_number[i - 1]:
            raise ValueError
        elif input_number[i - 1] <= 0:
            raise ValueError
except ValueError:
    print('Sorry, input file does not store valid data.')
    sys.exit()
except FileNotFoundError:
    print('Sorry, there is no such file.')
    sys.exit()

max_length = 0
current_length = 0
min_nb_rm = 0

ride_length = []
difference = 0
del_nb = []
nb_rm= 0
position = 0

# if the list is ap, then print the ride is perfect
if is_ap(input_number):
    max_length = len(input_number) - 1
    min_nb_rm = 0
    print('The ride is perfect!\n'
          'The longest good ride has a length of: {}\n'
          'The minimal number of pillars to remove to build a perfect ride from the rest is: {}'.format(max_length, min_nb_rm)
          )
else:
    for i in range(0, len(input_number) - 1):
        if difference != (input_number[i + 1] - input_number[i]):
            difference = input_number[i + 1] - input_number[i]
        else:
            continue
        for j in range(i + 2, len(input_number)):
            if input_number[j] - input_number[j - 1] != difference:
                break
            elif input_number[j] - input_number[j - 1] == difference:
                current_length += 1
        ride_length.append(current_length + 1)
        current_length = 0
# get the longest good ride in the list

    for g in range(0, len(input_number) - 1):       
        for i in range(0, len(input_number) - 1):
            difference = input_number[i + 1] - input_number[g]
            nb_rm = i
            position = i + 1
            for j in range(i + 2, len(input_number)):
                if (input_number[j] - input_number[position]) > difference:
                    nb_rm += (len(input_number) - j)
                    break
                elif (input_number[j] - input_number[position]) == difference:
                    position = j
                elif (input_number[j] - input_number[position]) < difference:
                    nb_rm += 1
            del_nb.append(nb_rm)
            nb_rm = 0

# time complexity is n ** 3
# use g to get first element in the ap, then i is the second element in the ap,
# then use j to find the other elements 

    print('The ride could be better...\n'
          'The longest good ride has a length of: {}\n'
          'The minimal number of pillars to remove to build a perfect ride from the rest is: {}'.format(max(ride_length), min(del_nb))
          )       
      
