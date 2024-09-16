# Using the marshmallow lib for serialization for redis
from marshmallow import Schema, fields, post_load
from app.game import Game, Player

# Schema for de/serializing player objects
class PlayerSchema(Schema):
    player_id = fields.Str(required=True)
    symbol = fields.Str(required=True)
    autoset_used = fields.Bool(dump_default=False)

    @post_load
    def make_player(self, data, **kwargs):
        return Player(**data) #Returns a player instance

# Schema for de/serializing game objects objects
class GameSchema(Schema):
    game_id = fields.Str(required=True)
    board_size = fields.Int(required=True)
    board = fields.List(fields.Str())
    players = fields.List(fields.Nested(PlayerSchema)) # players are part of the game
    current_turn = fields.Str(allow_none=True)
    winner = fields.Str(allow_none=True)
    is_over = fields.Bool()

    @post_load
    def make_game(self, data, **kwargs):
        # Reconstruct the Game object from deserialized data
        game = Game(game_id=data['game_id'], board_size=data.get('board_size', 3))
        game.board = data.get('board', game.board)
        game.players = data.get('players', [])
        game.current_turn = data.get('current_turn')
        game.winner = data.get('winner')
        game.is_over = data.get('is_over', False)
        return game # return a game instance
