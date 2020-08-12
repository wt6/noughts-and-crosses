"""Contains MiniMax class for choosing moves based upon Minimax algorithm"""

import random


class MiniMax(object):
    """Class for performing ranking of available moves using Minimax algorithm."""
    
    def __init__(self, win_matrix):
        self.players = (1,2)
        self.calc_depth = 9
        self.win_matrix = win_matrix
        self.choice = None

    def minimax_scores(self, board_matrix, player_turn=2, depth=0):
        """Calculates scores recursively.

        Returns highest scoring move on computer's turn, or lowest on user's turn
        """
        # Check for winner and get list of possible next moves
        winner = self.find_winner(board_matrix)
        moves = self.get_avail_moves(board_matrix)

        # For base case where there is a winner return the score
        if winner != None or moves == []:
            return self.score(winner, depth)

        # Limits depth level of recursion to user defined limit
        if depth >= self.calc_depth:
            return 0

        if player_turn == 1:
            nxt_player = 2
        else:
            nxt_player = 1

        # Populate the scores list, recursing as needed
        scores = []
        for idx, move in enumerate(moves):
            game_state = board_matrix[:]
            game_state[move] = player_turn
            scores.append(self.minimax_scores(game_state, player_turn=nxt_player, depth=depth+1))

        # Get min or max score and if computer's turn select choice for next move
        if player_turn == 1:
            score = self.get_min_score(scores)
        elif player_turn == 2:
            score = self.get_max_score(scores)
            idx_best_scores = [i for i, x in enumerate(scores) if x == score]
            self.choice = moves[random.choice(idx_best_scores)]
        return score

    def get_avail_moves(self, board_matrix):
        """Generates list of available moves for given board matrix."""
        moves = []
        for idx, sqr in enumerate(board_matrix):
            if sqr == 0:
                moves.append(idx)
        return moves

    def find_winner(self, board_matrix):
        """Takes board matrix and retuns which player has won"""
        for p in self.players:
            for line in self.win_matrix:
                num_in_line = 0
                for idx in line:
                    if board_matrix[idx] == p:
                        num_in_line += 1
                    if num_in_line == 3:
                        return p
        return None

    def score(self, winner, depth):
        """Returns Minimax score"""
        if winner == 1:
            return -10 + depth
        elif winner == 2:
            return 10 - depth
        else:
            return 0

    def get_min_score(self, scores):
        """Takes list of scores and returns lowest score"""
        lowest_score = scores[0]
        for score in scores:
            if score < lowest_score:
                lowest_score = score
        return lowest_score

    def get_max_score(self, scores):
        """Takes list of scores and returns highest score"""
        highest_score = scores[0]
        for score in scores:
            if score > highest_score:
                highest_score = score
        return highest_score

    def set_depth(self, depth):
        """Sets calculation depth of algorithm to provided value"""
        self.calc_depth = depth
