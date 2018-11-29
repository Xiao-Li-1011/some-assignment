import os
import sys
from argparse import ArgumentParser
from re import sub
import math

parser = ArgumentParser()
parser.add_argument('--file', dest = 'filename', required = True)
parser.add_argument('-print', dest = 'texfile', required = False, action = 'store_true')
args = parser.parse_args()

filename = args.filename

'''each line only have '1' or '0' and delete the ' '
   if not output a file with 'Incorrect input.' the wrong input
'''
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
except ValueError:
    print('Incorrect input.')
except FileNotFoundError:
    print('Can not find the file, giving up...')
    sys.exit()

#each line have the same length 

for i in range(1, len(grid)):
    if len(grid[i]) != len(grid[0]):
        print('Incorrect input.', file = outputFile)
        sys.exit()

class Point():
    def __init__(self, x = None, y = None, num = None):
        self.x = x
        self.y = y
        self.num = num
        self.dir = 0
    '''
        dir up = 1
    '''
direction_dictionary = {8:[-1, -1], 1:[-1, 0], 2:[-1, 1],\
                        7:[0, -1], 3:[0, 1], \
                        6:[1, -1], 5:[1, 0], 4:[1, 1]}

for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j] = Point(x = i, y = j, num = grid[i][j])
def change_direction(direction):
    if direction == 0:
        return 3
    elif direction in [1, 2, 3]:
        return direction - 3 + 8
    else:
        return direction - 3

global point_list
point_list = []

def find_point(i, j, direction):
    global point_list
    dirc = change_direction(direction)
    if 0 <= i + direction_dictionary[dirc][0] < len(grid) and 0 <= j + direction_dictionary[dirc][1] < len(grid[0]) \
        and grid[i + direction_dictionary[dirc][0]][j + direction_dictionary[dirc][1]].num == 1:
        if [i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]] not in point_list \
           and [i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]] != point_list[0]:
            point_list.append([i, j])
            grid[i][j].dir = dirc
            find_point(i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1], dirc)
        elif [i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]] in point_list \
             and [i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]] != point_list[0]:
            point_list = point_list[:point_list.index([i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]])]
            x = point_list[-1][0]
            y = point_list[-1][1]
            point_list = point_list[:-1]
            next_dirc = (grid[x][y].dir + 4) % 8
            if next_dirc == 0:
                next_dirc = 8
            find_point(x, y, next_dirc)
        elif [i + direction_dictionary[dirc][0], j + direction_dictionary[dirc][1]] == point_list[0]:
            grid[i][j].dir = dirc
            point_list.append([i, j])
            return True
    else:
        if direction == 8:
            find_point(i, j, 1)
        elif direction == 0:
            find_point(i, j, 5)
        else:
            find_point(i, j, direction + 1)
            
graph = []
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j].num == 1:
            try:
                point_list.append([i, j])
                find_point(i, j, 0)
                graph.append(point_list[1:] + [point_list[0]])
                for k in range(len(point_list)):
                    grid[point_list[k][0]][point_list[k][1]].num = 0
                point_list = []
            except RecursionError:
                print('Cannot get polygons as expected.')
                sys.exit()
                
'''
   find every polygon's peak point and put them in a list
   for convex and nb of invariant rotations
'''
peak_point = []
for i in range(len(graph)):
    L = [] 
    for j in range(len(graph[i]) - 1):
        if grid[graph[i][j + 1][0]][graph[i][j + 1][1]].dir != grid[graph[i][j][0]][graph[i][j][1]].dir:
           L.append([graph[i][j + 1][0], graph[i][j + 1][1]])

    if 3 <= grid[L[-1][0]][L[-1][1]].dir <= 5:
        peak_point.append([L[-1]] + L[:-1])
    else:
        t = L[:-1]
        t.reverse()        
        peak_point.append([L[-1]] + t)
        
'''
   firstly, diciding straight edge and bevel dege by direction.
   secondly, judge the sum of edge whether 0
'''
def perimeter(g):
    count_1 = 0
    count_2 = 0
    for i in range(len(g) - 1):
        if grid[g[i][0]][g[i][1]].dir % 2 == 0:
            count_1 += 1
        if grid[g[i][0]][g[i][1]].dir % 2 != 0:
            count_2 += 1
    if count_2 == 0:
        return '{}*sqrt(.32)'.format(count_1)
    if count_1 == 0:
        return '{}'.format(0.4 * 10 * count_2 / 10)
    if count_1 != 0 and count_2 != 0:
        return '{} + {}*sqrt(.32)'.format(0.4 * 10 * count_2 / 10, count_1)
    
'''
   green theorem
'''
def area(g):
    n = len(g)
    a = 0
    for i in range(0, n - 1):
        a = a + (g[i][0] + g[i + 1][0]) * (g[i + 1][1] - g[i][1])
    return 0.5 * abs(a) * 0.16

'''
   ccording to the first point the direction and the second point in
   the direction of the synthesis of the Angle of the convex
'''
def convex(g):
    for i in range(len(g) - 1):
        if grid[g[i][0]][g[i][1]].dir == 1 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [1, 2, 3, 4]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 2 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [2, 3, 4, 5]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 3 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [3, 4, 5, 6]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 4 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [4, 5, 6, 7]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 5 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [5, 6, 7, 8]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 6 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [6, 7, 8, 1]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 7 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [7, 8, 1, 2]:
            return 'no'
        elif grid[g[i][0]][g[i][1]].dir == 8 and grid[g[i + 1][0]][g[i + 1][1]].dir not in [8, 1, 2, 3]:
            return 'no'
    return 'yes'

'''
   Firstly，determine the number of vertices is odd or even
   Secondly，if the vertex number is odd, then turn once
   Thirdly，if the even number of vertices, but each point of the center has a different, so turn once
            if the even number of vertices, each point of the center of the same, but the number of vertices can be divided four,
            then turn over four times. All other things being reverse it twice
'''
def Nb_of_invariant_rotations(g):
    length = len(g)
    p = True
    if length % 2 != 0:
        return 1
    elif length % 2 == 0:
        for i in range(1, int(length / 2)):
            if (g[i][0] + g[i + int(length / 2)][0]) / 2.0 != (g[0][0] + g[int(length / 2)][0]) / 2.0 or \
               (g[i][1] + g[i + int(length / 2)][1]) / 2.0 != (g[0][1] + g[int(length / 2)][1]) / 2.0:
                return 1
        for i in range(2, length):
            if (g[i][0] - g[i - 1][0])**2 + (g[i][1] - g[i - 1][1])**2 == (g[1][0] - g[0][0])**2 + (g[1][1] - g[0][1])**2:
                continue
            else:
                p = False
        if p and length % 4 == 0:
            return 4
        else:
             return 2

'''
   1.Each vertex trigger a ray first
     and then determine the rays several intersections on a layer of graphics，then the intersection in a list(L)
   2.With a point on the vertex of the trigger a ray and the judge has several intersection, the intersection point in another list(R)
   3.raverse the list first, if one of a number of points on the left of the point in R, add 1，
     if one of a number of points on the right of the point in R, add 1
   By 1, 2, 3 can determine a graphic in is not in another graphic
   If the inside and not their own, depth plus 1
'''
def depth(g, point):
    count = 0
    L = []
    for i in range(len(g) - 1):
       if point[0] == g[i][0] and g[i][1] < point[1]:
           L.append([g[i][0], g[i][1]])
    R = []
    for i in range(len(g) - 1):
        if point[0] - 1 == g[i][0] and g[i][1] <= point[1]:
            R.append([g[i][0], g[i][1]])
    for i in L:
        if g[g.index(i) - 1] in R:
            count += 1
        if g[g.index(i) + 1] in R:
            count += 1
    if count % 2 != 0:
        return True
    if count % 2 == 0:
        return False
d = 0
depth_list = []
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i] != graph[j] and depth(graph[j], graph[i][0]):
            d += 1
    depth_list.append(d)
    d = 0

area_list = []
for i in range(len(graph)):
    area_list.append(area(graph[i]))

output_area_list = []
for i in range(len(area_list)):
    if area_list[i] == max(area_list):
        output_area_list.append(0)
    elif area_list[i] == min(area_list):
        output_area_list.append(100)
    else:
        output_area_list.append(100 - round(((area_list[i]) - min(area_list)) / (max(area_list) - min(area_list)) * 100))


if args.texfile:
    output_texfile = sub('\..*$', '', filename) + '.tex'
    with open(output_texfile, 'w') as tex_file:
        print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]',file = tex_file)
        print('\\draw[ultra thick] (0, 0) -- ({}, 0) -- ({}, {}) -- (0, {}) -- cycle;'\
              .format(len(grid[0]) - 1, len(grid[0]) - 1, len(grid) - 1, len(grid) - 1), file = tex_file)
        for i in range(max(depth_list) + 1):
            print('%Depth {}'.format(i), file = tex_file)
            for j in range(len(depth_list)):
                if depth_list[j] == i:
                    print('\\filldraw[fill=orange!{}!yellow] '.format(output_area_list[j]), end = '', file = tex_file)
                    for k in range(len(peak_point[j])):
                        print('({}, {}) -- '.format(peak_point[j][k][1], peak_point[j][k][0]), end = '', file = tex_file)
                    print('cycle;', file = tex_file)
        print('\\end{tikzpicture}\n'
              '\\end{center}\n'
              '\\vspace*{\\fill}\n'
              '\n'
              '\\end{document}', file = tex_file)
else:
    for i in range(len(graph)):
        print('Polygon {}:'.format(i + 1))
        print('    Perimeter: {}'.format(perimeter(graph[i])))
        print('    Area: {:.2f}'.format(area(graph[i])))
        print('    Convex: {}'.format(convex(peak_point[i])))
        print('    Nb of invariant rotations: {}'.format(Nb_of_invariant_rotations(peak_point[i])))
        print('    Depth: {}'.format(depth_list[i]))
                      
                      
           
   
   
