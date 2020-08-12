"""Contains Game, HumanPlayer, AIType, AIEasy and AIMiniMax classes.

AIType is parent class for AIEasy and AIMiniMax child classes.
"""

import random

from lib import gui
from lib.minimax_algorithm import MiniMax


class Game(object):
    """Tracks state of the game board, players move history and executes both player's moves."""
    
    def __init__(self, mode):
        self.mode = mode

        self.game_over = False
        self.winner = None # Will be 0=draw, 1=player, 2=Ai

        self.move_no = 1

        # 0=empty, 1=player, 2=AI
        self.board_matrix = [0,0,0,0,0,0,0,0,0]
        
        # Matrix of ways of winning
        self.win_matrix = [[0,1,2],# rows
                          [3,4,5],
                          [6,7,8],
                          [0,3,6],# columns
                          [1,4,7],
                          [2,5,8],
                          [0,4,8],# diagonals
                          [6,4,2],
                          ]
        
        if self.mode == 'easy':
            self.players = (HumanPlayer(self), AIEasy(self))
        elif self.mode == 'impossible':
            self.players = (HumanPlayer(self), AIMiniMax(self))
        
    def update(self, player_move):
        """Execute player's move and allow computer to take turn. Check for win after each turn."""
        if not player_move == None:
            self.players[0].update(player_move)
            self.move_no += 1
            self.check_win()
        if self.winner == None:
            self.players[1].update()
            self.move_no +=1
            self.check_win()

    def check_win(self):
        """Check for win, loose or draw."""
        # Check against win matrix if game is won or lost
        for player in [1,2]:
            for line in self.win_matrix:
                chain_len = 0
                for idx in line:
                    if self.board_matrix[idx] == player:
                        chain_len += 1
                        if chain_len == 3:
                            self.winner = player
                            return
                            
        # If empty sapce present then game is not over, otherwise its a draw
        for sqr in self.board_matrix:
            if sqr == 0:
                self.winner = None
                return
        self.winner = 0
        
     
class HumanPlayer(object):
    """Track and execute human player's moves."""

    def __init__(self, game):
        self.game = game
        self.moves = []

    def update(self, player_move):
        """Take player's move and update board matrix and moves list."""
        self.game.board_matrix[player_move] = 1
        self.moves.append(player_move)


class AIType(object):
    """Parent class for types of AI difficulty."""
    
    def __init__(self, game):
        self.game = game
        self.board_matrix = self.game.board_matrix
        self.win_matrix = self.game.win_matrix
        self.moves = []
        self.players = (1,2)

    def random(self):
        """Random method selects a move to make randomly from available squares on game board"""
        avail_squares = []
        for idx, sqr in enumerate(self.board_matrix):
            if sqr == 0:
                avail_squares.append(idx)
        nxt_move = random.choice(avail_squares)
        return nxt_move


class AIEasy(AIType):
    """Class for selecting and tracking moves when Easy difficulty setting selected in game menu"""
        
    def update(self):
        """Selects move by completing winning row, blocking user's winning row or otherwise
        randomly selecting an available tile. Then updates game board and list of moves."""
        nxt_move = self.win_or_block()
        if nxt_move == None:
            nxt_move = self.random()
        
        #Making move
        self.board_matrix[nxt_move] = 2
        self.moves.append(nxt_move)

    # If one move from winning or losing complete line to win or block.
    def win_or_block(self):
        """Checks for rows of 2 X's or O's where game could be won or user blocked from winning."""
        for p in reversed(self.players): #Reversed to check for winning moves before blocking moves.
            for line in self.win_matrix:
                chain_len = 0
                empty_sqr = None
                for idx in line:
                    if self.board_matrix[idx] == 0:
                        empty_sqr = idx
                    elif self.board_matrix[idx] == p:
                        chain_len += 1
                if chain_len == 2 and empty_sqr:
                    nxt_move = empty_sqr
                    return nxt_move
        return None


class AIMiniMax(AIType):
    """Class for managing computer's moves when impossible difficulty selected in game menu"""
    
    def __init__(self, game):
        AIType.__init__(self, game)
        
        self.minimax = MiniMax(self.win_matrix)
        self.moves_until_win = None
    
    def update(self):
        """Select move using minimax algorithm, update game board and list of moves."""
        if self.game.move_no == 1:
            nxt_move = self.random()
        else:
            minimax_score = self.minimax.minimax_scores(self.board_matrix)
            nxt_move = self.minimax.choice
            
            # If there is a guarenteed path to winnig then calculate remaining moves until win.
            if minimax_score > 0:
                self.moves_until_win = (9 - minimax_score)/2
        
        #Making move
        self.board_matrix[nxt_move] = 2
        self.moves.append(nxt_move)
