from collections import Counter
from functools import cmp_to_key


def identify_nonjoker_hand_type(c):
    """
    Determines the type of a poker hand based on the count of each card rank,
    excluding the joker. It returns an integer value representing the hand type,
    ranging from 0 (no pairs) to 6 (five of a kind).

    Args:
        c (Dict[int, int]): Representing a dictionary where keys are card ranks
            and values are their respective counts in a hand of cards.

    Returns:
        int: Representing a hand type in a card game, with values ranging from 0
        to 6, indicating different hand types such as a pair, three of a kind, etc.

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
    Determines the type of hand based on a given poker hand and its part, considering
    both Joker and non-Joker hands. It uses a counter to count the occurrences of
    each card and a helper function to identify non-Joker hand types.

    Args:
        h (str | List[str]): Representing a poker hand, where each character in
            the string or each element in the list represents a card in the hand.
        part (int): Used to determine the specific hand type when the hand contains
            jokers.

    Returns:
        int: A numerical identifier representing the type of poker hand.

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
    Compares two cards in a standard deck based on their ranking. It returns -1
    if the first card has a higher rank, 1 if the second card has a higher rank,
    and 0 if the ranks are equal, depending on the specified part of the deck.

    Args:
        c1 (str): A card rank, which can be any of the characters A, K, Q, J, T,
            9, 8, 7, 6, 5, 4, or 3.
        c2 (str): Representing the rank of a second card in a card game.
        part (int): Determining the ordering of card values. A value of 1 corresponds
            to a standard ordering where Jack is lower than Ten, while a value of
            2 corresponds to a non-standard ordering where Jack is higher than Ten.

    Returns:
        int: -1 if the first card is of lower rank than the second card,
        1 if the first card is of higher rank than the second card,
        or 0 if both cards have the same rank.

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
    Compares two poker hands of a specified part (e.g., high card, pair, two pair)
    and returns a value indicating the relative strength of the hands: 1 if the
    first hand is stronger, -1 if the second hand is stronger, and 0 if they are
    equal.

    Args:
        h1 (List[Card]): Represented as a list of five elements, each element being
            a Card object.
        h2 (List[Card]): Represented by the variable `h2` in the function. It
            represents the second hand being compared to the first hand.
        part (str): Used as an argument in the `identify_hand_type` and `compare_cards`
            functions, possibly to specify the type of comparison to be made, such
            as the community cards in a poker game.

    Returns:
        int: -1 if the first hand is weaker than the second hand,
        1 if the first hand is stronger than the second hand,
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
