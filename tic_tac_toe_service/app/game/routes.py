from flask import Blueprint, request, jsonify, current_app
from app.game import (create_new_game_service, get_game_state_service,join_existing_game_service,
                          make_a_move_service, abandon_game_service, autoset_service)

tic_tac_toe_bp = Blueprint('tic_tac_toe', __name__) # Add routes to blueprint
# Route to create a new game
@tic_tac_toe_bp.route('/games', methods=['POST'])
def create_new_game():
    data = request.get_json() or {}
    board_size = data.get('board_size', 3)

    if board_size < 3:
        return jsonify({"error": "Board size must be at least 3"}), 400

    game_id = create_new_game_service(current_app.redis, board_size, current_app.config['TTL'])
    return jsonify({"game_id": game_id}), 201

# Route to display the current game state
@tic_tac_toe_bp.route('/games/<game_id>', methods=['GET'])
def get_game_state(game_id):
    game_state = get_game_state_service(current_app.redis, game_id)
    if not game_state:
        return jsonify({"error": "Game not found."}), 404
    return jsonify(game_state), 200

# Route to join game
@tic_tac_toe_bp.route('/games/<game_id>/join', methods=['POST'])
def join_existing_game(game_id):
    data = request.get_json() or {}
    player_id = data.get('player_id')

    if not player_id:
        return jsonify({"error": "Player ID must be specified."}), 400

    game_state, error = join_existing_game_service(current_app.redis, game_id, player_id, current_app.config['TTL'])

    if error:
        return jsonify({"error": error}), 400
    return jsonify(game_state), 200

# Make a move in the game
@tic_tac_toe_bp.route('/games/<game_id>/move', methods=['POST'])
def make_a_move(game_id):
    data = request.get_json() or {}
    position = data.get('position')
    player_id = data.get('player_id')

    if position is None or player_id is None:
        return jsonify({"error": "Position and player_id must be specified."}), 400

    game_state, error = make_a_move_service(current_app.redis, game_id, player_id, position, current_app.config['TTL'])

    if error:
        return jsonify({"error": error}), 400
    return jsonify(game_state), 200

# Abandon a game
@tic_tac_toe_bp.route('/games/<game_id>/abandon', methods=['POST'])
def abandon_game(game_id):
    data = request.get_json() or {}
    player_id = data.get('player_id')

    if not player_id:
        return jsonify({"error": "Player ID must be specified."}), 400

    game_state, error = abandon_game_service(current_app.redis, game_id, player_id, current_app.config['TTL'])

    if error:
        return jsonify({"error": error}), 400
    return jsonify(game_state), 200

# Route for using autoset, to get the next move from ai
@tic_tac_toe_bp.route('/games/<game_id>/autoset', methods=['POST'])
def autoset(game_id):
    data = request.get_json() or {}
    depth = data.get('depth', 3)  # Default depth
    player_id = data.get('player_id')

    if not player_id:
        return jsonify({"error": "Player ID must be specified."}), 400

    game_state, error = autoset_service(current_app.redis, game_id, player_id, depth, current_app.config['TTL'])

    if error:
        return jsonify({"error": error}), 400
    return jsonify(game_state), 200

# Route for Testing redis connection
@tic_tac_toe_bp.route('/test-redis', methods=['GET'])
def test_redis():
    try:
        current_app.redis.ping()
        return jsonify({"status": "Redis is connected!"}), 200
    except Exception as e:
        current_app.logger.error(f"Redis connection error: {str(e)}")
        return jsonify({"error": str(e)}), 500
