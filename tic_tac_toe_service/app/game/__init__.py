from .models import Game, Player
from .schemas import GameSchema, PlayerSchema
from app.ai import minimax
from .services import ( create_new_game_service, get_game_state_service,join_existing_game_service, 
                       make_a_move_service, abandon_game_service, autoset_service)
from .routes import tic_tac_toe_bp