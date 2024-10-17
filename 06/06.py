import math

def number_of_ways_to_win_1(time, distance):
    """
    Calculates the number of possible times at which a race can be won, given a
    fixed time limit and a minimum distance requirement. It returns the count of
    valid times where the difference between the time limit and the winning time
    multiplied by the winning time exceeds the minimum distance.

    Args:
        time (int): Representing the available time for a racing competition.
        distance (int): Used in the calculation of the number of possible victories,
            representing the distance a runner has to cover. It is compared to the
            product of the remaining time and the number of rounds a runner has
            already won.

    Returns:
        int: The count of possible speeds at which a car can win a race, given a
        certain time limit and a minimum required distance.

    """
    victories = [t for t in range(time+1) if (time - t) * t > distance]
    return len(victories)

def number_of_ways_to_win_2(time, distance):
    """
    Calculates the number of ways to win a game on a circular track with a given
    time and distance. It uses the quadratic formula to find the solutions to a
    quadratic equation, which represent the positions where the game can be won.

    Args:
        time (float): Representing the time taken to complete a race, which is
            used in a formula to calculate the number of ways a player can win a
            game.
        distance (int): Interpreted as the coefficient of the squared term in a
            quadratic equation, representing the distance of a runner from the
            finish line.

    Returns:
        int: The number of possible ways to win a game, given time and distance constraints.

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
