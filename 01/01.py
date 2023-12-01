import re

digits_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

def getdigits_part2(line):
    """read digits from each line, including strings"""
    digits = []
    running_str = ""
    for c in line:
        running_str += c
        if c.isdigit():
            digits += [int(c)]            
        else:
            for digit_string in digits_dict.keys():
                digit_string_matched = re.match('.*(' + digit_string + ')$', running_str)
                if digit_string_matched:
                    digits += [digits_dict[digit_string_matched.group(1)]]
    return digits

def get_number_part1(line):
    """read first and last digit from each line"""
    digits = [int(c) for c in line if c.isdigit()]
    if len(digits) >= 1:
        return 10 * digits[0] + digits[-1]
    else:
        return 0

def get_number_part2(line):
    """read first and last digit from each line"""
    digits = getdigits_part2(line)
    if len(digits) >= 1:
        return 10 * digits[0] + digits[-1]
    else:
        return 0


if __name__ == '__main__':

    with open("./input", "r") as f:
        line = f.readline()
        i = 0
        sum_lines_1 = 0
        sum_lines_2 = 0

        while line:
            sum_lines_1 += get_number_part1(line)
            sum_lines_2 += get_number_part2(line)
            line = f.readline()

        print(f"Part 1: {sum_lines_1}; part 2: {sum_lines_2}")