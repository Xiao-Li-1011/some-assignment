import sys


def same_hero_n_times(input_number, nb_of_swiches):
    '''
    sort the input list, then switch the number from the least one while
    all the elements in the list switches to positive numbers if also have
    nb_of_switches, then switch the least positive number
    >>> same_hero_n_times([-7,1,2,3,4], 5)
    17
    >>> same_hero_n_times([4,-3,1,2,-7], 3)
    15
    >>> same_hero_n_times([1,2,3,4,5], 2)
    15
    '''
    output_number = [i for i in input_number]
    output_number.sort()
    for i in range(0, len(output_number)):
        if output_number[i] < 0:
            output_number[i] = output_number[i] - output_number[i] * 2
            nb_of_swiches -= 1
        if nb_of_swiches == 0:
            break
    if nb_of_swiches == 0:
        return sum(output_number)
    elif nb_of_swiches != 0:
        if nb_of_swiches % 2 == 0:
            return sum(output_number)
        elif nb_of_swiches % 2 != 0:
            return sum(output_number) - min(output_number) * 2

def hero_once(input_number, nb_of_swiches):
    '''
    sort the input list, then switch the elements in the list from the
    least one
    >>> hero_once([-7,1,2,3,4], 5)
    -3
    >>> hero_once([4,-3,1,2,-7], 3)
    15
    >>> hero_once([1,2,3,4,5], 2)
    9
    '''
    output_number = [i for i in input_number]
    output_number.sort()
    for i in range(0, len(output_number)):
        output_number[i] = output_number[i] - output_number[i] * 2
        nb_of_swiches -= 1
        if nb_of_swiches == 0:
            return sum(output_number)
            break

def consecutive_hero_once(input_number, nb_of_swiches):
    '''
    i to confirm the position and j for read the numbers in
    range(nb_of_swiches), then find the least sum of all sum
    switch them and get the result
    >>> consecutive_hero_once([-7,1,2,3,4], 5)
    -3
    >>> consecutive_hero_once([4,-3,1,2,-7], 3)
    5
    >>> consecutive_hero_once([1,2,3,4,5], 2)
    9
    '''
    output_number = [i for i in input_number]
    sum_number = []
    nb_of_swiches_sum = []
    for i in range(0, len(output_number) - nb_of_swiches + 1):
        for j in range(0, nb_of_swiches):
            nb_of_swiches_sum.append(output_number[i + j])
        sum_number.append(sum(nb_of_swiches_sum))
        nb_of_swiches_sum = []
    return (sum(output_number) - min(sum_number) * 2)

def consecutive_hero_max(input_number):
    '''
    need to consider switching nothing, then use for in for to find
    the largest sum of switched list
    >>> consecutive_hero_once([-7,1,2,3,4], 5)
    17
    >>> consecutive_hero_once([4,-3,1,2,-7], 3)
    11
    >>> consecutive_hero_once([1,2,3,4,5], 2)
    15
    '''
    output_number = [i for i in input_number]
    Sum_number = []
    Sum_number.append(sum(output_number))
    for i in range(1,len(output_number) + 1):
        for j in range(0, len(output_number) - i + 1):
            Sum_number.append(sum(output_number) - sum(output_number[j : j + i] * 2))
    return max(Sum_number)

try:
    input_number = input("Please input the heroes' powers: ").split(' ')
    input_number = [int(i) for i in input_number if i != '']
##    for i in range(0, len(input_number) - 1):
##        if input_number[i] == 0:
##            raise ValueError
except ValueError:
    print('Sorry, these are not valid power values.')
    sys.exit()

try:
    nb_of_swiches = int(input('Please input the number of power flips: '))
    if nb_of_swiches > len(input_number):
        raise ValueError
    if nb_of_swiches < 0:
        raise ValueError
except ValueError:
    print('Sorry, this is not a valid number of power flips.')
    sys.exit()

if nb_of_swiches == 0:
# mean switch nothing
    print('Possibly flipping the power of the same hero many times, the greatest achievable power is {}.\n'
          'Flipping the power of the same hero at most once, the greatest achievable power is {}.\n'
          'Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {}.\n'
          'Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is {}.'.format(sum(input_number), sum(input_number), sum(input_number), consecutive_hero_max(input_number))
          )
else:
    print('Possibly flipping the power of the same hero many times, the greatest achievable power is {}.\n'
          'Flipping the power of the same hero at most once, the greatest achievable power is {}.\n'
          'Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is {}.\n'
          'Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is {}.'.format(same_hero_n_times(input_number, nb_of_swiches), hero_once(input_number, nb_of_swiches), consecutive_hero_once(input_number, nb_of_swiches), consecutive_hero_max(input_number))
          )
