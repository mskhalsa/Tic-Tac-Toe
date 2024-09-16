from app.game import Game
from app.game import GameSchema
from app.game import minimax
import uuid

game_schema = GameSchema() # Load schema instance

# Save the game by serializing it
def save_game(redis_conn, game, ttl):
    serialized_game = game_schema.dumps(game)
    redis_conn.setex(f"game:{game.game_id}", ttl, serialized_game) # store it in db

# Load the game by deseralizing it
def load_game(redis_conn, game_id):
    serialized_game = redis_conn.get(f"game:{game_id}") # fetch data
    if not serialized_game:
        return None
    return game_schema.loads(serialized_game)

# create a new game and save it to db
def create_new_game_service(redis_conn, board_size, ttl):
    game_id = str(uuid.uuid4()) # Generate a unique game ID
    game = Game(game_id=game_id, board_size=board_size)
    save_game(redis_conn, game, ttl)
    return game_id

# fetch a game state
def get_game_state_service(redis_conn, game_id):
    game = load_game(redis_conn, game_id)
    if not game:
        return None
    return game.get_game_state()

# Puts a player in the game
def join_existing_game_service(redis_conn, game_id, player_id, ttl):
    game = load_game(redis_conn, game_id)
    if not game:
        return None, "Game not found."

    if not game.add_player(player_id): # attempt to add player
        return None, "Cannot join game."

    save_game(redis_conn, game, ttl) # save the game after adding
    return game.get_game_state(), None

# Lets a player make a move
def make_a_move_service(redis_conn, game_id, player_id, position, ttl):
    game = load_game(redis_conn, game_id)
    if not game:
        return None, "Game not found."

    try: #  attempt to make the given move
        if not game.make_move(player_id, position):
            return None, "Invalid move."
        save_game(redis_conn, game, ttl)
        return game.get_game_state(), None 
    except Exception as e:
        return None, str(e)

# service to abandon a game
def abandon_game_service(redis_conn, game_id, player_id, ttl):
    game = load_game(redis_conn, game_id)
    if not game:
        return None, "Game not found."

    try: # attempt to abandon the game as player
        game.abandon(player_id)
        save_game(redis_conn, game, ttl)
        return game.get_game_state(), None
    except Exception as e:
        return None, str(e)

# Make a move with autset/ai help
def autoset_service(redis_conn, game_id, player_id, depth, ttl):
    game = load_game(redis_conn, game_id)
    if not game:
        return None, "Game not found."

    if game.is_over:
        return None, "Game is already over."

    if game.current_turn != player_id:
        return None, "It's not your turn."

    if game.has_player_used_autoset(player_id):
        return None, "AutoSet can only be used once per game."

    # Get symbols
    player_symbol = game.get_player_symbol(player_id)
    opponent = next((p for p in game.players if p.player_id != player_id), None)
    if opponent:
        opponent_symbol = opponent.symbol
    else:
        return None, "Opponent not found."

    # Use Minimax to find the best move
    cloned_game = game.clone()
    _, best_move = minimax(cloned_game, depth, True, player_symbol, opponent_symbol)

    if best_move is None:
        return None, "No valid moves available."

    # Make the move
    game.make_move(player_id, best_move)
    game.set_player_autoset(player_id)
    save_game(redis_conn, game, ttl)

    return game.get_game_state(), None
