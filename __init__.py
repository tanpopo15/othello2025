# Generation ID: Hutch_1765786264263_4s22kq2mp (前半)

def myai(board, color):
    """
    オセロの最適な着手位置を決定する関数
    """
    size = len(board)
    opponent = 3 - color

    # スコアテーブル（外側ほど高スコア）
    score_table = create_score_table(size)

    # 有効な手を探索
    valid_moves = get_valid_moves(board, color)

    if not valid_moves:
        return None

    best_move = None
    best_score = -float('inf')

    # ミニマックス探索（5手先まで）
    for move in valid_moves:
        board_copy = [row[:] for row in board]
        captured = apply_move(board_copy, move, color)

        # 評価値を計算
        eval_score = minimax(board_copy, opponent, color, 5, score_table, size)
        eval_score += score_table[move[1]][move[0]] * 0.5
        eval_score += len(captured) * 10

        if eval_score > best_score:
            best_score = eval_score
            best_move = move

    return best_move


def create_score_table(size):
    """スコアテーブルを生成"""
    table = [[0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            # 四隅が最高スコア
            dist_to_corner = min(i, j, size - 1 - i, size - 1 - j)
            table[i][j] = (dist_to_corner + 1) ** 2

    return table


def get_valid_moves(board, color):
    """有効な着手位置を全て取得"""
    size = len(board)
    valid_moves = []

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0 and can_place(board, (j, i), color):
                valid_moves.append((j, i))

    return valid_moves


def can_place(board, pos, color):
    """指定位置に置けるかチェック"""
    x, y = pos
    size = len(board)

    if board[y][x] != 0:
        return False

    opponent = 3 - color
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        count = 0

        while 0 <= nx < size and 0 <= ny < size and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            count += 1

        if count > 0 and 0 <= nx < size and 0 <= ny < size and board[ny][nx] == color:
            return True

    return False


def apply_move(board, pos, color):
    """着手を適用し、取られた石を返す"""
    x, y = pos
    size = len(board)
    opponent = 3 - color
    captured = []

    board[y][x] = color
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        temp_captured = []

        while 0 <= nx < size and 0 <= ny < size and board[ny][nx] == opponent:
            temp_captured.append((nx, ny))
            nx += dx
            ny += dy

        if temp_captured and 0 <= nx < size and 0 <= ny < size and board[ny][nx] == color:
            for cx, cy in temp_captured:
                board[cy][cx] = color
                captured.append((cx, cy))

    return captured


def minimax(board, current_color, ai_color, depth, score_table, size):
    """ミニマックス探索"""
    if depth == 0:
        return evaluate_board(board, ai_color, score_table, size)

    valid_moves = get_valid_moves(board, current_color)

    if not valid_moves:
        opponent_moves = get_valid_moves(board, 3 - current_color)
        if not opponent_moves:
            return evaluate_board(board, ai_color, score_table, size)
        return minimax(board, 3 - current_color, ai_color, depth, score_table, size)

    if current_color == ai_color:
        max_eval = -float('inf')
        for move in valid_moves:
            board_copy = [row[:] for row in board]
            apply_move(board_copy, move, current_color)
            eval_score = minimax(board_copy, 3 - current_color, ai_color, depth - 1, score_table, size)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            board_copy = [row[:] for row in board]
            apply_move(board_copy, move, current_color)
            eval_score = minimax(board_copy, 3 - current_color, ai_color, depth - 1, score_table, size)
            min_eval = min(min_eval, eval_score)
        return min_eval


def evaluate_board(board, ai_color, score_table, size):
    """盤面を評価"""
    ai_score = 0
    opponent_score = 0
    opponent = 3 - ai_color

    for i in range(size):
        for j in range(size):
            if board[i][j] == ai_color:
                ai_score += score_table[i][j]
            elif board[i][j] == opponent:
                opponent_score += score_table[i][j]

    return ai_score - opponent_score

# Generation ID: Hutch_1765786264263_4s22kq2mp (後半)
