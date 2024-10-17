def get_mapped_value(x, map_list):
    """
    Calculates a mapped value by adjusting a given number `x` based on a mapping
    list `map_list`. It searches for the first mapping where `x` falls within a
    specified range and applies the corresponding offset to `x`.

    Args:
        x (int): Represented as a value to be mapped according to the rules specified
            in the `map_list`.
        map_list (List[Tuple[int, int, int]]): Populated with 3-element tuples.
            Each tuple contains three integers: the first integer represents the
            mapped value, the second integer represents the start of a range, and
            the third integer represents the length of the range.

    Returns:
        int|str: The mapped value of the input `x` based on the given `map_list`,
        where each element in `map_list` represents a mapping with a range `[m[1],
        m[1] + m[2]]` and a corresponding value `m[0]`.

    """
    for m in map_list:
        if x < m[1] or x > m[1] + m[2]:
            continue
        else:
            return m[0] + x - m[1]
    return x            

def get_mapped_ranges(range, map_list):
    """
    Generates a list of non-overlapping time ranges by mapping a given range onto
    a list of intervals with varying durations, ensuring the mapped ranges do not
    overlap with any intervals and cover the entire given range.

    Args:
        range (List[int]): Represented by a list of two integers. It defines a
            time interval from the first integer to the end at the second integer.
        map_list (List[Tuple[int, int, int]]): Represented as a list of tuples,
            where each tuple contains three integers. These integers appear to
            represent a start point, a duration, and possibly a width or height,
            but the exact meaning is unclear without further context.

    Returns:
        List[List[int]]: A list of sub-ranges that map the given input range to
        the specified range within the provided list of maps.

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
    Iterates over a list of ranges, applies a mapping function to each range using
    `get_mapped_ranges`, and accumulates the results into a single list of mapped
    ranges.

    Args:
        range_list (List[Dict[str, int]]): Expected to be a list of dictionaries
            where each dictionary represents a range with string keys and integer
            values.
        map_list (List[Dict[int, int]]): Presumably a list of dictionaries, where
            each dictionary represents a mapping from the original range to a new
            range.

    Returns:
        List[Dict[str,int]]: A list of dictionaries, where each dictionary represents
        a mapped range with its start and end values.

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