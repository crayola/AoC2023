INPUT = 'input'

def get_value(step):
    """
    Calculates a value based on the input string `step`. It iterates over each
    character in the string, updating the `current_value` using a formula that
    involves the character's ASCII value, a multiplier, and a modulo operation,
    resulting in a value between 0 and 255.

    Args:
        step (str): Expected to be a single character string.

    Returns:
        int: Calculated based on the given string `step` and the ASCII values of
        its characters.

    """
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    """
    Represents a lens with a label and focal length. It initializes a lens with a
    specified label and focal length, ensuring the focal length is an integer. The
    `__repr__` method provides a string representation of the lens.

    Attributes:
        label (str): Used to store a descriptive label for a lens, such as its
            name or designation.
        focal (int): Represented by the `int(focal)` conversion in the `__init__`
            method, indicating that the `focal` value is expected to be a string
            that can be converted to an integer.

    """
    def __init__(self, label, focal):
        """
        Initializes a new Lens object by setting its label and focal length. The
        focal length is converted to an integer.

        Args:
            label (str): Assigned to an instance variable. It is used to represent
                a label or identifier for an object, likely used for identification
                or display purposes.
            focal (int): Converted to an integer.

        """
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        """
        Returns a string representation of the Lens instance, combining the label
        and focal attributes with a space in between.

        Returns:
            str: A string representation of the object, combining its label and
            focal attributes.

        """
        return f"{self.label} {self.focal}"


class Box:
    """
    Manages a collection of lenses with unique labels. It allows adding new lenses
    or updating existing ones with the same label, and removing lenses by their
    label. The class also provides a string representation of the box and its contents.

    Attributes:
        boxnum (int): Initialized in the `__init__` method with a provided integer
            value. It uniquely identifies a box instance and is used in string representation.
        lenses (List[Lens]): Initialized in the `__init__` method as an empty list,
            which stores instances of the `Lens` class.

    """
    def __init__(self, boxnum):
        """
        Initializes a new Box object by setting its box number and an empty list
        for storing lenses.

        Args:
            boxnum (int): Assigned to the instance variable `self.boxnum` upon initialization.

        """
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        """
        Removes a lens from the lenses list based on the provided label. It iterates
        over the lenses, checks if the label matches, and if so, removes the
        corresponding lens from the list.

        Args:
            label (str): Used to identify the lens to be removed from the `self.lenses`
                list, based on the label attribute of the lens object.

        """
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        """
        Updates or adds a lens to the list of lenses if a lens with the same label
        already exists, replacing it with a new lens; otherwise, it appends the
        new lens to the list.

        Args:
            label (str): Used to identify a lens uniquely within the collection
                of lenses.
            focal (float): Required to create a new `Lens` object. It represents
                the focal length of a lens.

        """
        new_lens = Lens(label, focal) 
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label: 
                self.lenses[i] = new_lens
                return None
        self.lenses.append(new_lens)

    def __repr__(self):
        """
        Returns a string representation of the Box object, displaying its box
        number and the lenses it contains, if any.

        Returns:
            str: A string representation of the object, describing the box containing
            lenses or not.

        """
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
    




