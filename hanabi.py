import argparse
import inspect

from game_engine import HanabiEngine
import player_strategies


AVAILABLE_STRATEGIES = [methods[0] for methods in inspect.getmembers(player_strategies, inspect.isfunction)]
DEFAULT_SETUP = ', '.join([AVAILABLE_STRATEGIES[0]]*2)


def validate_args(args):
    """
    """
    # assert that strategies passed from the command-line are valid
    for strategy in args.p:
        try:
            assert(strategy in AVAILABLE_STRATEGIES)
        except AssertionError:
            print(f'Invalid player strategy: \'{strategy}\'. See help (-h) for available strategies.')
            return False
    return True

def main(players, rainbow_as_sixth):
    """
    """
    hanabi = HanabiEngine(players=players, rainbow_as_sixth=rainbow_as_sixth)
    hanabi.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulate a game of Hanabi with between 2-5 players.',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-p',
                        default=DEFAULT_SETUP,
                        type=lambda p: [p for p in p.split(', ')],
                        help= 'enter a list of 2-5 strategies as a string to set the number and type of players \n' + \
                             f'(default: a 2-player game specified as: -p \'{DEFAULT_SETUP}\') \n' + \
                             f'available strategies are: {AVAILABLE_STRATEGIES}')
    parser.add_argument('-r',
                        action='store_true',
                        help='include the rainbow suit as its own suit (default: False)')

    args = parser.parse_args()

    if validate_args(args):
        main(players=args.p, rainbow_as_sixth=args.r)
