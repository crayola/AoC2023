from pathlib import Path

from typing import Dict, List

input_path = Path('./input')

def part1_criterion(game_id, draws: List[Dict]):
    for draw in draws:
        if draw.get('red', 0) > 12 or draw.get('green', 0) > 13 or draw.get('blue', 0) > 14:
            return 0
    return int(game_id)
    
def parse_game(game_str: str):
    game_id, game = game_str.split(":")
    game_id = game_id.split(' ')[1]
    draws_str = game.split(';')
    draws = [parse_draw(draw) for draw in draws_str]
    return {'game_id': game_id, 'draws': draws}

def parse_draw(draw_str: str):
    draw = {}
    draw_str = draw_str.split(',')
    for d in draw_str:
        d = d.strip()
        value, color = d.split(' ')
        draw[color] = int(value)
    return draw

def calculate_power(draws: List[Dict]):
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
