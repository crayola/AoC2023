import math

def number_of_ways_to_win_1(time, distance):
    victories = [t for t in range(time+1) if (time - t) * t > distance]
    return len(victories)

def number_of_ways_to_win_2(time, distance):
    """
    Calculates the number of ways to win a game or reach a destination by finding
    the number of integer solutions to the equation `t = (x + y)`, where `t` is
    the time, `x` is the time taken to reach the destination, and `y` is the time
    taken to win the game.

    Args:
        time (float): Representing the time taken to cover the distance.
        distance (float): Defined as the product of the number of coins on one
            side of a board and the number of coins on the other side in a coin game.

    Returns:
        int: The number of ways to win a game, assuming that the game can be won
        with a certain time limit and a given distance.

    """
    return (
        1
        + math.floor((time + math.sqrt(time**2 - 4 * distance)) / 2.0)
        - math.ceil((time - math.sqrt(time**2 - 4 * distance)) / 2.0)
    )

if __name__ == "__main__":

    # part 1
    times, distances = [
        [int(y) for y in x.split(":")[1].strip().split()]
        for x in open("input").readlines()
    ]
    races = list(zip(times, distances))
    part1 = 1
    for r in races:
        part1 *= number_of_ways_to_win_1(*r)
    print(f"part 1: {part1}")

    # part 2
    time, distance = [
        int(x.split(":")[1].strip().replace(" ", "")) for x in open("input").readlines()
    ]

    part2 = number_of_ways_to_win_2(time, distance)
    print(f"part 2: {part2}")
