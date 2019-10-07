import argparse
import importlib
import inspect
import glob

from objects.game_engine import HanabiEngine


def _get_player_classes():
    """Dynamically sources (for reference) the player classes defined in the player_objects module."""
    available_player_classes = [] 

    file_path='./player_types/'
    file_names = [f.split('/')[-1] for f in glob.glob(f'{file_path}*.py')]

    for f in file_names:
        if f.startswith("__"):
            continue
        module = importlib.import_module(f'.{f[:-3]}', package=file_path.split('/')[1])
        player_class = [member[0] for member in inspect.getmembers(module, inspect.isclass) if member[0] != 'Player']
        available_player_classes += player_class

    return available_player_classes

def validate_args(args, available_player_classes):
    """Validate the arguments passed from the command-line, so that only valid player classes (for example) can be
    specified.
    """
    # assert that the player classes passed from the command-line are valid
    for player_class in args.p:
        try:
            assert(player_class in available_player_classes)
        except AssertionError:
            print(f'Invalid player class: \'{player_class}\'. See help (-h) for available classes.')
            return False
    return True

def main(players, rainbow_as_sixth, is_test):
    """Sets up a new Hanabi game engine and runs the game."""
    hanabi = HanabiEngine(players=players, rainbow_as_sixth=rainbow_as_sixth, is_test=is_test)
    hanabi.run()


if __name__ == '__main__':

    available_player_classes = _get_player_classes()
    default_setup = 'Rando, Rando'

    parser = argparse.ArgumentParser(description='Simulate a game of Hanabi with between 2-5 players.',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-t',
                        action='store_true',
                        help='run in test mode: iterate a single round of all players and then exit')
    parser.add_argument('-r',
                        action='store_true',
                        help='include the rainbow suit as its own suit (default: False)')
    parser.add_argument('-p',
                        default=default_setup,
                        type=lambda p: [p for p in p.split(', ')],
                        help='enter 2-5 comma separated classes to set the number and type of players \n' \
                              + f'(default: a 2-player game specified as: -p \'{default_setup}\') \n' \
                              + f'available player classes are: {available_player_classes}')

    args = parser.parse_args()

    if validate_args(args, available_player_classes):
        main(players=args.p, rainbow_as_sixth=args.r, is_test=args.t)
