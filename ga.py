from __future__ import print_function
import sys

if len(sys.argv) < 2:
    print('dp file')
    exit(1)

mx = []
with open(sys.argv[1], 'r') as f:
    for l in f:
        l = l.strip()
        if len(l) > 0:
            mx.append(map(float, l.split()))

n = len(mx)
m = len(mx[0])

def get(tab, i,k):
    global m,n
    if 0 <= i < m and 0 <= k < n:
        return tab[k][i]
    return 0

def valid(snake):
    """Verifies a snake is valid, i.e. length m, ascends at most 1, is contained in matrix"""
    global m,n
    for i in range(1,len(snake)):
        if abs(snake[i-1] - snake[i]) > 1:
            return False
        if not 0 <= snake[i-1] < n:
            return False
        if not 0 <= snake[i] < n:
            return False
    return m == len(snake)

def value(snake):
    """Collects the snake food"""
    if not valid(snake):
        return float('nan')     
    global mx
    return sum([mx[snake[i]][i] for i in range(len(snake))])

# print('Matrix:')
# for k in range(n):
#     for i in range(m):
#         print('%.2f' % mx[k][i], end=' ')
#     print()

in_depth = n/2
if len(sys.argv) >= 3:
    in_depth = int(sys.argv[2])

snake = []
for i in range(m):
    snake.append(in_depth)

print('Snake: %d'   % in_depth)
print('Valid: %s'   % str(valid(snake)))
print('Value: %.2f' % value(snake))
