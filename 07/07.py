from collections import Counter
from functools import cmp_to_key


def identify_nonjoker_hand_type(c):
    """
    Determines the type of a poker hand based on the count of each card rank. It
    returns a value from 0 to 6, where 6 represents a straight flush, 5 a four of
    a kind, and so on, down to 0 for a high card hand.

    Args:
        c (Dict[int, int]): Represented as a dictionary where keys are card ranks
            (integer values) and values are their respective counts in a hand of
            cards.

    Returns:
        int: An integer representing the type of a non-joker poker hand.

    """
    maxcount = max(c.values())
    mincount = min(c.values())
    if maxcount == 5:
        return 6
    if maxcount == 4:
        return 5
    if maxcount == 3:
        return 4 if mincount == 2 else 3
    if maxcount == 2:
        return 2 if len([x for x in c.values() if x == 2]) == 2 else 1
    if maxcount == 1:
        return 0
    return 0


def identify_hand_type(h, part):
    """
    Classifies poker hands into specific types based on their composition of cards
    and jokers. It takes a hand of cards and a part identifier as input and returns
    a unique integer representing the hand type.

    Args:
        h (str): Used to represent a poker hand, presumably consisting of a
            combination of card values and possibly "J" to represent a joker.
        part (int): Used to determine the hand type when a joker is present. It
            is used as a condition to decide the hand type based on the number of
            jokers in the hand.

    Returns:
        int: An integer representing the type of hand in a card game, with higher
        values indicating stronger hands.

    """
    c = Counter(h)
    if h == "JJJJJ":
        return 6
    c_nojoker = Counter([c for c in h if c != "J"])
    njtype = identify_nonjoker_hand_type(c_nojoker)
    if part == 1 or "J" not in h:
        return njtype
    else:
        num_jokers = c["J"]
        if num_jokers == 4:
            return 6
        if num_jokers == 3:
            return 6 if njtype == 1 else 5
        if num_jokers == 2:
            return 6 if njtype == 3 else (5 if njtype == 1 else 3)
        if num_jokers == 1:
            return njtype + 1 if njtype in [0, 5] else njtype + 2
    return 0


def compare_cards(c1, c2, part):
    """
    Compares the priority of two cards in a given game part. It uses a predefined
    ordering string to determine the relative values of the cards, returning -1
    if the first card has lower priority, 1 if it has higher priority, and 0 if
    they have equal priority.

    Args:
        c1 (str): Representing the rank of the first card to be compared, where
            the rank can be any of the letters A, K, Q, J, T, 9, 8, 7, 6, 5, 4,
            or 3.
        c2 (str): Used to represent the rank of a card to be compared with the
            rank of another card, c1.
        part (int): Used to determine the ordering of cards in a poker game. It
            is used to decide whether to include the Jack (J) in the ordering, as
            its position is different in two-part and three-part ordering systems.

    Returns:
        int: -1 if the first card has a lower ranking than the second,
        1 if the first card has a higher ranking than the second,
        or 0 if the two cards have the same ranking.

    """
    ordering = "AKQJT98765432" if part == 1 else "AKQT98765432J"
    ind1, ind2 = ordering.index(c1), ordering.index(c2)
    if ind1 > ind2:
        return -1
    if ind1 < ind2:
        return 1
    return 0


def compare_hands(h1, h2, part):
    """
    Compares two poker hands, `h1` and `h2`, based on their types and individual
    card values. It returns 1 if `h1` is higher, -1 if `h2` is higher, and 0 if
    they are equal.

    Args:
        h1 (List[Card]): Presumably a list of 5 cards representing a poker hand.
        h2 (List[Dict[str, any]]): Represented as a list of five dictionaries,
            each dictionary containing information about a card in the hand, such
            as its type or rank.
        part (str): Passed to the `identify_hand_type` and `compare_cards` functions.
            Its purpose is to specify the part of the hand being compared, such
            as the high card or the kicker.

    Returns:
        int: 1 if the first hand is stronger than the second,
        -1 if the first hand is weaker, and
        0 if the hands are equal.

    """
    h1_type, h2_type = identify_hand_type(h1, part), identify_hand_type(h2, part)
    if h1_type > h2_type:
        return 1
    if h1_type < h2_type:
        return -1
    for i in range(5):
        c1, c2 = h1[i], h2[i]
        if compare_cards(c1, c2, part) == 1:
            return 1
        if compare_cards(c1, c2, part) == -1:
            return -1
    return 0


if __name__ == "__main__":
    hands_bids = [x.split() for x in open("input").readlines()]

    # part 1
    hands_bids.sort(key=cmp_to_key(lambda x1, x2: compare_hands(x1[0], x2[0], part=1)))
    part1 = 0
    for i, hand_bid in enumerate(hands_bids, 1):
        hand, bid = hand_bid
        bid = int(bid)
        part1 += i * bid
    print(f"part 1: {part1}")

    # part 2
    hands_bids.sort(key=cmp_to_key(lambda x1, x2: compare_hands(x1[0], x2[0], part=2)))
    part1 = 0
    for i, hand_bid in enumerate(hands_bids, 1):
        hand, bid = hand_bid
        bid = int(bid)
        part1 += i * bid
    print(f"part 2: {part1}")
