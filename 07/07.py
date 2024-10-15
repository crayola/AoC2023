from collections import Counter
from functools import cmp_to_key


def identify_nonjoker_hand_type(c):
    """
    Determines the type of hand in a card game based on the counts of each card
    rank. It returns an integer value representing the hand type, with higher
    values indicating stronger hands.

    Args:
        c (Dict[int, int]): Representing a dictionary where keys are card ranks
            and values are their respective counts in a hand of cards.

    Returns:
        int: A representation of a hand type in a card game, ranging from 0 to 6,
        where higher values indicate a stronger hand.

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
    Identifies the type of a poker hand based on its constituent cards, considering
    both joker and non-joker combinations, and returns a numerical representation
    of the hand type.

    Args:
        h (str | List[str]): Representing a poker hand, which is a sequence of
            cards, where each card is either a joker "J" or a card from a standard
            deck.
        part (int): Used to determine the type of hand being evaluated.

    Returns:
        int: An integer representing a specific hand type in a card game, ranging
        from 0 to 6, with each value corresponding to a particular hand type.

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
    Determines the relative ranking of two cards, c1 and c2, based on their card
    values, with option to consider 'J' as high or low value, depending on the
    value of the part parameter.

    Args:
        c1 (str): A character representing a card.
        c2 (str): Representing the rank of a second card in a card game, where it
            is compared to the rank of `c1` according to a specific ordering defined
            by the `part` parameter.
        part (int): Used to determine the card ordering: 'part == 1' uses a standard
            ordering (Ace to 2, then Jack to 10, Jack to 2), while 'part == 0'
            uses a non-standard ordering (Ace to King, then Jack to 2).

    Returns:
        int: -1 if c1 is of lower rank than c2,
        1 if c1 is of higher rank than c2,
        0 if c1 and c2 have the same rank.

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
    Compares two poker hands of five cards each. It first identifies the type of
    each hand, then compares them. If one hand is higher than the other, it returns
    1 or -1, respectively. If hands are equal, it compares each card in order,
    returning 1, -1, or 0 accordingly.

    Args:
        h1 (List[Card]): Representing a hand of cards with five elements, where
            each element is a Card object.
        h2 (List[Dict[str, int]]): Represented by a list of five dictionaries.
        part (str): Used to identify the type of hand being compared, which in
            turn determines how the hand types and card comparisons are handled.

    Returns:
        int: 1 if the first hand is better, -1 if the second hand is better, and
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
