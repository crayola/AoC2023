INPUT = 'input'

def get_value(step):
    """
    Calculates a hash value based on input string `step` by iteratively applying
    a formula combining ASCII values of characters, multiplication, and modulo
    operation to produce a final value between 0 and 255.

    Args:
        step (str): Expected to be a single character string.

    Returns:
        int: Derived from the input string `step` through a transformation involving
        ASCII values, multiplication, and modulo operation.

    """
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    """
    Represents a lens with a label and focal length. It initializes a lens with a
    given label and focal length, and provides a string representation of the lens
    using its label and focal length.

    Attributes:
        label (str): Assigned a value in the constructor `__init__` method.
        focal (int): Initialized in the `__init__` method with a value converted
            to an integer.

    """
    def __init__(self, label, focal):
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        return f"{self.label} {self.focal}"


class Box:
    """
    Represents a container for lenses, identified by a unique box number. It allows
    adding and updating lenses with specified labels and focal lengths, while
    removing lenses based on their labels.

    Attributes:
        boxnum (int): Initialized in the `__init__` method with a given `boxnum`
            parameter.
        lenses (List[Lens]): Initialized in the `__init__` method with an empty
            list. It stores Lens objects, representing individual lenses within
            the box.

    """
    def __init__(self, boxnum):
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        """
        Updates the Box instance by adding a new lens or replacing an existing
        lens with the same label. It checks if a lens with the given label already
        exists, and if so, replaces it; otherwise, it adds the new lens to the
        list of lenses.

        Args:
            label (str): Used to identify a lens uniquely within a collection of
                lenses.
            focal (float): Representing the focal length of the lens.

        """
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
    




