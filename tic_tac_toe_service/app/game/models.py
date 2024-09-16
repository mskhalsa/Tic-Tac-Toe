from typing import List, Optional
from copy import deepcopy

class Player:
    def __init__(self, player_id: str, symbol: str, autoset_used=False):
        # the players name/id, their symbol X/O, and their autoset flag
        self.player_id = player_id 
        self.symbol = symbol
        self.autoset_used = autoset_used 

# The game class for the actual game
class Game:
    def __init__(self, game_id: str, board_size: int = 3):
        self.game_id = game_id # Unique id for the game
        self.board_size = board_size
        self.board = ['' for _ in range(board_size * board_size)] 
        self.players: List[Player] = [] # players in the game
        self.current_turn: Optional[str] = None
        self.winner: Optional[str] = None
        self.is_over: bool = False #

    # Add a player to the game
    def add_player(self, player_id: str) -> bool:
        if len(self.players) >= 2:
            return False
        # Assign symbols to players X for first, O for second
        symbol = 'X' if not self.players else 'O'
        self.players.append(Player(player_id, symbol))
        if not self.current_turn:
            self.current_turn = player_id
        return True

    # Make a move for a player at a given position
    def make_move(self, player_id: str, position: int) -> bool:
        if self.is_over: # Cannot move if game over
            return False
        if self.current_turn != player_id: # Its not this players turn
            return False
        if position < 0 or position >= self.board_size * self.board_size: # Position is out of bounds
            return False
        if self.board[position] != '': # position is already occupied
            return False

        # Get the players symbol, check if in game
        player_symbol = next((p.symbol for p in self.players if p.player_id == player_id), None)
        if not player_symbol:
            return False

        # Place the players symbol on the board
        self.board[position] = player_symbol

        # Check if this move wins the game
        if self.check_winner(player_symbol):
            self.winner = player_id
            self.is_over = True
        else:
            # Check for a draw
            if all(cell != '' for cell in self.board):
                self.is_over = True
            else:
                # Switch to the next player's turn
                self.switch_turn()
        return True

    # Switch turns
    def switch_turn(self):
        next_player = next(p for p in self.players if p.player_id != self.current_turn)
        self.current_turn = next_player.player_id

    # Check if a player is winner
    def check_winner(self, symbol: str) -> bool:
        n = self.board_size
        board = self.board
        lines = []

        # Check rows
        for i in range(n):
            start = i * n
            lines.append(board[start:start + n])

        # Columns
        for i in range(n):
            lines.append([board[i + j * n] for j in range(n)])

        # main diagonal
        lines.append([board[i * (n + 1)] for i in range(n)])

        # Other diagonal
        lines.append([board[(i + 1) * (n - 1)] for i in range(n)])

        # Check if any line has all symbols matching the player symbol
        for line in lines:
            if all(cell == symbol for cell in line):
                return True
        return False

    # Abandon a game - the other player wins
    def abandon(self, player_id: str):
        self.is_over = True
        self.winner = next((p.player_id for p in self.players if p.player_id != player_id), None)

    # Dictionary of the game state
    def get_game_state(self):
        return {
            'game_id': self.game_id,
            'board_size': self.board_size,
            'board': self.board,
            'players': [{'player_id': p.player_id, 'symbol': p.symbol, 'autoset_used': p.autoset_used} for p in self.players],
            'current_turn': self.current_turn,
            'winner': self.winner,
            'is_over': self.is_over
        }

    # Get symbol for player
    def get_player_symbol(self, player_id: str) -> Optional[str]:
        player = self.get_player_by_id(player_id)
        return player.symbol if player else None

    # Check if autoset used
    def has_player_used_autoset(self, player_id: str) -> bool:
        player = self.get_player_by_id(player_id)
        return player.autoset_used if player else False

    # Mark autoset used
    def set_player_autoset(self, player_id: str):
        player = self.get_player_by_id(player_id)
        if player:
            player.autoset_used = True
    
    # Iterate to the next player id
    def get_player_by_id(self, player_id: str):
        return next((p for p in self.players if p.player_id == player_id), None)

    # create a copy of this object for ai
    def clone(self):
        return deepcopy(self)
