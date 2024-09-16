from app.game import Game
from app.game import minimax
# This test plays a mock game which demonstrates the AI AutoSet capability as per spec
# Here the AI should should move to position 7 and take the win
def test_play_mock_game_with_autoset_middle_game():
    board = [
        "X", "O", "X",  # The ai should move to position 7 to win game
        "X", "O", "",
        "O", "", ""
    ]
    board_size = 3

    print("Current board state before AutoSet:")
    print_board(board, board_size)
    game = Game(game_id="test_game", board_size=board_size)
    game.board = board  
    game.current_turn = "O"
    
    _, best_move = minimax(game, depth=3, is_maximizing=True, player_symbol="O", opponent_symbol="X")
    game.board[best_move] = "O"  # ai moves

    assert best_move == 7, "AutoSet should move to position 7 to win the game"
    assert game.board[7] == "O", "AutoSet should have moved at position 7 to win the game"

    print("Board state after AutoSet:")
    print_board(game.board, board_size)

# Print the board to a readable format
def print_board(board, board_size):
    for i in range(0, len(board), board_size):
        print(board[i:i + board_size])
    print("\n")
