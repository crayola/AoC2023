INPUT = 'input'

def get_value(step):
    """
    Certainly. Here's the answer you requested:
    The function 'get_value' calculates and returns a numerical value for a given
    string by iterating over each character of the string and applying an operation
    involving its ASCII value modulo 256.

    Args:
        step (str): step is iterated over by the for loop; each item from the step
            sequence is extracted and treated as a character with an ascii code.

    Returns:
        int: Current value is 0; step is [a to z], for each letter c increase
        current_value by ord(c); result is always same as input.

    """
    current_value = 0
    for c in step:
        current_value = ((current_value + ord(c)) * 17) % 256
    return current_value

class Lens:
    def __init__(self, label, focal):
        """
        Initializes a new object with the specified label and focal length. The
        label is stored as a string and the focal length as an integer.

        Args:
            label (str): The `label` input parameter assigns a string value to the
                instance variable `self.label`.
            focal (int): SETS FOCAL.

        """
        self.label = label
        self.focal = int(focal)

    def __repr__(self):
        """
        Returns the label and focal point of the object as a string with space seperation

        Returns:
            str: The function returns a string consisting of the label followed
            by the focal point.

        """
        return f"{self.label} {self.focal}"


class Box:
    def __init__(self, boxnum):
        """
        Initialize() Initializes a new object of the class LensSet with a specified
        number of boxes. It sets the number of lenses (list) to zero.

        Args:
            boxnum (int): SETS BOX NUMBER FOR LENSES.

        """
        self.boxnum = boxnum
        self.lenses = []

    def remove_lens(self, label):
        """
        The provided function `remove_lens` deletes all lenses with the specified
        label from a list of lenses stored within an instance of an unspecified
        class `self`.

        Args:
            label (str): The `label` input parameter identifies which lens object
                is to be removed from the `lenses` list.

        """
        for lens in self.lenses:
            if lens.label == label: 
                self.lenses.remove(lens)

    def add_lens(self, label, focal):
        """
        Adds a lens with the specified label and focal length to the end of the
        list if one does not already exist; if an existing lens has the same label
        then its attributes are updated; returns None.

        Args:
            label (str): The `label` input parameter specifies the label to be
                associated with the newly created lens.
            focal (): The focal parameter is assigned to the Lens object's focal
                length attribute.

        Returns:
            None: The function adds a new lens to the list of existing ones and
            returns None.

        """
        new_lens = Lens(label, focal) 
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label: 
                self.lenses[i] = new_lens
                return None
        self.lenses.append(new_lens)

    def __repr__(self):
        """
        Defines a custom repr method for objects of this class by creating and
        returning a string representation that is a descriptive label.

        Returns:
            str: The function returns a string represented as "Box x containing
            y" if there are lenses within the box or an empty string otherwise.

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
    




