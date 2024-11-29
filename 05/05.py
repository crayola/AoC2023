def get_mapped_value(x, map_list):
    """
    maps a given value `x` to its position in a list of pairs, and returns the
    corresponding value after subtraction of the midpoint of the range.

    Args:
        x (float): numerical value that is being searched for in the list of maps
            provided as input to the function, and the function uses it to determine
            whether it is present in the list and if so, returns its mapped value.
        map_list (list): 2-element lists of boundaries for which the value should
            be mapped.

    Returns:
        int: the value of `x` after being mapped through the list of tuples in `map_list`.

    """
    for m in map_list:
        if x < m[1] or x > m[1] + m[2]:
            continue
        else:
            return m[0] + x - m[1]
    return x            

def get_mapped_ranges(range, map_list):
    """
    maps a range of numbers to a list of non-overlapping intervals, respecting the
    specified range and excluding any interval that overlaps with the previous one.

    Args:
        range (list): 2-element bounding range for which the maps in the `map_list`
            should be checked for overlap.
        map_list (list): list of mapped ranges, which is filtered based on the
            given range's start and end points to produce a new list of only
            overlapping mapped ranges.

    Returns:
        int: a list of pairs of numbers representing the mapped ranges.

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
    takes a list of ranges and a list of maps and returns all the mapped ranges.

    Args:
        range_list (list): list of ranges to be mapped.
        map_list (list): 2D array of mapped ranges, which is used to generate the
            final list of mapped ranges for each range in the `range_list`.

    Returns:
        list: a list of all mapped ranges found in the input `range_list`.

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