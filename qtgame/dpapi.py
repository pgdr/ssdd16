def _zeroes(mx):
    """Constructs a zero matrix of shape same as mx"""
    width = len(mx)
    height = len(mx[0])

    dp = []
    for i in range(width):
        dp.append([])
        for j in range(height):
            dp[i].append(0)
    return dp

def _get(tab,i,j,width,height,ret=0):
    """Get an element of matrix tab, or val(0) if out of bounds indices"""
    if 0 <= i < width and 0 <= j < height:
        return tab[i][j]
    return ret


def dynamicProgramming(mx):
    """Computes optimum value using dynamic programming.
       Returns solution path."""
    dpt    = _zeroes(mx)
    width  =  len(mx)
    height = len(mx[0])
    
    for i in range(width-1,-1,-1):
        for j in range(height):
            val = _get(mx, i, j, width, height)
            dp_val = max(_get(dpt, i+1, j-1, width, height),
                         _get(dpt, i+1, j  , width, height),
                         _get(dpt, i+1, j+1, width, height))
            dpt[i][j] = val + dp_val

    # build snake
    snake = []
    for i in range(width):
        cbest = 0
        c_j_idx = 0
        for j in range(height):
            if dpt[i][j] > cbest:
                if i == 0 or abs(snake[i-1] - j) <= 1:
                    cbest = dpt[i][j]
                    c_j_idx = j
        snake.append(c_j_idx)

    return snake
