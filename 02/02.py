from pathlib import Path

from typing import Dict, List

input_path = Path('./input')

def part1_criterion(game_id, draws: List[Dict]):
    """
    Checks if a given game ID meets certain criteria based on the number of red,
    green, and blue draws. It iterates through a list of draws, ensuring none
    exceed specified thresholds. If any draw exceeds the threshold, the function
    returns 0; otherwise, it returns the integer value of the game ID.

    Args:
        game_id (int): Passed as an integer to the function, where it is implicitly
            converted to an integer using the `int()` function before being returned.
        draws (List[Dict]*): Expected to be a list of dictionaries, where each
            dictionary represents a draw and may contain keys 'red', 'green', and
            'blue' representing the quantities of each color drawn.

    Returns:
        int|0: 0 if any of the color quantities in the draws exceed their respective
        maximums, otherwise the integer value of game_id.

    """
    for draw in draws:
        if draw.get('red', 0) > 12 or draw.get('green', 0) > 13 or draw.get('blue', 0) > 14:
            return 0
    return int(game_id)
    
def parse_game(game_str: str):
    """
    Parses a string representing a game into a dictionary containing the game's
    ID and a list of draws. It splits the input string, extracts the game ID, and
    uses a helper function `parse_draw` to process each draw.

    Args:
        game_str (str*): Expected to be a string containing game information in a
            specific format, where it is split into game ID and draws by a colon
            and semicolon respectively.

    Returns:
        Dict[str,Union[str,List[Dict]]]: A dictionary containing two keys: 'game_id'
        and 'draws'.
        The value of 'game_id' is a string representing the game ID.
        The value of 'draws' is a list of dictionaries, each representing a draw
        in the game.

    """
    game_id, game = game_str.split(":")
    game_id = game_id.split(' ')[1]
    draws_str = game.split(';')
    draws = [parse_draw(draw) for draw in draws_str]
    return {'game_id': game_id, 'draws': draws}

def parse_draw(draw_str: str):
    """
    Parses a string of comma-separated values into a dictionary, where each key
    is a color and the corresponding value is the number associated with it.

    Args:
        draw_str (str*): Represented as a string containing comma-separated values,
            where each value is in the format 'number color'.

    Returns:
        Dict[str,int]: A dictionary where keys are colors and values are corresponding
        drawing values.

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
    Calculates the product of the maximum values of red, blue, and green draws
    from a list of dictionaries.

    Args:
        draws (List[Dict]*): Represented as a list of dictionaries, where each
            dictionary contains key-value pairs representing the number of red,
            blue, and green draws.

    Returns:
        int: The product of the maximum values of red, blue, and green from the
        input list of dictionaries.

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
