import re
import itertools

class DiffCommands:
    def __init__(self, filename = None):
        self.filename = filename
        self.contents = []
        self.info = [[[0], 'None', [0]]]
        if filename is None:
            return
        with open(filename) as file:
            for line in file:
                judge = re.match('^(\d+(?:,\d+)?)([acd])(\d+(?:,\d+)?)$', line)
                if judge:
                    left_number, action, right_number = judge.groups()
                    self.contents.append(line)
                    self.info.append([[int(i) for i in left_number.split(',')], action, [int(i) for i in right_number.split(',')]])
                    continue
                else:
                    raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                
        for i in range(1, len(self.info)):
            if (self.info[i][1] == 'd' and len(self.info[i][2]) != 1) or \
               (self.info[i][1] == 'a' and len(self.info[i][0]) != 1):
                raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            if self.info[i][1] == 'c' and self.info[i - 1][0][-1] + 1 >= self.info[i][0][0]:
                raise DiffCommandsError('Cannot possibly be the commands for the diff of two files3')
            
            if self.info[i][1] == 'a':
                diff_left = self.info[i][0][0] - self.info[i - 1][0][-1]
                diff_right = self.info[i][2][0] - 1 - self.info[i - 1][2][-1]
            elif self.info[i][1] == 'c':
                diff_left = self.info[i][0][0] - self.info[i - 1][0][-1]
                diff_right = self.info[i][2][0] - self.info[i - 1][2][-1]
            elif self.info[i][1] == 'd':
                diff_left = self.info[i][0][0] - 1 - self.info[i - 1][0][-1]
                diff_right = self.info[i][2][0] - self.info[i - 1][2][-1]
            else:
                continue
            if diff_left != diff_right:
                raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            
    def __str__(self):
        return (''.join(self.contents)).strip()

class DiffCommandsError(Exception):
    def __init__(self, message):
        self.message = message

class OriginalNewFiles:
    def __init__(self, filename1 = None, filename2 = None):
        self.filename1 = filename1
        self.filename2 = filename2
        if not filename1 or not filename2:
            return
        self.contents1 = []
        self.contents2 = []

        with open(filename1) as file:
            for line in file:
                self.contents1.append(line)
        with open(filename2) as file:
            for line in file:
                self.contents2.append(line)

    def is_a_possible_diff(self, diff_commands):
        # diff_commands.info
        for i in range(1, len(diff_commands.info)):
            if diff_commands.info[i][0][-1] > len(self.contents1) or \
               diff_commands.info[i][2][-1] > len(self.contents2):
                return False
            if diff_commands.info[i][1] == 'a':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1], diff_commands.info[i][0][0]
                diff_right_start, diff_right_end = diff_commands.info[i - 1][2][-1], diff_commands.info[i][2][0] - 1
            elif diff_commands.info[i][1] == 'c':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1] , diff_commands.info[i][0][0] - 1
                diff_right_start, diff_right_end = diff_commands.info[i - 1][2][-1], diff_commands.info[i][2][0] - 1
            elif diff_commands.info[i][1] == 'd':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1], diff_commands.info[i][0][0] - 1
                diff_right_start, diff_right_end = diff_commands.info[i - 1][2][-1], diff_commands.info[i][2][0]
            else:
                continue
            if self.contents1[diff_left_start : diff_left_end] != self.contents2[diff_right_start : diff_right_end]:
                return False
        return True

    def output_diff(self, diff_commands):
        # diff_commands.info
        # diff_commands.contents
        if not self.is_a_possible_diff(diff_commands):
            return
        for i in range(1, len(diff_commands.info)):
            print(diff_commands.contents[i - 1], end = '')
            if diff_commands.info[i][1] == 'a':
                for j in range(diff_commands.info[i][2][0] - 1, diff_commands.info[i][2][-1]):
                    print('> ', end = '')
                    print(self.contents2[j], end = '')
            elif diff_commands.info[i][1] == 'c':
                for j in range(diff_commands.info[i][0][0] - 1, diff_commands.info[i][0][-1]):
                    print('< ', end = '')
                    print(self.contents1[j], end = '')
                print('---')
                for j in range(diff_commands.info[i][2][0] - 1, diff_commands.info[i][2][-1]):
                    print('> ', end = '')
                    print(self.contents2[j], end = '')
            elif diff_commands.info[i][1] == 'd':
                for j in range(diff_commands.info[i][0][0] - 1, diff_commands.info[i][0][-1]):
                    print('< ', end = '')
                    print(self.contents1[j], end = '')
        return

    def output_unmodified_from_original(self, diff_commands):
        # diff_commands.info
        output_original = ['None']
        truth_table = []
        for line in self.contents1:
            output_original.append(line)
            truth_table.append(False)
        
        if not self.is_a_possible_diff(diff_commands):
            return
        if len(diff_commands.info) == 1:
            for line in self.contents1:
                print(line, end = '')
            return
        for i in range(1, len(diff_commands.info)):
            if diff_commands.info[i][1] == 'a':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1], diff_commands.info[i][0][0]
            elif diff_commands.info[i][1] == 'c':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1], diff_commands.info[i][0][0] - 1
            elif diff_commands.info[i][1] == 'd':
                diff_left_start, diff_left_end = diff_commands.info[i - 1][0][-1], diff_commands.info[i][0][0] - 1
            else:
                continue
            truth_table[diff_left_start : diff_left_end] = [True] * (diff_left_end - diff_left_start)
        if len(truth_table) > diff_commands.info[-1][0][-1]:
            for i in range(diff_commands.info[-1][0][-1], len(truth_table)):
                truth_table[i] = True
        truth_table.insert(0, True)
        for i in range(1, len(truth_table)):
            if truth_table[i] == True:
                print(output_original[i], end = '')
            elif truth_table[i] == False and truth_table[i - 1] == True:
                print('...')
        return 
            
    def output_unmodified_from_new(self, diff_commands):
        # diff_commands.info
        output_new = ['None']
        truth_table = []
        for line in self.contents2:
            output_new.append(line)
            truth_table.append(True)
        
        if not self.is_a_possible_diff(diff_commands):
            return
        if len(diff_commands.info) == 1:
            for line in self.contents2:
                print(line, end = '')
            return
        for i in range(1, len(diff_commands.info)):
            if diff_commands.info[i][1] == 'a':
                diff_right_start = diff_commands.info[i][2][0] - 1
                diff_right_end = diff_commands.info[i][2][-1]
            elif diff_commands.info[i][1] == 'c':
                diff_right_start = diff_commands.info[i][2][0] - 1
                diff_right_end = diff_commands.info[i][2][-1]
            elif diff_commands.info[i][1] == 'd':
                continue
            else:
                continue
            if diff_right_start != diff_right_end:
                truth_table[diff_right_start : diff_right_end] = [False] * (diff_right_end - diff_right_start)
            else:
                truth_table[diff_right_start] = False

        truth_table.insert(0, True)
        for i in range(1, len(truth_table)):
            if truth_table[i] == True:
                print(output_new[i], end = '')
            elif truth_table[i] == False and truth_table[i - 1] == True:
                print('...')
        return 

    def get_all_diff_commands(self):
        # create lcs table
        if self.contents1 == self.contents2:
            return [DiffCommands()]
        lcs_table = []
        for i in range(len(self.contents1) + 1):
            row = []
            for j in range(len(self.contents2) + 1):
                row.append(0)
            lcs_table.append(row)
                
        same_line = []
        for i in range(1, len(lcs_table)):
            for j in range(1, len(lcs_table[i])):
                if self.contents1[i - 1] == self.contents2[j - 1]:
                    lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
                    same_line.append([i, j, lcs_table[i][j]])
                else:
                    lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])

        max_lcs_number = same_line[-1][-1]
        list_of_method = list(itertools.combinations(same_line, max_lcs_number))
        remove_index = []
        for i in range(len(list_of_method)):
            if list_of_method[i][0][2] != 1:
                remove_index.append(i)
                continue
            for j in range(1, len(list_of_method[i])):
                if list_of_method[i][j][2] == list_of_method[i][j - 1][2] + 1 and \
                   list_of_method[i][j][0] > list_of_method[i][j - 1][0] and \
                   list_of_method[i][j][1] > list_of_method[i][j - 1][1]:
                    continue
                else:
                    remove_index.append(i)
                    break
        remove_index = sorted(remove_index, reverse = True)
        for i in remove_index:
            list_of_method.pop(i)

        diffs = []
        for method in list_of_method:
            diff = DiffCommands()
            
            diff_left = [0]
            diff_right = [0]
            for i in range(len(method)):
                diff_left.append(method[i][0])
                diff_right.append(method[i][1])
            diff_left.append(len(self.contents1) + 1)
            diff_right.append(len(self.contents2) + 1)
            
            for i in range(1, len(method) + 2):
                # from left up to right down in a line
                # 1
                #   2
                #     3
                if diff_left[i] == diff_left[i - 1] + 1 and \
                   diff_right[i] == diff_right[i - 1] + 1:
                    continue

                # from left up to right down not in a line in a square
                # need change
                #  1  ...  1
                # ... ... ...
                #  1  ...  2
                if diff_left[i] > diff_left[i - 1] + 1 and \
                   diff_right[i] > diff_right[i - 1] + 1:
                    if diff_left[i] - diff_left[i - 1] > 2 and \
                       diff_right[i] - diff_right[i - 1] > 2:
                        diff.contents.append('{},{}c{},{}\n'.format(diff_left[i - 1] + 1, \
                                                                    diff_left[i] - 1, \
                                                                    diff_right[i - 1] + 1, \
                                                                    diff_right[i] - 1))
                    elif diff_left[i] - diff_left[i - 1] == 2 and \
                         diff_right[i] - diff_right[i - 1] > 2:
                        diff.contents.append('{}c{},{}\n'.format(diff_left[i] - 1, \
                                                                 diff_right[i - 1] + 1, \
                                                                 diff_right[i] - 1))
                    elif diff_left[i] - diff_left[i - 1] > 2 and \
                         diff_right[i] - diff_right[i - 1] == 2:
                        diff.contents.append('{},{}c{}\n'.format(diff_left[i - 1] + 1, \
                                                                 diff_left[i] - 1, \
                                                                 diff_right[i] - 1))
                    else:
                        diff.contents.append('{}c{}\n'.format(diff_left[i] - 1, \
                                                              diff_right[i] - 1))
                                               
                # from up to down need delete
                # 1
                # 1
                # 2
                if diff_left[i] > diff_left[i - 1] + 1 and \
                   diff_right[i] == diff_right[i - 1] + 1:
                    if diff_left[i] - diff_left[i - 1] > 2:
                        diff.contents.append('{},{}d{}\n'.format(diff_left[i - 1] + 1, \
                                                                 diff_left[i] - 1, \
                                                                 diff_right[i] - 1))
                    else:
                        diff.contents.append('{}d{}\n'.format(diff_left[i] - 1, \
                                                              diff_right[i] - 1))

                # from left to right need add
                # 1 1 2
                if diff_left[i] == diff_left[i - 1] + 1 and \
                   diff_right[i] > diff_right[i - 1] + 1:
                    if diff_right[i] - diff_right[i - 1] > 2:
                        diff.contents.append('{}a{},{}\n'.format(diff_left[i] - 1, \
                                                                 diff_right[i - 1] + 1, \
                                                                 diff_right[i] - 1))
                    else:
                        diff.contents.append('{}a{}\n'.format(diff_left[i] - 1, \
                                                              diff_right[i] - 1))

            diffs.append(diff)
        diffs = sorted(diffs, key = lambda x : x.contents)
        return diffs
       
##diff1 = DiffCommands('diff_1.txt')
##diff2 = DiffCommands('diff_2.txt')
##diff3 = DiffCommands('diff_3.txt')
##
##p1 = OriginalNewFiles('file_1_1.txt', 'file_1_2.txt')
##p2 = OriginalNewFiles('file_2_1.txt', 'file_2_2.txt')
##p3 = OriginalNewFiles('file_3_1.txt', 'file_3_2.txt')

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

##print('1')
##diffs1 = p1.get_all_diff_commands()
##print(len(diffs1))
##for i in range(len(diffs1)):
##    print(diffs1[i])
##print('2')
##diffs2 = p2.get_all_diff_commands()
##print(len(diffs2))
##for i in range(len(diffs2)):
##    print(diffs2[i])
##print('3')
##diffs3 = p3.get_all_diff_commands()
##print(len(diffs3))
##for i in range(len(diffs3)):
##    print(diffs3[i])
