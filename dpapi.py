def _zeroes(mx):
    """Constructs a zero matrix of shape same as mx"""
    n = len(mx)
    m = len(mx[0])

    dp = []
    for k in range(n):
        dp.append([])
        for i in range(m):
            dp[k].append(0)
    return dp

def _get(tab, i,k,m,n,ret=0):
    """Get an element of matrix tab, or val(0) if out of bounds indices"""
    if 0 <= i < m and 0 <= k < n:
        return tab[k][i]
    return ret


def dynamicProgramming(mx):
    """Computes optimum value using dynamic programming.
       Returns solution path."""
    dpt = _zeroes(mx)
    n = len(mx)
    m = len(mx[0])
    
    for i in range(m-1,-1,-1):
        for k in range(n):
            val = _get(mx, i,k,m,n)
            dp_val = max(_get(dpt,i+1, k-1,m,n),
                         _get(dpt,i+1, k,m,n),
                         _get(dpt,i+1, k+1,m,n))
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
    print('OPT: %.2f' % dpt[snake[0]][0])
    return snake
