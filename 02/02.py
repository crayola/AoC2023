from pathlib import Path

from typing import Dict, List

input_path = Path('./input')

def part1_criterion(game_id, draws: List[Dict]):
    """
    Returns a value based on the game ID, but only if all draws in the list have
    colors within specified limits. If any draw exceeds these limits, the function
    immediately returns 0. The limits are 12 for red, 13 for green, and 14 for blue.

    Args:
        game_id (int): Converted to an integer using the `int()` function before
            being returned.
        draws (List[Dict]): Expected to contain a list of dictionaries, where each
            dictionary represents a draw and has keys 'red', 'green', and 'blue'
            representing the quantities of each color drawn.

    Returns:
        int|0: 0 if any draw has a color count exceeding the specified threshold,
        and the game ID otherwise.

    """
    for draw in draws:
        if draw.get('red', 0) > 12 or draw.get('green', 0) > 13 or draw.get('blue', 0) > 14:
            return 0
    return int(game_id)
    
def parse_game(game_str: str):
    """
    Parses a game string into a dictionary containing a game ID and a list of
    draws. The game string is expected to be in the format "ID: game;draw1;draw2;...".
    The function splits the string into game ID and draws, then splits the draws
    into individual strings and parses each one using the `parse_draw` function.

    Args:
        game_str (str): Expected to be a string containing a game ID and draws in
            a specific format, separated by a colon and semicolons respectively.

    Returns:
        Dict[str,Union[int,List[Dict[str,Any]]]]: A dictionary containing two
        key-value pairs: 'game_id' and 'draws'.

    """
    game_id, game = game_str.split(":")
    game_id = game_id.split(' ')[1]
    draws_str = game.split(';')
    draws = [parse_draw(draw) for draw in draws_str]
    return {'game_id': game_id, 'draws': draws}

def parse_draw(draw_str: str):
    """
    Transforms a string of comma-separated numbers and colors into a dictionary
    where keys are colors and values are corresponding numbers.

    Args:
        draw_str (str): Expected to be a comma-separated string where each part
            represents a number and its corresponding color, separated by a space.

    Returns:
        Dict[str,int]: A dictionary where keys are colors and values are integers
        representing the corresponding values in the draw string.

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
    Determines the maximum values of red, blue, and green draws from a list of
    dictionaries, then returns the product of these maximum values.

    Args:
        draws (List[Dict]): Represented as a list of dictionaries. Each dictionary
            represents a draw and contains keys for red, blue, and green, with
            their respective values.

    Returns:
        int: The product of the maximum number of red, blue, and green draws found
        in the input list of dictionaries.

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
