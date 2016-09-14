from __future__ import print_function
import sys

def zeroes(mx):
    n = len(mx)
    m = len(mx[0])

    dp = []
    for k in range(n):
        dp.append([])
        for i in range(m):
            dp[k].append(0)
    return dp

def get(tab, i,k,m,n):
    if 0 <= i < m and 0 <= k < n:
        return tab[k][i]
    return 0


def dodp(mx):
    dpt = zeroes(mx)
    n = len(mx)
    m = len(mx[0])
    
    for i in range(m-1,-1,-1):
        for k in range(n):
            val = get(mx, i,k,m,n)
            dp_val = max(get(dpt,i+1, k-1,m,n),
                         get(dpt,i+1, k,m,n),
                         get(dpt,i+1, k+1,m,n))
            dpt[k][i] = val + dp_val
    snake = []
    for i in range(m):
        cbest = 0
        c_k_idx = 0
        for k in range(n):
           if dpt[k][i] > cbest:
               if i == 0 or abs(snake[i-1] - k) <= 1:
                   cbest = dpt[k][i]
                   c_k_idx = k
        snake.append(c_k_idx)
    return snake


def main():
    if len(sys.argv) != 2:
        print('dp file')
        exit(1)
     
    mx = []
    with open(sys.argv[1], 'r') as f:
        for l in f:
            l = l.strip()
            if len(l) > 0:
                mx.append(map(float, l.split()))
     
    snake = dodp(mx)
    print(snake)


# main()
