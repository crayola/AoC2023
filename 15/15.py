INPUT = 'input'

def get_value(step):
    """
    Calculates a hash value for a given string `step` by iterating over each
    character, multiplying the current value by 17, adding the ASCII value of the
    character, and taking the modulus by 256.

    Args:
        step (str): Expected to be a string containing a single character.

    Returns:
        int: A hash value calculated based on the input string `step`, using a
        combination of ASCII values and modular arithmetic.

    """
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    """
    Represents a lens with a label and focal length, allowing instances to be
    created with specific attributes. The `__repr__` method provides a string
    representation of the lens, including its label and focal length.

    Attributes:
        label (str): Assigned a value in the `__init__` method. It stores a string
            that represents the name or description of the lens.
        focal (int): Initialized through the `__init__` method, where it is set
            to the value of the `focal` parameter passed to the method after being
            converted to an integer.

    """
    def __init__(self, label, focal):
        """
        Initializes a new instance of the Lens class by setting two instance
        variables: `label` and `focal`. The `focal` value is converted to an integer.

        Args:
            label (str): Assigned to the instance variable `self.label`, indicating
                that it is used to store a descriptive name or identifier for the
                object.
            focal (int): Converted from its original type to an integer.

        """
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        return f"{self.label} {self.focal}"


class Box:
    """
    Represents a container for lenses with unique labels. It has methods to add
    lenses, replace existing lenses with the same label, and remove lenses by
    label. A box can be represented as a string, including its number and contents.

    Attributes:
        boxnum (int): Initialized with the value of the `boxnum` parameter passed
            to the `__init__` method.
        lenses (List[Dict[str,int]]): Initialized in the `__init__` method as an
            empty list, which stores instances of the `Lens` class.

    """
    def __init__(self, boxnum):
        """
        Initializes a new Box object with a specified box number and an empty list
        of lenses. The box number is stored as an instance variable, and the lenses
        list is initialized to store lenses associated with the box.

        Args:
            boxnum (int): Assigned to the instance variable `self.boxnum`, indicating
                a unique identifier for the object being initialized, likely
                representing a box or container.

        """
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        """
        Deletes a lens from the Box instance's list of lenses, based on a label
        match. The lens to be removed is identified by its label, which must be a
        unique attribute of each lens.

        Args:
            label (str): Used to identify a lens to be removed from the `self.lenses`
                list.

        """
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        """
        Adds a new lens to the existing collection of lenses in the Box instance,
        replacing any existing lens with the same label, or appending the new lens
        if no matching label exists.

        Args:
            label (str): Used to identify a lens uniquely among a collection of lenses.
            focal (float): Representing the focal length of a lens.

        """
        new_lens = Lens(label, focal) 
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label: 
                self.lenses[i] = new_lens
                return None
        self.lenses.append(new_lens)

    def __repr__(self):
        """
        Returns a string representation of the Box object, including its number
        and contents, if any, formatted as a sentence for easy understanding.

        Returns:
            str|None: A string representation of the object, describing the box
            number and its contents, or an empty string if the box is empty.

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
    




