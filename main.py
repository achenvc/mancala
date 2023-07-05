from board import *
from player import *
import random
import argparse

DEPTH = 8
NUM_GAMES = 20


def main(args):
    global DEPTH
    global NUM_GAMES

    player_num = 1
    if args.play_games:
        p1_wins = 0  # ai
        p2_wins = 0  # random
        for i in range(NUM_GAMES):
            board = Board()
            while not board.game_over():
                if player_num == 2:  # random player
                    possible = board.possible_moves(player_num)
                    move = random.choice(possible)
                else:
                    # _, move = board.minimax(DEPTH, player_num, -1)
                    _, move = board.alphabeta(DEPTH, 1, -10000, 10000, -1)
                board = board.make_move(player_num, move)
                player_num = 2 if player_num == 1 else 1

            player, score_diff = board.who_won()
            if player == 1:
                p1_wins += 1
            else:
                p2_wins += 1
            print(str(score_diff), end=" ")

    else:
        board = Board()
        board.print_board()
        while not board.game_over():
            print(f'Player {player_num}\'s turn:')
            if player_num == 2:  # random player
                possible = board.possible_moves(player_num)
                move = random.choice(possible)
                # move = random.randint(0, 5)
            else:
                # _, move = board.minimax(DEPTH, player_num, -1)
                _, move = board.alphabeta(DEPTH, 1, -10000, 10000, -1)
            new_board = board.make_move(player_num, move)
            print(f'Player {player_num} moved {move}.')
            new_board.print_board()
            print()
            board = new_board
            player_num = 2 if player_num == 1 else 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--play_games', action='store_true')
    args = parser.parse_args()
    main(args)
