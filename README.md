Introduction
This API lets you create and play games against other players with customizable board sizes to accommodate beyond the standad 3x3 board with 2 players.
The player can also use an AI to assist them in the game.

Key features include:
- Create a Game
- Join a Game
- Place an X or O on the board
- Abandon a game
- Wait your turn
- Auto Set (if a player use automatic placement, the web service makes a move on their behalf based on some simple AI, only a single automatic placement is allowed per player per game)

1. Creating a game
- To create a game make a POST request to the /games endpoint
- Pass the Parameters -> "board_size" : 3 (this makes a 3x3 board)

    - This will return a gameid which will be the key for your game
    - Use this key for all game requests in the future
- Example:
        curl -X POST http://localhost:5000/games -H "Content-Type: application/json" -d '{
        "board_size": 3
        }'

2. Joining a game
- For Player vs Player, the second player joins by making a POST request to /games/<gameid>/join
    - With params: "player_id" : "Mehar
    
- Example:
        curl -X POST http://localhost:5000/games/<gameid>/join -H "Content-Type: application/json" -d '{
        "player_id": "Mehar"
        }'

3. Make a move X or O
- For Making a move in the game ( the player must wait their turn) by making a POST request to /games/<gameid>/move
    - With parameters: "position": 5, "player_id" : "Mehar"

- Example:
        curl -X POST http://localhost:5000/games/<gameid>/move -H "Content-Type: application/json" -d '{
        "player_id": "Mehar",
        "position": 5
        }'

4. Use Autoset/AI assistance
- To get assistance from the ai in the game make a POS"T request to /games/<gameid>/autoset
    - With parameters: "depth" : 3, player_id = "Mehar"
    - The depth parameter is the depth configuration for ai.

- Example:
        curl -X POST http://localhost:5000/games/<gameid>/autoset -H "Content-Type: application/json" -d '{
        "player_id": "Mehar",
        "depth": 3
        }'

5. Adandon a game
- For abandonning a game make a POST request to /games/<gameid>/abandon
    - With parameters: "player_id" : "Mehar" (or whatever your player is)

- Example:
        curl -X POST http://localhost:5000/games/<gameid>/abandon -H "Content-Type: application/json" -d '{
        "player_id": "Mehar"
        }'

6. View the gameboard
- To look at the current game board make a GET request to /games/<gameid>

- Example:
        curl -X GET http://localhost:5000/games/<gameid>


Example:
1. Make a game
curl -X POST http://localhost:5000/games -H "Content-Type: application/json" -d '{
  "board_size": 3
}'

2. Using the gameid, join the game
curl -X POST http://localhost:5000/games/<gameid>/join -H "Content-Type: application/json" -d '{
  "player_id": "Mehar"
}'

3. Second player joins
curl -X POST http://localhost:5000/games/<gameid>/join -H "Content-Type: application/json" -d '{
  "player_id": "Singh"
}'

4. Player X (Mehar) makes a move
curl -X POST http://localhost:5000/games/<gameid>/move -H "Content-Type: application/json" -d '{
  "player_id": "Mehar",
  "position": 0
}'

5. Player O (Singh ) makes a move
curl -X POST http://localhost:5000/games/<gameid>/move -H "Content-Type: application/json" -d '{
  "player_id": "Singh",
  "position": 4
}'

6. Mehar uses autoset
curl -X POST http://localhost:5000/games/<gameid>/autoset -H "Content-Type: application/json" -d '{
  "player_id": "Mehar",
  "depth": 3
}'

.
.
.
.


Local deployment instructions:
- This app is dockerized and runs with compose

1. Go to the parent directory
    - Execute: docker compose -f docker-compose.prod.yml build (This might take a few minutes)
    - This will build your composition 
    - After the build Execute this: docker compose -f docker-compose.prod.yml up -d
        - Make sure port 6379 and 5000 are free on your computer!
    - This will spin up your app in the background
    - You can check with: 'docker ps' to ensure they are running
    - Now you can make requests to the tic-tac-toe service!


    - To stop Execute: docker compose -f docker-compose.prod.yml down -v

Thanks!