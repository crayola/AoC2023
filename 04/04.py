from collections import defaultdict


def calculate_intersect_size(card: str):
    winning, draw = [x.split() for x in card.split("|")]
    intersect = set(winning) & set(draw)
    return len(intersect)


if __name__ == "__main__":
    lines = open("input").readlines()

    part1_values = [
        2 ** (calculate_intersect_size(line.split(":")[1]) - 1)
        for line in lines
        if calculate_intersect_size(line) > 0
    ]
    part1_sum = sum(part1_values)
    print(f"part 1: {part1_sum}")

    copies = defaultdict(int)
    for line in lines:
        card_number_str, card = line.split(":")
        card_number = int(card_number_str.split(" ")[-1])
        copies[card_number] += 1
        intersect_size = calculate_intersect_size(card)
        for i in range(intersect_size):
            copies[card_number + i + 1] += copies[card_number]
    print(f"part 2: {sum(copies.values())}")
