def calculate_steps(start_position, destinations):
    position = start_position
    cursor = 0
    steps = 0
    while position not in destinations:
        position = network[position][instructions[cursor]]
        cursor += 1
        steps += 1
        if cursor == len(instructions):
            cursor = 0
    return steps


def get_loop(start_position):
    position = start_position
    cursor = 0
    steps = 0
    cache = {}
    dest_steps = []
    while (position, cursor) not in cache:
        cache[position, cursor] = steps
        position = network[position][instructions[cursor]]
        cursor += 1
        steps += 1
        if position[2] == "Z":
            dest_steps.append(steps)
        if cursor == len(instructions):
            cursor = 0
    loop_start = cache[(position, cursor)]
    loop_length = steps - loop_start
    dest_steps = [x - loop_start for x in dest_steps]
    return {
        "loop_start": loop_start,
        "loop_length": loop_length,
        "dest_steps": dest_steps,
    }


# def get_part2(cycles):


if __name__ == "__main__":
    instructions_str, network_str = open("input").read().split("\n\n")
    network_dictstr = dict([(x.split(" = ")) for x in network_str.split("\n")])
    network = {k: v.strip("()").split(", ") for k, v in network_dictstr.items()}

    instructions = [0 if x == "L" else 1 for x in instructions_str]

    print(f"part 1: {calculate_steps('AAA', ['ZZZ'])}")

    # part 2
    starter_nodes = [x for x in network.keys() if x[2] == "A"]

    loop_lengths = [get_loop(s)["loop_length"] for s in starter_nodes]
    part2 = len(instructions)
    # some magic happening here.. relies on implicit properties of the input data :-()
    for ll in loop_lengths:
        part2 *= ll // len(instructions)

    print(f"part 2: {part2}")
