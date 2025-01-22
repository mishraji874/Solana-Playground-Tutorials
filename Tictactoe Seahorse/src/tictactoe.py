from seahorse.prelude import *

declare_id('D7sdb2RhuKQVSYYwuWKJmmyodTNgerDkARSqczmakTLg')

# Game account
# Okay, so let's start with how to represent the game state. We do this in Seahorse with an account class which we'll call Game. This will need to store the grid, the players, who's turn it is and if anyone has won. For the sake of simplification we'll be taking the classic tic-tac-toe 3x3 grid and flattening it into a traditional zero indexed array of length 9. The array will be filled with integers as we need to represent 3 states, "X", "O" or "empty" which we can represent with the integers "1", "2" and "0" respectively. u8 means an unsigned integer of 8 bits, i.e. a value from 0 to 255, inclusive.
class Game(Account):
    grid: Array[u8, 9] # array of ints, length 9
    players: Array[Pubkey, 2] # array of 2 pubkeys
    curr_player: u8
    game_status: u8


#   Winning states
# Next we'll set up some Enums that allow us to express the four possible winning states of a game. The variants include InProgress for a game still in progress, Draw for a draw, Player1Wins for player 1 winning, and Player2Wins for player 2 winning. These Enums will be referenced later in our code.
class GameState(Enum):
    InProgress = 0
    Player1Wins = 1
    Player2Wins = 2
    Draw = 3


# initialize game
# Let's create an instruction to initialize a new game. The function will take four arguments, the signer, an empty Game account instance and the public addresses of the 2 players. The game is a program derived account (PDA) initialized by two seeds, a string "ttt" and the signer's public key address. We set the game status to 0 which means active, when the game enters a finished state this will turn to 1. Current player is set to player 1.
@instruction
def init_game(owner: Signer, player1: Pubkey, player2: Pubkey, game: Empty[Game]):
    game = game.init(
        payer = owner,
        seeds = ['ttt', owner]
    )
    game.players[0] = player1
    game.players[1] = player2
    game.game_status = 0
    game.curr_player = 1


# check if someone has won
# Next we want to create our win_check function which checks the grid to see if a player has won the game. There are eight possible lines which can be drawn on a 3x3 grid which gives us eight possible win conditions in a game of tic-tac-toe. We check each one in turn and if any one of the conditions is true we return a game state indicating the current player has won. If no one has won, we also check to see if the board is full. If we find it is full, we return a game state of Draw otherwise we return InProgress indicating the game is still in play.
def win_check(grid: Array[u8, 9], player: u8)-> GameState:

  # check for 8 possible win conditions
  if(
    (grid[0] == player and grid[1] == player and grid[2] == player) or
    (grid[0] == player and grid[3] == player and grid[6] == player) or
    (grid[6] == player and grid[7] == player and grid[8] == player) or
    (grid[2] == player and grid[5] == player and grid[8] == player) or
    (grid[0] == player and grid[4] == player and grid[8] == player) or
    (grid[2] == player and grid[4] == player and grid[6] == player) or
    (grid[1] == player and grid[4] == player and grid[7] == player) or
    (grid[3] == player and grid[4] == player and grid[5] == player)
  ):
    if player == 1:
      return GameState.Player1Wins
    else:
      return GameState.Player2Wins

  # check for full board i.e. draw
  for i in range(9):
    if grid[i] == 0:
      return GameState.InProgress

  return GameState.Draw
    


# play a turn
# Our second instruction allows for a player to take their turn. The function takes four arguments: two accounts - the signer and the game instance - and two integers - the player and their move. The first part of this instruction is entirely input validation. We do five checks to ensure that the instruction is being called in a correct way that fits the rules of the game. Each of these checks is commented below.
@instruction
def play_game(player: Signer, game_data: Game, played_by: u8, move_position: u8):
    # check the game is active
    assert game_data.game_status == 0, "This game is already finished"

    # check for the validd signer
    assert game_data.players[played_by - 1] == player.key(), "Invalid Signer"

    # check the correct player is taking their turn
    assert played_by == game_data.curr_player, "Invalid Player"

    # check that move is possible
    assert move_position > 0 and move_position < 10, "Invalid move, off the grid"

    # check that grid position iis unoccupied
    assert game_data.grid[move_position - 1] == 0, "Invalid move, position occupied"

    # # Next we move to our game logic. Firstly we decrement the move_position by one so it fits the zero indexing of the array. Then we mark the grid with the player's number. Next we check if the player has won. This logic will be separated out into a separate function win_check which we'll come to next. We also switch the current player. Lastly we print the status of the game based on the result of the win_check function.
    move_position -= 1

    game_data.grid[move_position] = game_data.curr_player

    game_status = win_check(Array(game_data.grid, len = 9), game_data.curr_player)

    if game_data.curr_player == 2:
        game_data.curr_player = 1
    else:
        game_data.curr_player = 2

    if(game_status == GameState.InProgress):
        print("Ready for next move")
    
    if(game_status == GameState.Player1Wins):
        game_data.game_status = 1
        print("Player1 wins")
    
    if(game_status == GameState.Player2Wins):
        game_data.game_status = 2
        print("Player2 wins")

    if(game_status == GameState.Draw):
        game_data.game_status = 3
        print("Draw")