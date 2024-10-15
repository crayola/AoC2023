from pathlib import Path

from typing import Dict, List

input_path = Path('./input')

def part1_criterion(game_id, draws: List[Dict]):
    """
    Checks each draw in the list to see if any of the color quantities exceed their
    respective maximums (red: 12, green: 13, blue: 14). If any exceed, it returns
    0; otherwise, it returns the game ID as an integer.

    Args:
        game_id (int): Converted to an integer before being returned as the
            function's result.
        draws (List[Dict]*): Expected to be a list of dictionaries, where each
            dictionary represents a draw and contains keys for 'red', 'green', and
            'blue' with their respective values.

    Returns:
        int|0: 0 if any draw in the list exceeds its color limit, and the game_id
        as an integer otherwise.

    """
    for draw in draws:
        if draw.get('red', 0) > 12 or draw.get('green', 0) > 13 or draw.get('blue', 0) > 14:
            return 0
    return int(game_id)
    
def parse_game(game_str: str):
    """
    Breaks down a string representation of a game into its constituent parts. It
    extracts the game ID, splits the game into individual draws, and parses each
    draw into a structured format.

    Args:
        game_str (str*): Expected to contain a string representing a game, where
            the game is separated from its ID by a colon, and different draws are
            separated by semicolons.

    Returns:
        Dict[str,Union[str,List[Dict]]]: A dictionary containing two key-value pairs:
        - `game_id`: a string representing the unique identifier of the game.
        - `draws`: a list of dictionaries, where each dictionary represents a draw
        in the game.

    """
    game_id, game = game_str.split(":")
    game_id = game_id.split(' ')[1]
    draws_str = game.split(';')
    draws = [parse_draw(draw) for draw in draws_str]
    return {'game_id': game_id, 'draws': draws}

def parse_draw(draw_str: str):
    """
    Transforms a comma-separated string of drawing elements into a dictionary where
    keys are colors and values are corresponding integer values.

    Args:
        draw_str (str*): Represented as a string of comma-separated values, where
            each value is a space-separated pair of a number and a color.

    Returns:
        Dict[str,int]: A dictionary where keys are colors and values are integers
        representing the corresponding draw values.

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
    Determines the maximum number of red, blue, and green balls drawn in a series
    of draws and returns their product. It assumes each draw is a dictionary with
    keys 'red', 'blue', and 'green' representing the number of each color drawn.

    Args:
        draws (List[Dict]*): Expected to be a list of dictionaries, where each
            dictionary represents a draw and contains keys 'red', 'blue', and
            'green' with integer values.

    Returns:
        int: The product of the maximum number of red, blue, and green draws across
        all input dictionaries.

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
