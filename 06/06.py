import math

def number_of_ways_to_win_1(time, distance):
    """
    Calculates the number of valid racing times, given a maximum time and a distance.
    It returns the count of times where the difference between the maximum time
    and the valid time is greater than the distance.

    Args:
        time (int): Representing the total amount of time available to complete a
            race or a certain activity.
        distance (int): Assumed to be the maximum distance a runner can cover in
            a given time.

    Returns:
        int: The number of possible speeds at which a race can be won, given a
        time limit and a distance.

    """
    victories = [t for t in range(time+1) if (time - t) * t > distance]
    return len(victories)

def number_of_ways_to_win_2(time, distance):
    """
    Calculates the number of ways to win a game, where a win is achieved by crossing
    a certain distance within a given time, using a quadratic equation to find the
    number of possible steps.

    Args:
        time (float): Representing the time it takes to walk a certain distance.
        distance (int): Used in the quadratic formula to calculate the discriminant.

    Returns:
        int: The number of distinct ways a character can move from one position
        to another, given the time and distance constraints.

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
