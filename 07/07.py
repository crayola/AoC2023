from collections import Counter
from functools import cmp_to_key


def identify_nonjoker_hand_type(c):
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
    ordering = "AKQJT98765432" if part == 1 else "AKQT98765432J"
    ind1, ind2 = ordering.index(c1), ordering.index(c2)
    if ind1 > ind2:
        return -1
    if ind1 < ind2:
        return 1
    return 0


def compare_hands(h1, h2, part):
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
