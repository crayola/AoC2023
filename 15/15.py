INPUT = 'input'

def get_value(step):
    """
    Calculates a hash value for a given string `step`. It multiplies the sum of
    ASCII values of its characters by 17, modulo 256, to produce a fixed-size integer.

    Args:
        step (str): Used as an input string.

    Returns:
        int: A hash value calculated based on the input string `step`.

    """
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    """
    Represents a lens with a label and a focal length. It initializes the lens
    with a given label and focal length, and returns a string representation of
    the lens in the format "label focal".

    Attributes:
        label (str): Initialized in the `__init__` method with a given label, which
            appears to be a string representing the name or description of the lens.
        focal (int): Initialized with the value passed to the `focal` parameter
            of the `__init__` method.

    """
    def __init__(self, label, focal):
        """
        Initializes the Lens object with a label and a focal length, which is
        converted to an integer.

        Args:
            label (str): Assigned to an instance variable of the same name. It
                represents a label, likely a string identifier, for the object
                being created.
            focal (int): Converted to an integer using the `int()` function.

        """
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        """
        Provides a string representation of the object, combining the label and
        focal attributes of the Lens instance.

        Returns:
            str: A string representation of the object, specifically a string that
            includes the label and focal attributes of the object.

        """
        return f"{self.label} {self.focal}"


class Box:
    """
    Manages a collection of lenses with unique labels. It allows adding lenses
    with specific labels and focal lengths, updating existing lenses with the same
    label, and removing lenses by their labels.

    Attributes:
        boxnum (int): Initialized in the `__init__` method with the `boxnum`
            parameter passed to the `Box` class constructor.
        lenses (List[Lens]): Initialized in the `__init__` method as an empty list.
            It stores Lens objects, which represent individual lenses. The `lenses`
            attribute is used to keep track of the lenses contained in the box.

    """
    def __init__(self, boxnum):
        """
        Initializes a new Box instance with a specified box number and an empty
        list to store lenses. The box number is stored as an instance variable,
        while the lenses list is initialized to accommodate future lens additions.

        Args:
            boxnum (int): Assigned to the instance variable `self.boxnum`. It
                appears to be a unique identifier for the object.

        """
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        """
        Removes a lens from the Box's list of lenses based on the provided label.

        Args:
            label (str): Used to identify the lens to be removed from the `self.lenses`
                list.

        """
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        """
        Updates or adds a lens to the Box's collection. It checks if a lens with
        the given label already exists, and if so, it replaces it with a new lens.
        If not, it adds the new lens to the collection.

        Args:
            label (str): Used to identify a lens uniquely. It is checked for
                existence in the list of lenses before adding a new lens with the
                same label.
            focal (float): Used to initialize the focal length of a new `Lens`
                object, which is created when a lens with a matching label is not
                found in the existing list of lenses.

        """
        new_lens = Lens(label, focal) 
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label: 
                self.lenses[i] = new_lens
                return None
        self.lenses.append(new_lens)

    def __repr__(self):
        """
        Provides a string representation of the Box object, including its number
        and contents, which are the lenses if any exist.

        Returns:
            str: A string representation of the object, describing its contents.

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
    




