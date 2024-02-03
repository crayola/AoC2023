import math

def number_of_ways_to_win_1(time, distance):
    """
    The given function `number_of_ways_to_win_1(time`, distance`) calculates the
    number of ways to win a game or race with `time` rounds/laps and `distance`
    total distance to cover by each player/vehicle. It does this by checking if
    the remaining distance to cover (calculated as `(time - t) * t`) is greater
    than or equal to `distance`, for all possible values of `t` between `0` and
    `time + 1`.

    Args:
        time (int): The `time` input parameter specifies the number of turns that
            have already been played. It is used to determine which moves are
            possible and to calculate the number of ways to win.
        distance (int): The `distance` parameter determines the minimum number of
            wins required for a player to win the game. The function returns the
            number of ways a player can win the game with at most `time` wins if
            they have already won `distance` games.

    Returns:
        int: The output returned by the function `number_of_ways_to_win_1(time=3)(distance=6)`
        would be 2 because there are two ways to achieve a total distance of 6
        using three turns: (3 and 0) or (1 and 2 and 1).

    """
    victories = [t for t in range(time+1) if (time - t) * t > distance]
    return len(victories)

def number_of_ways_to_win_2(time, distance):
    """
    This function calculates the number of ways to win a game by finding the number
    of positive integer solutions to the equation x^2 - 4 Dy = 0 when x and y are
    both non-negative. It takes two parameters: time (a positive real number) and
    distance (a positive real number). The function first computes the square root
    of time minus distance and then finds the number of solutions to the equation
    using mathematical floor and ceiling functions.

    Args:
        time (float): The `time` input parameter represents the time it takes for
            the entity to move the given distance. It is used to calculate the
            square root of the time and distance combinations to find the number
            of ways the entity can win.
        distance (float): The `distance` input parameter determines the maximum
            allowed difference between the current time and the time at which the
            player must reach their destination to win the game.

    Returns:
        int: The output returned by the function `number_of_ways_to_win_2` is 1.

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
