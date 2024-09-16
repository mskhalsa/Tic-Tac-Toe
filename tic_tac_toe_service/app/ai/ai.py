#Contains the AI logic for making moves using a modified Minimax algorithm.
# will take in teh game with a depth limit, and uses this algorithm to calculate
# the best possible move within that depth.
def minimax(game, depth, is_maximizing, player_symbol, opponent_symbol):

    if game.check_winner(player_symbol):
        return (1, None)
    if game.check_winner(opponent_symbol):
        return (-1, None)
    if all(cell != '' for cell in game.board) or depth == 0:
        return (0, None)

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for i, cell in enumerate(game.board):
            if cell == '':
                game.board[i] = player_symbol
                score, _ = minimax(game, depth - 1, False, player_symbol, opponent_symbol)
                game.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        return (best_score, best_move)
    else:
        best_score = float('inf')
        best_move = None
        for i, cell in enumerate(game.board):
            if cell == '':
                game.board[i] = opponent_symbol
                score, _ = minimax(game, depth - 1, True, player_symbol, opponent_symbol)
                game.board[i] = ''
                if score < best_score:
                    best_score = score
                    best_move = i
        return (best_score, best_move)
