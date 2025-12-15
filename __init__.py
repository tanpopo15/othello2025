# Generation ID: Hutch_1765782627575_zeo16y37y (前半)

def myai(board, color):
    """
    オセロで最も得点が取れる位置を返す
    board: 6x6 または 8x8 のボード
    color: 置く色 (1=BLACK, 2=WHITE)
    return: (column, row) タプル
    """
    size = len(board)
    
    # スコアマップの生成（外側ほど高得点）
    score_map = generate_score_map(size)
    
    # 有効な手を取得
    valid_moves = get_valid_moves(board, color, size)
    
    if not valid_moves:
        return None
    
    # 各手のスコアを計算
    best_score = -1
    best_move = None
    
    for col, row in valid_moves:
        # ボードをコピーして手を試す
        temp_board = [row[:] for row in board]
        flipped = simulate_move(temp_board, col, row, color, size)
        
        # スコア計算
        move_score = calculate_score(temp_board, color, score_map, size)
        
        if move_score > best_score:
            best_score = move_score
            best_move = (col, row)
    
    return best_move


def generate_score_map(size):
    """スコアマップを生成（外側ほど高得点）"""
    score_map = [[0] * size for _ in range(size)]
    
    for i in range(size):
        for j in range(size):
            # 辺からの距離
            dist = min(i, j, size - 1 - i, size - 1 - j)
            score_map[i][j] = dist + 1
    
    # 四隅を最高得点に
    score_map[0][0] = size
    score_map[0][size - 1] = size
    score_map[size - 1][0] = size
    score_map[size - 1][size - 1] = size
    
    return score_map


def get_valid_moves(board, color, size):
    """有効な手を全て取得"""
    valid_moves = []
    opponent = 3 - color
    
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0 and is_valid_move(board, j, i, color, opponent, size):
                valid_moves.append((j, i))
    
    return valid_moves


def is_valid_move(board, col, row, color, opponent, size):
    """指定位置が有効な手かチェック"""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dx, dy in directions:
        x, y = col + dx, row + dy
        if 0 <= x < size and 0 <= y < size and board[y][x] == opponent:
            x += dx
            y += dy
            while 0 <= x < size and 0 <= y < size:
                if board[y][x] == 0:
                    break
                if board[y][x] == color:
                    return True
                x += dx
                y += dy
    
    return False


def simulate_move(board, col, row, color, size):
    """手を実行してひっくり返す"""
    opponent = 3 - color
    board[row][col] = color
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    flipped = 0
    
    for dx, dy in directions:
        flip_list = []
        x, y = col + dx, row + dy
        
        while 0 <= x < size and 0 <= y < size and board[y][x] == opponent:
            flip_list.append((x, y))
            x += dx
            y += dy
        
        if 0 <= x < size and 0 <= y < size and board[y][x] == color and flip_list:
            for fx, fy in flip_list:
                board[fy][fx] = color
                flipped += 1
    
    return flipped


def calculate_score(board, color, score_map, size):
    """ボードのスコアを計算"""
    score = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == color:
                score += score_map[i][j]
    return score

# Generation ID: Hutch_1765782627575_zeo16y37y (後半)
