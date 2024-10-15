def get_mapped_value(x, map_list):
    """
    Maps a given value `x` within a specified range to a new value based on a list
    of mappings. Each mapping is defined by a tuple containing a reference value,
    a lower bound, and an upper bound.

    Args:
        x (int): Represented as a variable that holds a value to be checked against
            a list of mappings.
        map_list (List[Tuple[int, int, int]]): Used to define a list of mappings,
            where each mapping is a tuple containing three integers.

    Returns:
        int|str: Either the input value `x` if it does not match any mapping in
        the `map_list`, or a calculated value by applying a linear transformation
        to `x` based on the mapping that matches.

    """
    for m in map_list:
        if x < m[1] or x > m[1] + m[2]:
            continue
        else:
            return m[0] + x - m[1]
    return x            

def get_mapped_ranges(range, map_list):
    """
    Takes a time range and a list of map ranges, and returns a list of non-overlapping
    time ranges that cover the original range, taking into account the map ranges'
    start and end times, and their durations.

    Args:
        range (List[int]): Representing a time interval with a start time (`range[0]`)
            and a duration (`range[1]`).
        map_list (List[List[int]]): Used to represent a list of intervals, where
            each interval is defined by a list of three integers: the start of the
            interval, the duration of the interval, and an unknown value.

    Returns:
        List[List[int]]: A list of non-overlapping ranges that cover the entire
        input `range` and are mapped to the input `map_list`.

    """
    mapped_ranges = []

    map_list = [m for m in map_list if not (range[0] > m[1] + m[2] or range[0] + range[1] < m[1])] 

    runner = range[0]
    limit = range[0] + range[1]
    for map in map_list:
        if runner > map[1] + map[2]:
            continue
        if runner >= map[1] and runner <= map[1] + map[2]:
            mapped_ranges.append([map[0] + runner - map[1], min(limit - runner, map[2] - runner + map[1])])
            runner = map[1] + map[2] 
        if runner < map[1]:
            mapped_ranges.append([runner, map[1]-runner])
            runner = map[1] 
    
    if runner < limit:
        mapped_ranges.append([runner, limit-runner])

    return mapped_ranges


def get_all_mapped_ranges(range_list, map_list):
    """
    Processes a list of ranges and maps each range to a corresponding list of
    mapped ranges using the `get_mapped_ranges` function, then combines the results
    into a single list.

    Args:
        range_list (List[Dict[str, int]]): Expected to contain a list of dictionaries,
            where each dictionary represents a range and has string keys and integer
            values.
        map_list (List[Dict[int, int]]): Used to represent a list of mappings,
            where each mapping is a dictionary containing a range and its corresponding
            mapped value.

    Returns:
        List[Dict[str,int]]: A list of dictionaries where each dictionary represents
        a mapped range.

    """
    mapped_ranges = []
    for r in range_list:
        mapped_ranges += get_mapped_ranges(r, map_list)
    return mapped_ranges 


if __name__ == "__main__":
    with open("input", "r") as f:
        seeds = [int(x) for x in f.readline().split(':')[1].strip().split()]
        full_str = f.read()
        maps = [[[int(z) for z in y.split()] for y in x.split(':')[1].strip().split('\n')] for x in full_str.split('\n\n')]
    locations = []
    for s in seeds:
        for m in maps:
            s = get_mapped_value(s, m)
        locations.append(s)
    print(f"part 1: {min(locations)}")

    # part 2
    seed_ranges = []
    for m in maps:
        m.sort(key=lambda x: x[1])
    while seeds:
        seed_range_length, seed_range_start = seeds.pop(), seeds.pop()
        seed_ranges.append([seed_range_start, seed_range_length])
    seed_ranges.reverse()

    ranges = seed_ranges
    
    for m in maps:
        ranges = get_all_mapped_ranges(ranges, m)

    print(f"part 2: {min(x[0] for x in ranges)}")