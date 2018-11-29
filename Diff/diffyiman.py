import re
import itertools

class DiffCommands:
    def __init__(self, file = None):
        self.file = file
        self.diffcommands = []
        self.left = [[0]]
        self.action = ['*']
        self.right = [[0]]
        if file is None:
            return
        with open(file) as file:
            for line in file:
                self.diffcommands.append(line)
                get_info = re.match('^(\d+(?:,\d+)?)([acd])(\d+(?:,\d+)?)$', line)
                if get_info:
                    self.left.append([int(i) for i in get_info.groups()[0].split(',')])
                    self.action.append(get_info.groups()[1])
                    self.right.append([int(i) for i in get_info.groups()[2].split(',')])
                else:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')

        for i in range(1, len(self.action)):
            if self.action[i] == 'a':
                if len(self.left[i]) != 1:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                else:
                    if self.left[i][0] - self.left[i - 1][-1] != self.right[i][0] - 1 - self.right[i - 1][-1]:
                        raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            if self.action[i] == 'c':
                if self.left[i - 1][-1] + 1 >= self.left[i][0]:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                else:
                    if self.left[i][0] - self.left[i - 1][-1] != self.right[i][0] - self.right[i - 1][-1]:
                        raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            if self.action[i] == 'd':
                if len(self.right[i]) != 1:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                else:
                    if self.left[i][0] - 1 - self.left[i - 1][-1] != self.right[i][0] - self.right[i - 1][-1]:
                        raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            
    def __str__(self):
        return (''.join(self.diffcommands)).strip()

class DiffCommandsError(Exception):
    def __init__(self, message):
        self.message = message

class OriginalNewFiles:
    def __init__(self, file1 = None, file2 = None):
        self.file1 = file1
        self.file2 = file2
        if not file1 or not file2:
            return
        self.contents1 = []
        self.contents2 = []
        with open(file1) as file:
            for line in file:
                self.contents1.append(line)
        with open(file2) as file:
            for line in file:
                self.contents2.append(line)

    def is_a_possible_diff(self, diffs):
        solutions = self.get_all_diff_commands()
        L = [solutions[i].diffcommands for i in range(len(solutions))]
        print(diffs.diffcommands)
        print(L)
        if diffs.diffcommands in [solutions[i].diffcommands for i in range(len(solutions))]:
            return True
        return False
    def output_diff(self, diffs):
        if not self.is_a_possible_diff(diffs):
            return
        for i in range(1, len(diffs.action)):
            print(diffs.diffcommands[i - 1], end = '')
            if diffs.action[i] == 'a':
                for j in range(diffs.right[i][0] - 1, diffs.right[i][-1]):
                    print('> ' + self.contents2[j], end = '')
            elif diffs.action[i] == 'c':
                for j in range(diffs.left[i][0] - 1, diffs.left[i][-1]):
                    print('< ' + self.contents1[j], end = '')
                print('---')
                for j in range(diffs.right[i][0] - 1, diffs.right[i][-1]):
                    print('> ' + self.contents2[j], end = '')
            elif diffs.action[i] == 'd':
                for j in range(diffs.left[i][0] - 1, diffs.left[i][-1]):
                    print('< ' + self.contents1[j], end = '')
        return
                
    def output_unmodified_from_original(self, diffs):
        if not self.is_a_possible_diff(diffs):
            return
        output_contents1 = []
        for line in self.contents1:
            output_contents1.append('...')

        for i in range(1, len(diffs.action)):
            if diffs.action[i] == 'a':
               output_contents1[diffs.left[i - 1][-1] : diffs.left[i][0]] = self.contents1[diffs.left[i - 1][-1] : diffs.left[i][0]]
            elif diffs.action[i] == 'c':
               output_contents1[diffs.left[i - 1][-1] : diffs.left[i][0] - 1] = self.contents1[diffs.left[i - 1][-1] : diffs.left[i][0] - 1]                
            elif diffs.action[i] == 'd':
               output_contents1[diffs.left[i - 1][-1] : diffs.left[i][0] - 1] = self.contents1[diffs.left[i - 1][-1] : diffs.left[i][0] - 1]

        if len(self.contents1) > diffs.left[-1][-1]:
            for i in range(diffs.left[-1][-1], len(self.contents1)):
                output_contents1[i] = self.contents1[i]
        output_contents1.insert(0, '*')
        print(output_contents1)
        for i in range(1, len(output_contents1)):
            if output_contents1[i] == '...' and output_contents1[i - 1] != '...':
                print('...')
            elif output_contents1[i] != '...':
                print(output_contents1[i], end = '')
        return 
    def output_unmodified_from_new(self, diffs):
        if not self.is_a_possible_diff(diffs):
            return
        
        output_contents2 = []
        for line in self.contents2:
            output_contents2.append(line)
            
        for i in range(1, len(diffs.action)):
            if diffs.action[i] == 'a':
                start = diffs.right[i][0] - 1
                end = diffs.right[i][-1]
            elif diffs.action[i] == 'c':
                start = diffs.right[i][0] - 1
                end = diffs.right[i][-1]
            else:
                continue
            if start == end:
                output_contents2[start] = '...'
            else:
                output_contents2[start : end] = ['...'] * (end - start)
            
        output_contents2.insert(0, '*')
        print(output_contents2)
        for i in range(1, len(output_contents2)):
            if output_contents2[i] == '...' and output_contents2[i - 1] != '...':
                print('...')
            elif output_contents2[i] != '...':
                print(output_contents2[i], end = '')
        return
    
    def get_all_diff_commands(self):
        if self.contents1 == self.contents2:
            return [DiffCommands()]
        lcs_table = []
        for i in range(len(self.contents1) + 1):
            lcs_table.append([0 for _ in range(len(self.contents2) + 1)])

        
        same_commands = []
        for i in range(1, len(lcs_table)):
            for j in range(1, len(lcs_table[i])):
                if self.contents1[i - 1] == self.contents2[j - 1]:
                    lcs_table[i][j]  = lcs_table[i - 1][j - 1] + 1
                    same_commands.append([i, j, lcs_table[i][j]])
                else:
                    lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])
        for i in range(len(lcs_table)):
            for j in range(len(lcs_table[i])):
                print(lcs_table[i][j], end = '')
            print()

        print(same_commands)
        max_index_number = same_commands[-1][-1]
        diffs = list(itertools.combinations(same_commands, max_index_number))
        remove_position = []
        for i in range(len(diffs)):
            if diffs[i][0][2] != 1 or diffs[i][-1][2] != max_index_number:
                remove_position.append(i)
                continue
            for j in range(1, len(diffs[i]) - 1):
                if diffs[i][j][2] != diffs[i][j - 1][2] + 1 or \
                   diffs[i][j][0] <= diffs[i][j - 1][0] or \
                   diffs[i][j][1] <= diffs[i][j - 1][1]:
                    remove_position.append(i)
                    break
        remove_position = sorted(remove_position, reverse = True)
        for index in remove_position:
            diffs.pop(index)
        
        solutions = []
        for diff in diffs:
            solution = DiffCommands()
            diff_left = [0] + [diff[i][0] for i in range(len(diff))] + [len(self.contents1) + 1]
            diff_right = [0] + [diff[i][1] for i in range(len(diff))] + [len(self.contents2) + 1]
            for i in range(1, len(diff_left)):
                if diff_left[i] > diff_left[i - 1] + 1 and diff_right[i] == diff_right[i - 1] + 1:
                    if diff_left[i] - diff_left[i - 1] > 2:
                        solution.diffcommands.append('{},{}d{}\n'.format(diff_left[i - 1] + 1, diff_left[i] - 1, diff_right[i] - 1))
                    else:
                        solution.diffcommands.append('{}d{}\n'.format(diff_left[i] - 1, diff_right[i] - 1))
                if diff_left[i] == diff_left[i - 1] + 1 and diff_right[i] > diff_right[i - 1] + 1:
                    if diff_right[i] - diff_right[i - 1] > 2:
                        solution.diffcommands.append('{}a{},{}\n'.format(diff_left[i] - 1, diff_right[i - 1] + 1, diff_right[i] - 1))
                    else:
                        solution.diffcommands.append('{}a{}\n'.format(diff_left[i] - 1, diff_right[i] - 1))
                if diff_left[i] > diff_left[i - 1] + 1 and diff_right[i] > diff_right[i - 1] + 1:
                    if diff_left[i] > diff_left[i - 1] + 2 and diff_right[i] > diff_right[i - 1] + 2:
                        solution.diffcommands.append('{},{}c{},{}\n'.format(diff_left[i - 1] + 1, diff_left[i] - 1, diff_right[i - 1] + 1, diff_right[i] - 1))
                    elif diff_left[i] == diff_left[i - 1] + 2 and diff_right[i] > diff_right[i - 1] + 2:
                        solution.diffcommands.append('{}c{},{}\n'.format(diff_left[i] - 1, diff_right[i - 1] + 1,diff_right[i] - 1))
                    elif diff_left[i] > diff_left[i - 1] + 2 and diff_right[i] == diff_right[i - 1] + 2:
                        solution.diffcommands.append('{},{}c{}\n'.format(diff_left[i - 1] + 1, diff_left[i] - 1, diff_right[i] - 1))
                    else:
                        solution.diffcommands.append('{}c{}\n'.format(diff_left[i] - 1, diff_right[i] - 1))
            solutions.append(solution)
        solutions = sorted(solutions, key = lambda x : x.diffcommands)
        return solutions
                        
                        
            
        

        

        
        
                


        
diff1 = DiffCommands('diff_1.txt')
diff2 = DiffCommands('diff_2.txt')
diff3 = DiffCommands('diff_3.txt')

p1 = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
p2 = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
p3 = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')
##
##print(p1.is_a_possible_diff(diff1))
##print(p1.is_a_possible_diff(diff2))
##print(p1.is_a_possible_diff(diff3))
##print()
##print(p2.is_a_possible_diff(diff1))
##print(p2.is_a_possible_diff(diff2))
##print(p2.is_a_possible_diff(diff3))
##print()
##print(p3.is_a_possible_diff(diff1))
##print(p3.is_a_possible_diff(diff2))
##print(p3.is_a_possible_diff(diff3))

##print('1')
##print(diff1)
##print('2')
##print(diff2)
##print('3')
##print(diff3)

##print('1')
##p1.output_diff(diff1)
##print()
##print('2')
##p2.output_diff(diff2)
##print()
##print('3')
##p3.output_diff(diff3)

##print('1')
##p1.output_unmodified_from_original(diff1)
##print()
##print('2')
##p2.output_unmodified_from_original(diff2)
##print()
##print('3')
##p3.output_unmodified_from_original(diff3)

##print('1')
##p1.output_unmodified_from_new(diff1)
##print()
##print('2')
##p2.output_unmodified_from_new(diff2)
##print()
##print('3')
##p3.output_unmodified_from_new(diff3)

print('1')
diffs1 = p1.get_all_diff_commands()
print(len(diffs1))
for i in range(len(diffs1)):
    print(diffs1[i])
    print()
print('2')
diffs2 = p2.get_all_diff_commands()
print(len(diffs2))
for i in range(len(diffs2)):
    print(diffs2[i])
    print()
print('3')
diffs3 = p3.get_all_diff_commands()
print(len(diffs3))
for i in range(len(diffs3)):
    print(diffs3[i])
    print()
