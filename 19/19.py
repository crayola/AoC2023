from typing import List

INPUT = "input"


class Part:
    """
    Represents a part with ratings, where ratings are key-value pairs. It calculates
    the total value of the ratings and has methods to apply the part to workflows,
    navigating through the workflow graph based on the destination specified by
    the part's ratings.

    Attributes:
        ratings (Dict[str,int]): Populated by parsing a string representation of
            ratings, where each rating is a key-value pair separated by an equals
            sign and enclosed in a dictionary, and then converted to a dictionary
            of integers.
        value (int): Calculated by summing the values of all ratings associated
            with the part.

    """
    def __init__(self, part_str: str):
        """
        Initializes the object with a string representation of ratings. It parses
        the input string into a dictionary where keys are rating names and values
        are corresponding integer values. The sum of all ratings is stored as the
        object's value.

        Args:
            part_str (str*): Expected to be a string containing a list of ratings
                in the format "key=value,key=value,...".

        """
        self.ratings = {
            k: int(v)
            for k, v in dict(
                [x.split("=") for x in part_str.strip("{}").split(",")]
            ).items()
        }
        self.value = sum(self.ratings.values())

    def apply(self, workflows):
        """
        Navigates a workflow graph by recursively applying the `apply` method to
        the current destination node until it reaches a node labeled "A" or "R",
        then returns the final destination node.

        Args:
            workflows (Dict[str, Workflow]): Accessed by its keys.

        Returns:
            str: The destination, either 'A' or 'R'.

        """
        dest = "in"
        while dest not in ["A", "R"]:
            dest = workflows[dest].apply(self)
        return dest

    def __repr__(self):
        return f"Part: {self.ratings}"


class Rule:
    """
    Represents a decision-making rule with a criterion and a destination. It can
    parse rules from strings, apply them to `Part` objects, and reverse the rule's
    comparison operator.

    Attributes:
        str (str): Assigned the value of the `rule_str` parameter passed to the
            `__init__` method. It is used to store the original string representation
            of the rule.
        criterion (str|None): Used to store the condition of the rule. It contains
            information about the rating, comparison operator, and value.
        dest (str|int): Used to store the destination of a rule, which is either
            the destination string when a criterion is not specified or the
            identifier of a part when a criterion is specified.
        rating (str): Extracted from the `criterion` string which represents a
            character rating in the format of a single character followed by a
            comparison operator and a value.
        comp (str|None): Used to represent the comparison operator in a rule. It
            can be either ">" for greater than or "<" for less than, or None for
            a terminal rule.
        value (int): Extracted from the criterion string by taking all characters
            from the third index onwards of the `criterion` string.

    """
    def __init__(self, rule_str: str):
        """
        Initialize the object's attributes based on the input rule string. If the
        string contains a colon, it is assumed to be in the format "Rc:dest" where
        Rc is a rating, a comparison operator, and a value, otherwise it is a destination.

        Args:
            rule_str (str*): Required for the function to execute properly.

        """
        if ":" in rule_str:
            self.str = rule_str
            self.criterion, self.dest = rule_str.split(":")
            self.rating, self.comp, self.value = (
                self.criterion[0],
                self.criterion[1],
                int(self.criterion[2:]),
            )
        else:
            self.criterion = None
            self.dest = rule_str

    def apply(self, part: Part):
        """
        Evaluates a rule based on the provided part and applies it to the ratings
        of the part. It checks if the rating of the specified attribute meets the
        defined condition (greater than or less than a specified value) if a
        criterion is provided.

        Args:
            part (Part*): Passed to the function, presumably to be evaluated against
                a set of criteria.

        Returns:
            bool: `True` if the part meets the specified criterion, and `False` otherwise.

        """
        if self.criterion:
            value = part.ratings[self.rating]
            if self.comp == ">":
                return value > self.value
            if self.comp == "<":
                return value < self.value
        else:
            return True

    def reverse(self):
        reversed_rule = Rule(self.str.replace(">", "(").replace("<", ")"))
        return reversed_rule

    def __repr__(self):
        return (
            f"Rule: {self.criterion if self.criterion else 'Terminal'} => {self.dest}"
        )


class Worflow:
    """
    Represents a workflow with a set of rules. It initializes a workflow from a
    string, applies rules to a part, and identifies winning rules by recursively
    aggregating rules based on their criteria and destinations.

    Attributes:
        name (str): Extracted from the input string `workflow_str` by splitting
            it at the first occurrence of '{' after removing trailing '}'.
        rules (List[Rule]): Populated with objects of type Rule, which are created
            from a string of rules in the workflow definition.

    """
    def __init__(self, workflow_str: str):
        self.name, rules_str = workflow_str.strip("}").split("{")
        self.rules = [Rule(rule) for rule in rules_str.split(",")]

    def apply(self, part: Part):
        for rule in self.rules:
            if rule.apply(part):
                return rule.dest

    def rules_that_win(self, rules=List[Rule]):
        """
        Identifies winning rules by recursively applying given rules and their
        reversals to a workflow, aggregating results based on rule destinations
        and criteria.

        Args:
            rules (List[Rule]): Optional, with a default value of an empty list.
                It represents a collection of rules to be evaluated.

        Returns:
            List[List[Rule]]: A list of all possible combinations of winning rules
            that lead to a successful outcome.

        """
        winning_rules = []
        agg_rules = rules
        for r in self.rules:
            if r.criterion:
                if r.dest == "A":
                    winning_rules.append(agg_rules + [r])
                    agg_rules.append(r.reverse())
                elif r.dest == "R":
                    agg_rules.append(r.reverse())
                else:
                    winning_rules.extend(
                        workflows[r.dest].rules_that_win(agg_rules + [r])
                    )
                    agg_rules.append(r.reverse())
            else:
                if r.dest == "A":
                    winning_rules.append(agg_rules)
                elif r.dest == "R":
                    pass
                else:
                    winning_rules.extend(workflows[r.dest].rules_that_win(agg_rules))
        return winning_rules

    def __repr__(self):
        """
        Returns a string representation of the Workflow object, including its name
        and rules, formatted as a multi-line string.

        Returns:
            str: A formatted string representation of the object, including its
            name and rules, suitable for debugging or logging purposes.

        """
        return f"""
Workflow {self.name}:
Rules:
{self.rules}"""


class Criteria:
    """
    Calculates the number of possible values for a given set of criteria based on
    a specific rule format. It parses rules to determine valid character ranges
    and returns the total number of possible combinations for a set of criteria.

    Attributes:
        criteria (List[str]): Populated with a list of strings representing the
            criteria extracted from the `rules` parameter in the `__init__` method.

    """
    def __init__(self, rules=List[Rule]):
        self.criteria = [r.criterion for r in rules]

    def count_possible(self, c: chr):
        """
        Calculates the number of possible values for a given character within a
        set of criteria, represented as strings with a character and a symbol (<,
        >, (, or )) indicating the range.

        Args:
            c (chr*): Used as the character prefix to identify criteria in `self.criteria`.

        Returns:
            int: The number of possible values for a given character `c` based on
            its criteria.

        """
        c_min = max(
            [int(x[2:]) + 1 for x in self.criteria if x[:2] == c + ">"]
            + [int(x[2:]) for x in self.criteria if x[:2] == c + ")"]
            + [1]
        )
        c_max = min(
            [int(x[2:]) - 1 for x in self.criteria if x[:2] == c + "<"]
            + [int(x[2:]) for x in self.criteria if x[:2] == c + "("]
            + [4000]
        )
        return max(0, c_max - c_min + 1)

    def count_all_possible(self):
        """
        Calculates the total number of possible combinations of the letters "s",
        "a", "m", and "x".

        Returns:
            int: The product of four counts, each obtained by calling `count_possible`
            with a different character: "s", "a", "m", and "x".

        """
        return (
            self.count_possible("s")
            * self.count_possible("a")
            * self.count_possible("m")
            * self.count_possible("x")
        )


if __name__ == "__main__":
    workflows_str, parts_str = open(INPUT).read().split("\n\n")
    parts = [Part(p) for p in parts_str.split("\n")]

    workflows_list = [Worflow(w) for w in workflows_str.split("\n")]
    workflows = {w.name: w for w in workflows_list}

    part1 = sum([p.value for p in parts if p.apply(workflows) == "A"])
    print(f"Part 1: {part1}")

    part2 = sum(
        [Criteria(w).count_all_possible() for w in workflows["in"].rules_that_win([])]
    )
    print(f"Part 2: {part2}")
