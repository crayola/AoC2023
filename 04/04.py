from collections import defaultdict


def calculate_intersect_size(card: str):
    """
    Calculates the size of the intersection set between two sets of cards, one
    considered winning and the other a draw, based on their split card values.

    Args:
        card (str*): Assumed to be a string containing two cards separated by a
            "|" character, where each card is a space-separated string of items.

    Returns:
        int: The size of the intersection between the winning and draw sets of cards.

    """
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
