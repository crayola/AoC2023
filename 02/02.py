from pathlib import Path

from typing import Dict, List

input_path = Path('./input')

def part1_criterion(game_id, draws: List[Dict]):
    """
    Evaluates a set of draws for a specific game ID. It checks each draw for
    excessive red, green, or blue values and returns 0 if any draw exceeds these
    limits. Otherwise, it returns the game ID as an integer.

    Args:
        game_id (int): Converted to an integer using `int(game_id)` before being
            returned as the function result.
        draws (List[Dict]): Expected to be a list of dictionaries, where each
            dictionary represents a single draw with keys 'red', 'green', and
            'blue' representing the quantities of each color drawn.

    Returns:
        int|0: 0 if any draw in the list exceeds the specified color limits,
        otherwise the integer value of the game_id.

    """
    for draw in draws:
        if draw.get('red', 0) > 12 or draw.get('green', 0) > 13 or draw.get('blue', 0) > 14:
            return 0
    return int(game_id)
    
def parse_game(game_str: str):
    """
    Parses a string representation of a game into a dictionary containing the game
    ID and a list of draws, where each draw is parsed by the `parse_draw` function.

    Args:
        game_str (str): Expected to contain a string representation of a game.

    Returns:
        Dict[str,Union[int,List[Dict[str,Any]]]]: A dictionary with two key-value
        pairs: 'game_id' and 'draws'. The 'game_id' key maps to a string, and the
        'draws' key maps to a list of dictionaries.

    """
    game_id, game = game_str.split(":")
    game_id = game_id.split(' ')[1]
    draws_str = game.split(';')
    draws = [parse_draw(draw) for draw in draws_str]
    return {'game_id': game_id, 'draws': draws}

def parse_draw(draw_str: str):
    """
    Takes a string of comma-separated values, parses it into a dictionary, and
    returns the dictionary containing the drawn numbers and their corresponding colors.

    Args:
        draw_str (str): Expected to be a comma-separated string containing
            space-separated values representing numbers and colors.

    Returns:
        Dict[str,int]: A dictionary with string keys representing colors and integer
        values representing drawn numbers.

    """
    draw = {}
    draw_str = draw_str.split(',')
    for d in draw_str:
        d = d.strip()
        value, color = d.split(' ')
        draw[color] = int(value)
    return draw

def calculate_power(draws: List[Dict]):
    """
    Determines the maximum power by finding the maximum number of red, blue, and
    green draws from a list of dictionaries, where each dictionary represents a
    draw and contains keys for the number of each color drawn.

    Args:
        draws (List[Dict]): Expected to contain a list of dictionaries where each
            dictionary represents a draw and contains keys for the color 'red',
            'blue', and 'green' with integer values.

    Returns:
        int: The product of the maximum values of 'red', 'blue', and 'green' drawn
        in all the sets.

    """
    reds = 0
    blues = 0
    greens = 0
    for d in draws:
        reds = max(reds, d.get('red', 0))
        blues = max(blues, d.get('blue', 0))
        greens = max(greens, d.get('green', 0)) 
    return reds * blues * greens


if __name__ == '__main__':
    lines = open(input_path).readlines()
    part_1 = 0
    part_2 = 0
    for x in lines:
        part_1 += part1_criterion(**parse_game(x))
        part_2 += calculate_power(parse_game(x)['draws'])
    print(f'part 1: {part_1}')
    print(f'part 2: {part_2}')
