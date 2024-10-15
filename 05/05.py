def get_mapped_value(x, map_list):
    """
    Maps a given value `x` within a specified range to a corresponding value based
    on a list of mappings. Each mapping is defined by a tuple containing the lower
    bound, upper bound, and the offset value.

    Args:
        x (int): Represented as a position value, which is a number that needs to
            be mapped according to a given set of rules.
        map_list (List[Tuple[int, int, int]]): Used to represent a list of mappings,
            where each mapping is a tuple of three integers.

    Returns:
        int|str: The mapped value for a given input `x` if it falls within a
        specified range defined by the mapping list `map_list`, otherwise it returns
        the original input `x`.

    """
    for m in map_list:
        if x < m[1] or x > m[1] + m[2]:
            continue
        else:
            return m[0] + x - m[1]
    return x            

def get_mapped_ranges(range, map_list):
    """
    Takes a range and a list of maps as input, and returns a list of non-overlapping
    sub-ranges within the input range that are covered by the maps.

    Args:
        range (List[int]): Expected to contain two elements: the start and the
            length of a time interval or a range.
        map_list (List[Dict[str, int]]): Typically expected to contain dictionaries
            with at least three integer keys, representing a map with a position
            (`1`), a width (`2`), and a height (`3`).

    Returns:
        List[List[int]]: A list of intervals representing the ranges of a given
        input range that overlap with the intervals in the input list of maps.

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
    Iterates over a list of input ranges, applies the `get_mapped_ranges` function
    to each range, and accumulates the results into a single list of mapped ranges.

    Args:
        range_list (List[RangeType]): Expected to be a list of range objects.
        map_list (List[Dict[int, int]]): Used to map values in the `range_list`
            to new values. The dictionaries in the `map_list` represent these
            mappings, where each key is a value in a range and each value is its
            corresponding mapped value.

    Returns:
        List[Dict[str,int]]: A list of dictionaries, where each dictionary contains
        a range and its mapped values.

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