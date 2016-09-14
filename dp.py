from __future__ import print_function
import sys

if len(sys.argv) != 2:
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

dp = []
for k in range(n):
    dp.append([])
    for i in range(m):
        dp[k].append(0)

def get(tab, i,k):
    global m,n
    if 0 <= i < m and 0 <= k < n:
        return tab[k][i]
    return 0

for i in range(m-1,-1,-1):
    for k in range(n):
        val = get(mx, i,k)
        dp_val = max(get(dp,i+1, k-1),
                     get(dp,i+1, k),
                     get(dp,i+1, k+1))
        dp[k][i] = val + dp_val


print('Matrix:')
for k in range(n):
    for i in range(m):
        print('%.2f' % mx[k][i], end=' ')
    print()

print('DP:')
for k in range(n):
    for i in range(m):
        print('%.2f' % dp[k][i], end=' ')
    print()

