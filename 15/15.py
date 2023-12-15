INPUT = 'input'

def get_value(step):
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    def __init__(self, label, focal):
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        return f"{self.label} {self.focal}"


class Box:
    def __init__(self, boxnum):
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        new_lens = Lens(label, focal) 
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label: 
                self.lenses[i] = new_lens
                return None
        self.lenses.append(new_lens)

    def __repr__(self):
        boxstr = f"Box {self.boxnum} containing {self.lenses}" if self.lenses else ""
        return boxstr


if __name__ == '__main__':
    steps = open(INPUT).read().split(',')
    
    #part 1
    part1 = sum([get_value(step) for step in steps])
    print(f"part 1: {part1}")

    #part 2
    boxes = [Box(label) for label in range(256)]

    for step in steps:
        if '-' in step:
            label = step[:-1]
            boxes[get_value(label)].remove_lens(label)
        if '=' in step:
            label, focal = step.split('=')
            boxes[get_value(label)].add_lens(label, focal)

    part2 = sum([(box.boxnum + 1) * lens.focal * (i+1) for box in boxes for i, lens in enumerate(box.lenses)])
    print(f"part 2: {part2}")
    




