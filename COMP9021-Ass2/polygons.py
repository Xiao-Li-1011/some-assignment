import os
import sys
from argparse import ArgumentParser
from re import sub
import math

class Point():
    def __init__(self, x = None, y = None, value = None):
        if x == None and y == None:
            self.x = 0
            self.y = 0
        elif x == None or y == None:
            print('Need two coordinates, point not created.')
        else:
            self.x = x
            self.y = y
        self.value = value
        self.or_value = value
        '''
        direction have eight value:
        right is 1, right down is 2, down is 3, left down is 4
        left is 5, left up is 6, up is 7, right up is 8
        default is 0
        '''
        self.out_direction = 0
    
parser = ArgumentParser()
parser.add_argument('--file', dest = 'filename', required = True)
parser.add_argument('-print', dest = 'texfile', required = False, action = 'store_true')
args = parser.parse_args()

filename = args.filename

# each line only have '1' or '0' and delete the ' '
# if not output a file with 'Incorrect input.' the wrong input
try:
    grid = []
    with open(filename) as file:
        for line in file:
            L = []
            for c in line:
                if c == '1' or c == '0':
                    L.append(int(c))
                elif c == ' ':
                    continue
                elif c == '\n':
                    break
                else:
                    raise ValueError
            if len(L) <= 50 and len(L) >= 2:
                grid.append(L)
            elif not L:
                continue
            else:
                raise ValueError
# get the grid and only have '1' or '0'
# other print 'Incorrect input.'
except ValueError:
    print('Incorrect input.')
    sys.exit()
except FileNotFoundError:
    print('Can not find the file, giving up...')
    sys.exit()
    
# each line have the same length
for i in range(1, len(grid)):
    if len(grid[i]) != len(grid[0]):
        print('Incorrect input.')
        sys.exit()

global P
P = []
# array have all the points in one graph
graph = []
# array only have peak points in one graph
graph_only_peak = []

# change the grid to save class Point into double dimensional array.
for i in range(len(grid)):
    for j in range(len(grid[0])):
        grid[i][j] = Point(x = i, y = j, value = grid[i][j])

# recursion function to get polygons.
def start_draw(i, j, direction):
    global P
    if direction == 0:
        start_direction = 1
    elif direction == 2:
        start_direction = 8
    else:
        start_direction = (direction - 2 + 8) % 8
    if start_direction == 1 and \
                         j + 1 < len(grid[0]) and grid[i][j + 1].value == 1:
        if [i, j + 1] not in P and [i, j + 1]  != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i, j + 1, start_direction)
        elif [i, j + 1] in P and [i, j + 1] != P[0]:
            P = P[ : P.index([i, j + 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i, j + 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
            
    elif start_direction == 2 and \
                           i + 1 < len(grid) and j + 1 < len(grid[0]) and grid[i + 1][j + 1].value == 1:
        if [i + 1, j + 1] not in P and [i + 1, j + 1] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i + 1, j + 1, start_direction)
        elif [i + 1, j + 1] in P and [i + 1, j + 1] != P[0]:
            P = P[ : P.index([i + 1, j + 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i + 1, j + 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
            
    elif start_direction == 3 and \
                           i + 1 < len(grid) and grid[i + 1][j].value == 1:
        if [i + 1, j] not in P and [i + 1, j] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i + 1, j, start_direction)
        elif [i + 1, j] in P and [i + 1, j] != P[0]:
            P = P[ : P.index([i + 1, j])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i + 1, j] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
            
    elif start_direction == 4 and \
                           i + 1 < len(grid) and j > 0 and grid[i + 1][j - 1].value == 1:
        if [i + 1, j - 1] not in P and [i + 1, j - 1] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i + 1, j - 1, start_direction)
        elif [i + 1, j - 1] in P and [i + 1, j - 1] != P[0]:
            P = P[ : P.index([i + 1, j - 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i + 1, j - 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
        
    elif start_direction == 5 and \
                           j > 0 and grid[i][j - 1].value == 1:
        if [i, j - 1] not in P and [i, j - 1] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i, j - 1, start_direction)
        elif [i, j - 1] in P and [i, j - 1] != P[0]:
            P = P[ : P.index([i, j - 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i, j - 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
        
    elif start_direction == 6 and \
                           i > 0 and j > 0 and grid[i - 1][j - 1].value == 1:
        if [i - 1, j - 1] not in P and [i - 1, j - 1] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i - 1, j - 1, start_direction)
        elif [i - 1, j - 1] in P and [i - 1, j - 1] != P[0]:
            P = P[ : P.index([i - 1, j - 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i - 1, j - 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
        
    elif start_direction == 7 and \
                           i > 0 and grid[i - 1][j].value == 1:
        if [i - 1, j] not in P and [i - 1, j] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i - 1, j, start_direction)
        elif [i - 1, j] in P and [i - 1, j] != P[0]:
            P = P[ : P.index([i - 1, j])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i - 1, j] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
        
    elif start_direction == 8 and \
                           i > 0 and j + 1 < len(grid[0]) and grid[i - 1][j + 1].value == 1:
        if [i - 1, j + 1] not in P and [i - 1, j + 1] != P[0]:
            P.append([i, j])
            grid[i][j].out_direction = start_direction
            start_draw(i - 1, j + 1, start_direction)
        elif [i - 1, j + 1] in P and [i - 1, j + 1] != P[0]:
            P = P[ : P.index([i - 1, j + 1])]
            start_x = P[-1][0]
            start_y = P[-1][1]
            P = P[ : -1]
            start_draw(start_x, start_y, (grid[start_x][start_y].out_direction + 3 + 8) % 8)
        elif [i - 1, j + 1] == P[0]:
            grid[i][j].out_direction = start_direction
            P.append([i, j])
            return True
        
    else:
        if direction == 8:
            start_draw(i, j, 1)
        elif direction == 0:
            start_draw(i, j, 4)
        else:
            start_draw(i, j, direction + 1)

# function to compute the perimeter by using the Point.direction in graph.
# 1, 3, 5, 7 is 0.4 ; 2, 4, 6, 8 is sqrt(.32)
def perimeter(graph):
    perimeter_1 = 0
    perimeter_2 = 0
    for i in range(len(graph) - 1):
        if grid[graph[i][0]][graph[i][1]].out_direction % 2 == 1:
            perimeter_1 += 1
        elif grid[graph[i][0]][graph[i][1]].out_direction % 2 == 0:
            perimeter_2 += 1
    if perimeter_1 and perimeter_2:
        return '{} + {}*sqrt(.32)'.format(0.4 * 10 * perimeter_1 / 10, perimeter_2)
    if not perimeter_1 and not perimeter_2:
        return False
    if perimeter_1:
        return '{}'.format(0.4 * 10 * perimeter_1 / 10)
    if perimeter_2:
        return '{}*sqrt(.32)'.format(perimeter_2)

# function to compute the area by using Point.x Point.y
'''
    how to compute the area of a polygons with the x,y of all points of the polygons
    P0(x0, y0), P1(x1, y1), ..., P(xn, yn)
    R1 = x0 * y1 + x1 * y2 + ... + xn-1 * yn
    R2 = x1 * y0 + x2 * y1 + ... + xn * yn-1
    area = |R1 - R2| / 2 
'''
def area(graph):
    result1 = 0
    result2 = 0
    for i in range(len(graph) - 1):
        result1 += graph[i][0] * graph[i + 1][1]
        result2 += graph[i][1] * graph[i + 1][0]
    area = abs(result1 - result2) / 2 * 0.16
    return area

# function to compute if two direction less than 180 degrees
# yes return True
# no return False
def less_180(a, b):
    if a == 1:
        if b in [6, 7, 8]:
            return False
        else:
            return True
    if a == 2:
        if b in [1, 7, 8]:
            return False
        else:
            return True
    if a == 3:
        if b in [1, 2, 8]:
            return False
        else:
            return True
    if a == 4:
        if b in [1, 2, 3]:
            return False
        else:
            return True
    if a == 5:
        if b in [2, 3, 4]:
            return False
        else:
            return True
    if a == 6:
        if b in [3, 4, 5]:
            return False
        else:
            return True
    if a == 7:
        if b in [4, 5, 6]:
            return False
        else:
            return True
    if a == 8:
        if b in [5, 6, 7]:
            return False
        else:
            return True

# function using less_180() to compute whether the graph is convex or not
# if one angle greater than 180 degrees return 'no' 
def convex(graph):
    for i in range(len(graph) - 2):
        if not less_180(grid[graph[i][0]][graph[i][1]].out_direction, \
                        grid[graph[i + 1][0]][graph[i + 1][1]].out_direction):
            return 'no'
    return 'yes'

# function to compute depth
'''
    for computing graph in another graph
    because of the recursion
    could change the question 'graph in another graph' to question 'starting point of graph in another graph'
'''
def point_in_out(point, graph):
    x = point[0]
    y = point[1]
    list_y = []
    list_y_1 = []
    nb_line = 0
    for point_compare in graph[:-1]:
        if point_compare[0] == x and point_compare[1] < y:
            list_y.append(point_compare)
        if point_compare[0] == x - 1 and point_compare[1] <= y:
            list_y_1.append(point_compare)
    if not list_y or not list_y_1:
        return False
    for i in list_y_1:
        index_nb = graph[: -1].index(i)
        if index_nb == len(graph) - 2:
            if graph[index_nb - 1] in list_y:
                nb_line += 1
            if graph[0] in list_y:
               nb_line += 1
        elif index_nb == 0:
            if graph[-2] in list_y:
                nb_line += 1
            if graph[index_nb + 1] in list_y:
               nb_line += 1
        else:
            if graph[index_nb - 1] in list_y:
                nb_line += 1
            if graph[index_nb + 1] in list_y:
                nb_line += 1
    if nb_line % 2 == 0:
        return False
    elif nb_line % 2 == 1:
        return True

# function to compute whether each edges of a polygon is same    
def is_perfect_polygon(graph):
    diff = (graph[1][0] - graph[0][0]) ** 2 + (graph[1][1] - graph[0][1]) ** 2
    for i in range(2, len(graph)):
        if (graph[i][0] - graph[i - 1][0]) ** 2 + (graph[i][1] - graph[i - 1][1]) ** 2 != diff:
            return False
    return True

# function to compute the number of invariant rotations
'''
    if the number of a polygon's edges is odd
    return 1
    if the number of a polygon's edges is even
    could have three results 1 or 2 or 4
    if is not perfect return 1
    if a polygon is perfect and the edges of a polygon % 4 != 0
    return 2 
    if a polygon is perfect and the edges of a polygon % 4 == 0
    return 4
'''
def nb_of_invariant_rotations(graph):
    if len(graph) % 2 == 1:
        return 1
    else:
        diff = len(graph) // 2
        x_mid = (graph[0][0] + graph[diff][0]) / 2.0
        y_mid = (graph[0][1] + graph[diff][1]) / 2.0
        for i in range(1, diff):
            if (graph[i][0] + graph[i + diff][0]) / 2.0 != x_mid or \
               (graph[i][1] + graph[i + diff][1]) / 2.0 != y_mid:
                return 1
        if is_perfect_polygon(graph) and len(graph) % 4 == 0:
            return 4
        else:
            return 2

# get the graph array
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j].value == 1:
            P.append([i, j])
            try:
                start_draw(i, j, 0)
                graph.append(P[1:] + [P[0]])
                for k in range(len(P)):
                    grid[P[k][0]][P[k][1]].value = 0
                P = []
            except RecursionError:
                print('Cannot get polygons as expected.')
                sys.exit()

# get the graph array only have peak point
for i in range(len(graph)):
    trans = []
    for j in range(len(graph[i]) - 1):
        if grid[graph[i][j + 1][0]][graph[i][j + 1][1]].out_direction != \
           grid[graph[i][j][0]][graph[i][j][1]].out_direction:
            trans.append([graph[i][j + 1][0], graph[i][j + 1][1]])
    if 1 <= grid[trans[-1][0]][trans[-1][1]].out_direction <= 3: 
        graph_only_peak.append([trans[-1]] + trans[:-1])
    else:
        translist = trans[:-1]
        translist.reverse()
        graph_only_peak.append([trans[-1]] + translist)

# get the depth array for each polygon
count_depth = 0
graph_depth = []
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i] == graph[j]:
            continue
        if point_in_out(graph[i][0], graph[j]):
            count_depth += 1
    graph_depth.append(count_depth)
    count_depth = 0

# record the maximal area and minimal area
max_area = 0
min_area = 384.16

if args.texfile:
    for i in range(len(graph)):
        if max_area <= area(graph[i]):
            max_area = area(graph[i])
        if min_area >= area(graph[i]):
            min_area = area(graph[i])
    diff_area = max_area - min_area
    output_texfile = sub('\..*$', '', filename) + '.tex'
    with open(output_texfile, 'w') as outputTexfile:
        print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]', \
              file = outputTexfile
              )
        print('\\draw[ultra thick] (0, 0) -- ({}, 0) -- ({}, {}) -- (0, {}) -- cycle;'\
              .format(len(grid[0]) - 1, len(grid[0]) - 1, len(grid) - 1, len(grid) - 1), \
              file = outputTexfile)

        # 100 - (area - min) / (max - min) * 100 round to get the color number
        for d in range(max(graph_depth) + 1):
            print('%Depth {}'.format(d), file = outputTexfile)
            for i in range(len(graph_depth)):
                if graph_depth[i] == d:
                    if area(graph[i]) != max_area and area(graph[i]) != max_area:
                        print('\\filldraw[fill=orange!{}!yellow] ' \
                              .format(100 - round((area(graph[i]) - min_area) / diff_area * 100)), \
                              end = '', file = outputTexfile)
                    elif area(graph[i]) == max_area:
                        print('\\filldraw[fill=orange!0!yellow] ', \
                              end = '', file = outputTexfile)
                    elif area(graph[i]) == min_area:
                        print('\\filldraw[fill=orange!100!yellow] ', \
                              end = '', file = outputTexfile)
                    for j in range(len(graph_only_peak[i])):
                          print('({}, {}) -- ' \
                                .format(graph_only_peak[i][j][1], graph_only_peak[i][j][0]), \
                                end = '', file = outputTexfile)
                    print('cycle;', file = outputTexfile)
        print('\\end{tikzpicture}\n'
              '\\end{center}\n'
              '\\vspace*{\\fill}\n'
              '\n'
              '\\end{document}', \
              file = outputTexfile)

    # os.system('pdflatex ' + output_texfile)
    # for file in (sub('\..*$', '', filename) + ext for ext in ('.aux', '.log')):
    #     os.remove(file)
else:
    for i in range(len(graph)):
        print('Polygon {}:'.format(i + 1))
        print('    Perimeter: {}'.format(perimeter(graph[i])))
        print('    Area: {:.2f}'.format(area(graph[i])))
        print('    Convex: {}'.format(convex(graph_only_peak[i])))
        print('    Nb of invariant rotations: {}'.format(nb_of_invariant_rotations(graph_only_peak[i])))
        print('    Depth: {}'.format(graph_depth[i]))      
