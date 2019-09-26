#!/usr/bin/env python3
"""
A go game instance.

"""
class GoMatch:
    def __init__(self, boardsize=None):
        """
        Initialize the match.

        """
        if boardsize not in [9, 13, 19]:
            raise ValueError('Board size not in 9, 13, 19')

        self._boardsize = boardsize

        self._board = dict()

        self._setup_board()

    def _setup_board(self):
        """
        Setup the game board.

        """
        field_entry = {
            'owner': None
        }
        for x in range(self._boardsize + 2):
            x_str = 'x_{}'.format(x)

            self._board[x_str] = dict()

            for y in range(self._boardsize + 2):
                y_str = 'y_{}'.format(y)

                self._board[x_str][y_str] = dict(field_entry)

    def assign_white(self, player_id=None):
        """
        Assign the white player.

        """
        return self._assign_player(color='white', player_id=player_id)

    def assign_black(self, player_id=None):
        """
        Assign the white player.

        """
        return self._assign_player(color='black', player_id=player_id)

    def _assign_player(self, color=None, player_id=None):
        """
        Assign a player id to a color.

        """
        if color not in ['white', 'black']:
            raise ValueError('Can only assign "black" or "white" as color')

        if not player_id:
            raise ValueError('Missing player_id')
