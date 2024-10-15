def get_mapped_value(x, map_list):
    """
    Returns a mapped value based on a given input `x` and a list of mappings
    `map_list`. Each mapping in `map_list` is a tuple of three values: a base value
    and a range with a start and end value.

    Args:
        x (int): Interpreted as a value to be mapped. It is compared to a range
            of values in the `map_list` to determine the mapped result.
        map_list (List[Tuple[int, int, int]]): Used to store a list of mappings,
            where each mapping is a tuple of three integers representing a range
            and a shift. The range is defined by a start and end value, and the
            shift is the value to be added to any input within the range.

    Returns:
        int|str: The mapped value of input `x` based on the provided `map_list`
        if `x` falls within a specified range, otherwise it returns `x` unchanged.

    """
    for m in map_list:
        if x < m[1] or x > m[1] + m[2]:
            continue
        else:
            return m[0] + x - m[1]
    return x            

def get_mapped_ranges(range, map_list):
    """
    Calculates the overlapping ranges between a given range and a list of mapped
    ranges, returning a list of new ranges that result from the overlap.

    Args:
        range (List[int]): Represented by a list of two integers, where the first
            integer is the start of the range and the second integer is the length
            of the range.
        map_list (List[Tuple[int, int, int]]): Composed of non-overlapping intervals,
            where each interval is a tuple of three integers representing the
            start, end, and width of the interval.

    Returns:
        List[List[int]]: A list of non-overlapping integer ranges that cover the
        entire input range, taking into account the constraints imposed by the map_list.

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
    Takes a list of ranges and a list of mappings, recursively applies the mappings
    to each range, and returns a list of all resulting mapped ranges.

    Args:
        range_list (List[Range]): Expected to contain one or more ranges, where a
            range is likely a data structure representing a sequence of values.
        map_list (List[Dict[int, int]]): Used to store mappings of original range
            values to their corresponding mapped values.

    Returns:
        List[Dict[int,int]]: A list of dictionaries, where each dictionary contains
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