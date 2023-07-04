from board import *
from player import *
import random


def main():
    board = Board()
    board.print_board()
    player_num = 1
    while not board.game_over():
        print(f'Player {player_num}\'s turn:')
        if player_num == 2:  # random player
            possible = board.possible_moves(player_num)
            move = random.choice(possible)
            # move = random.randint(0, 5)
        else:
            _, move = board.minimax(8, player_num, -1)
        new_board = board.make_move(player_num, move)
        print(f'Player {player_num} moved {move}.')
        new_board.print_board()
        print()
        board = new_board
        player_num = 2 if player_num == 1 else 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
