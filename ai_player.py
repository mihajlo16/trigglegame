
from enums import Player, Direction
from copy import deepcopy
from board import draw_and_update
import math

class AIPlayer:
    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def choose_best_move(self, game):
        _, best_move = self.minimax(game, self.max_depth, -math.inf, math.inf, True)
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.board.gameFinished:
            return self.evaluate(game, Player.X), None

        best_move = None
        moves = game.generate_all_moves()

        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                new_game = deepcopy(game)
                letter, number, direction = new_game.split_position(move)
                xPoints, oPoints, success = draw_and_update(
                    new_game.board.board,
                    new_game.board.boardSize,
                    new_game.board.branchState,
                    new_game.board.triggleState,
                    new_game.board.currentPlayer,
                    letter, number, direction,
                    False
                )
                if not success:
                    continue
                new_game.board.xPoints += xPoints
                new_game.board.oPoints += oPoints
                new_game.board.currentPlayer = Player.O if new_game.board.currentPlayer == Player.X else Player.X

                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in moves:
                new_game = deepcopy(game)
                letter, number, direction = new_game.split_position(move)
                xPoints, oPoints, success = draw_and_update(
                    new_game.board.board,
                    new_game.board.boardSize,
                    new_game.board.branchState,
                    new_game.board.triggleState,
                    new_game.board.currentPlayer,
                    letter, number, direction,
                    False
                )
                if not success:
                    continue
                new_game.board.xPoints += xPoints
                new_game.board.oPoints += oPoints
                new_game.board.currentPlayer = Player.O if new_game.board.currentPlayer == Player.X else Player.X

                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, game, player):
        x = game.board.xPoints
        o = game.board.oPoints
        my_score = x if player == Player.X else o
        opponent_score = o if player == Player.X else x
        remaining = sum(1 for t in game.board.triggleState.values() if t['igracKojiJeZauzeo'] == Player.N)
        return (my_score - opponent_score) + 0.01 * remaining
