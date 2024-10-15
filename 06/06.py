import math

def number_of_ways_to_win_1(time, distance):
    """
    Calculates the number of ways a runner can win a race by having a faster average
    speed than the opponent. It takes time and distance as inputs and returns the
    count of valid times based on the condition (time - t) * t > distance.

    Args:
        time (int): Representing the maximum number of turns or moves available
            in a game, typically ranging from 1 to any positive integer. Its value
            determines the possible combinations of moves that can be made.
        distance (int): Used to calculate the number of ways a certain victory
            condition can be achieved in a race. The specific nature of this
            condition is not explicitly stated.

    Returns:
        int: The number of possible victories in a game, where each victory is
        represented by a valid time at which a player can win, given a maximum
        time and a distance.

    """
    victories = [t for t in range(time+1) if (time - t) * t > distance]
    return len(victories)

def number_of_ways_to_win_2(time, distance):
    """
    Calculates the number of possible ways to win a race, given the time and
    distance between two points. It uses the quadratic formula to find the roots
    of a quadratic equation, representing the time it takes to travel the distance.

    Args:
        time (float): Representing the time taken by a runner to cover a certain
            distance.
        distance (float): Interpreted as the coefficient `b` in the quadratic
            equation `at^2 + bt + c = 0`, where `a = 1` and `c = -distance`.

    Returns:
        int: The number of different ways to win a game given time and distance
        constraints, based on a quadratic equation solution.

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
