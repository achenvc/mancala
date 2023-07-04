from player import *


class Board:
    depth = 10

    def __init__(self):
        self.NUM_TILES = 6
        self.scores = [0, 0]
        self.p1_board = [4] * self.NUM_TILES
        self.p2_board = [4] * self.NUM_TILES

    def reset(self):
        self.NUM_TILES = 6
        self.scores = [0, 0]
        self.p1_board = [4] * self.NUM_TILES
        self.p2_board = [4] * self.NUM_TILES

    def print_board(self):
        p1_side = ""
        for tile in self.p1_board:
            p1_side += str(tile) + "    "
        p2_side = ""
        for tile in self.p2_board:
            p2_side += str(tile) + "    "
        print(p1_side)
        print(p2_side)
        print(f'PLAYER 1: {self.scores[0]}    PLAYER 2: {self.scores[1]}')

    def game_over(self):
        # checks if game is over
        # game is only over if one side's tiles has no more pebbles
        is_over = True
        for tile in self.p1_board:
            if tile > 0:
                is_over = False
        if is_over:
            return True

        is_over = True
        # else, check player 2's board
        for tile in self.p2_board:
            if tile > 0:
                is_over = False
        return is_over

    def possible_moves(self, player_num):
        if player_num == 1:
            tiles = self.p1_board
        else:
            tiles = self.p2_board
        return [i for i in range(self.NUM_TILES) if tiles[i] > 0]

    def make_move(self, player_num, move):
        new_board = Board()
        new_board.p1_board = self.p1_board.copy()
        new_board.p2_board = self.p2_board.copy()
        new_board.scores = self.scores.copy()

        if player_num == 1:
            side = 1
            p_tiles = new_board.p1_board
            o_tiles = new_board.p2_board
        else:
            side = 2
            p_tiles = new_board.p2_board
            o_tiles = new_board.p1_board

        pebbles = p_tiles[move]
        p_tiles[move] = 0

        curr_tiles = p_tiles

        move += 1
        while pebbles > 0:
            if move < len(p_tiles):
                curr_tiles[move] += 1
                pebbles -= 1
                move += 1
            else:  # on opp side now
                if player_num == side:
                    new_board.scores[player_num - 1] += 1
                pebbles -= 1
                move = 0
                side = 1 if side == 2 else 2
                curr_tiles = o_tiles if side != player_num else p_tiles

        # check if we ended up on a blank space
        if player_num == side and move != 0 and p_tiles[move - 1] == 1:
            # if so, steal opponent's opposite tiles
            opp_tiles = o_tiles[move - 1]
            new_board.scores[player_num - 1] += (opp_tiles + 1)
            o_tiles[move - 1] = 0
            p_tiles[move - 1] = 0

        return new_board

    def who_won(self):
        if not self.game_over():
            return -1, 0
        else:
            score_diff = self.scores[0] - self.scores[1]
            if score_diff == 0:
                return 0, score_diff  # tie
            else:
                winner = 1 if score_diff > 0 else 2
                return winner, score_diff

    def eval_board(self):
        winner, _ = self.who_won()
        if winner == 1:  # player 1 (max) wins
            return 100
        elif winner == 2:
            return -100
        else:
            # using heuristics
            return self.scores[0] - self.scores[1] # reward if we have more points than opponent

    def count_potential_captures(self, num_player):
        # find indexes of 0s
        res = 0
        if num_player == 1:
            tiles = self.p1_board
        else:
            tiles = self.p2_board
        zeroes = [i for i in range(self.NUM_TILES) if tiles[i] == 0]
        for i in range(self.NUM_TILES):
            if i + tiles[i] in zeroes:
                res += 1
        return res


    def minimax(self, depth, num_player, move):
        if depth == 0 or self.game_over():
            return self.eval_board(), move

        if num_player == 1:  # maximizing player
            max_eval = -10000
            max_move = -1
            for move in self.possible_moves(num_player):
                new_board = self.make_move(num_player, move)
                eval, _ = new_board.minimax(depth - 1, 2, max_move)
                if eval > max_eval:
                    max_eval = eval
                    max_move = move

            return max_eval, max_move

        if num_player == 2:  # minimizing player
            min_eval = 10000
            min_move = -1
            for move in self.possible_moves(num_player):
                new_board = self.make_move(num_player, move)
                eval, _ = new_board.minimax(depth - 1, 1, min_move)
                if eval < min_eval:
                    min_eval = eval
                    min_move = move
            return min_eval, min_move
