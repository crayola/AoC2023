from typing import List

INPUT = "input"


class Part:
    """
    Represents a part with ratings, calculates its total value, and applies it to
    workflows to determine its destination, which can be either "A" or "R".

    Attributes:
        ratings (Dict[str,int]): Initialized with a dictionary containing key-value
            pairs representing ratings of different parts.
        value (int): Calculated as the sum of all ratings in the `ratings` dictionary.

    """
    def __init__(self, part_str: str):
        """
        Initializes the object with a string representation of ratings, parses the
        string into a dictionary of ratings, and calculates the total value from
        these ratings.

        Args:
            part_str (str): Expected to be a string representing a dictionary of
                ratings in the format "{key1=value1, key2=value2, ...}".

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
        Traverses a workflow network, starting from the 'in' node, until it reaches
        a node that is either 'A' or 'R', and returns the destination node.

        Args:
            workflows (Dict[str, Workflow]): Used to store and manage a collection
                of workflows, where each key is a string identifier and each value
                is a Workflow object.

        Returns:
            str: Either "A" or "R"

        """
        dest = "in"
        while dest not in ["A", "R"]:
            dest = workflows[dest].apply(self)
        return dest

    def __repr__(self):
        """
        Returns a string representation of the object, which includes the class
        name and the value of the ratings attribute.

        Returns:
            str: Representing the object's state in a human-readable format.

        """
        return f"Part: {self.ratings}"


class Rule:
    """
    Defines a rule with a criterion and a destination. It allows rules to be applied
    to a `Part` object, evaluating the criterion and returning a boolean result.
    Rules can also be reversed and represented as strings.

    Attributes:
        str (str): Assigned the initial value of the `rule_str` parameter in the
            `__init__` method.
        criterion (str|None): Used to store a condition based on which a rule is
            applied. It is composed of a rating, a comparison operator, and a
            value, and is used to evaluate a `Part` object.
        dest (str): Initialized with the part after the colon in the rule string
            or with the entire rule string if no colon is present.
        rating (str|int): Extracted from the `criterion` string. It represents the
            rating part of the rule, which can be a single character for terminal
            rules or a combination of a character and a value for non-terminal rules.
        comp (str|None): Used to represent comparison operators. It can be either
            ">" for greater than or "<" for less than, or None for a terminal rule.
        value (int): Extracted from the `criterion` string where it is assumed to
            be the last part of the string, starting from the third character.

    """
    def __init__(self, rule_str: str):
        """
        Initializes an instance of the Rule class. It takes a string rule_str as
        input, parsing it into its constituent parts: criterion, destination,
        rating, comparison operator, and value.

        Args:
            rule_str (str): Defined as a string that represents a rule. It is
                expected to either contain a colon (:) or be a single value.

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
        Evaluates a part against a rule, returning True or False based on the
        comparison of a rating value against a specified value, or always returning
        True if no criterion is set.

        Args:
            part (Part): Passed to the function, where it is used to access the
                ratings of the part, specifically the rating at the index defined
                by `self.rating`.

        Returns:
            bool: True if the part meets the specified condition, False otherwise.

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
        """
        Creates a new Rule instance with the input string's operators reversed,
        replacing '>' with '(' and '<' with ')'.

        Returns:
            Rule: A new instance of the Rule class, created by replacing all
            occurrences of ">" with "(" and "<" with ")" in the string attribute
            of the current instance.

        """
        reversed_rule = Rule(self.str.replace(">", "(").replace("<", ")"))
        return reversed_rule

    def __repr__(self):
        """
        Returns a string representation of the rule, indicating whether it is a
        terminal rule (no criterion) or a rule with a criterion, and its destination.

        Returns:
            str: A string representation of the object, describing a rule as 'Rule:
            Terminal => dest' or 'Rule: criterion => dest' depending on whether
            self.criterion is None or not.

        """
        return (
            f"Rule: {self.criterion if self.criterion else 'Terminal'} => {self.dest}"
        )


class Worflow:
    """
    Implements a workflow system with the following functionality:
    it initializes a workflow from a string representation, applies rules to a
    given part, identifies winning rules based on their criteria and destinations,
    and provides a string representation of the workflow.

    Attributes:
        name (str): Derived from the `workflow_str` parameter of the `__init__`
            method, which is the first part of the `workflow_str` split by the `{`
            character.
        rules (List[Rule]): Initialized in the `__init__` method as a list of
            `Rule` objects, created by splitting a string of rules into individual
            rules and instantiating each one with the `Rule` class.

    """
    def __init__(self, workflow_str: str):
        """
        Initializes a Worflow instance by parsing a workflow string into its
        constituent parts: name and rules. It extracts the name and rules string,
        then splits the rules string into individual rules, instantiating each as
        a Rule object.

        Args:
            workflow_str (str): Expected to contain a string representation of a
                workflow, likely in the format of "{rule1},{rule2},..." enclosed
                in curly braces.

        """
        self.name, rules_str = workflow_str.strip("}").split("{")
        self.rules = [Rule(rule) for rule in rules_str.split(",")]

    def apply(self, part: Part):
        """
        Iterates over a list of rules, applies each rule to a given `part`, and
        returns the destination of the first rule that successfully applies.

        Args:
            part (Part): Used to apply a rule to a specific part.

        Returns:
            Part|None: Either the destination part if a rule applies, or None if
            no rule applies.

        """
        for rule in self.rules:
            if rule.apply(part):
                return rule.dest

    def rules_that_win(self, rules=List[Rule]):
        """
        Generates all possible combinations of rules that lead to a win state from
        a given set of rules. It recursively explores different branches of the
        workflow based on the destination of each rule.

        Args:
            rules (List[Rule]): Defaulted to an empty list, allowing the function
                to be called without specifying any rules.

        Returns:
            List[List[Rule]]: A list of lists of rules, where each sublist represents
            a set of winning rules that satisfy certain conditions and lead to a
            specific destination.

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
        Provides a string representation of the Worflow object, including its name
        and rules, suitable for debugging or logging purposes.

        Returns:
            str: A formatted string representing the workflow object, including
            its name and rules.

        """
        return f"""
Workflow {self.name}:
Rules:
{self.rules}"""


class Criteria:
    """
    Calculates the number of possible values for a set of criteria based on given
    rules. It uses a set of rules to determine valid ranges for each criterion and
    returns the total number of possible combinations.

    Attributes:
        criteria (List[str]): Initialized with a list containing the criterion of
            each rule in the input list of rules.

    """
    def __init__(self, rules=List[Rule]):
        """
        Initializes the object with a list of rules, extracting the criterion from
        each rule.

        Args:
            rules (List[Rule]): Optional, with a default value of an empty list.
                It is expected to contain one or more Rule objects.

        """
        self.criteria = [r.criterion for r in rules]

    def count_possible(self, c: chr):
        """
        Calculates the number of possible values for a given character 'c' by
        determining its minimum and maximum values from the criteria list. It
        returns the count of possible values, ensuring it is not negative.

        Args:
            c (chr): Used to represent a character. It appears to be used to filter
                a list of criteria based on specific patterns, such as '>' and
                '<', to determine a range of possible values.

        Returns:
            int: The number of possible values for the given character c within
            the specified criteria.

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
        Calculates the total number of possible combinations by multiplying the
        counts of each individual character ("s", "a", "m", and "x") from the
        `count_possible` method.

        Returns:
            int: The product of the counts of possible words that can be formed
            using the letters 's', 'a', 'm', and 'x'.

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
