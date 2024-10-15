from typing import List

INPUT = "input"


class Part:
    """
    Represents a part with ratings, calculates its total value, and applies a
    workflow based on its current destination.

    Attributes:
        ratings (Dict[str,int]): Initialized with a dictionary comprehension that
            extracts key-value pairs from a string representation of ratings, where
            each key-value pair is separated by an equals sign and each key-value
            pair is separated by a comma.
        value (int): Calculated by summing the values of the ratings stored in the
            `ratings` dictionary.

    """
    def __init__(self, part_str: str):
        """
        Initializes an object of the Part class with a given string representation
        of ratings. It parses the string, extracts key-value pairs, converts values
        to integers, and stores them in the ratings dictionary. The sum of all
        ratings is stored in the value attribute.

        Args:
            part_str (str*): Extracted from a string that contains a collection
                of ratings in key-value format, enclosed within curly braces and
                separated by commas, where each key-value pair is separated by an
                equals sign.

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
        Traverses a directed graph of workflows, starting from an initial node
        "in", until it reaches either node "A" or node "R".

        Args:
            workflows (Dict[str, Workflow]): Used as a mapping of string keys to
                Workflow objects.

        Returns:
            str: Either "A" or "R" after traversing the workflows dictionary.

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
    be initialized from a string, applied to a `Part` object, reversed, and
    represented as a string. The rule checks if a value meets a condition and
    directs the flow accordingly.

    Attributes:
        str (str): Initialized with the `rule_str` parameter in the `__init__` method.
        criterion (str|None): Used to store the first part of a rule string that
            contains a comparison operator. It can be either a string containing
            a rating, comparison operator, and value or None for terminal rules.
        dest (str|int): Initialized with the right-hand side of a rule string,
            which is either another rule string when the rule string contains a
            colon, or the rule string itself when the rule string does not contain
            a colon.
        rating (str): Extracted as the first character of the `criterion` string,
            representing a rating category.
        comp (str|None): Used to store the comparison operator. It can be either
            ">" for greater than, "<" for less than, or None if the rule is a
            terminal rule.
        value (int): Extracted from the criterion string, which is the substring
            of the criterion starting from the third character.

    """
    def __init__(self, rule_str: str):
        """
        Initializes the object with a rule string. If the string contains a colon,
        it extracts the criterion, destination, rating, comparison operator, and
        value. Otherwise, it sets the criterion to None and the destination to the
        rule string.

        Args:
            rule_str (str*): Used to initialize the object with a rule string that
                can be either a criterion specification or a destination.

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
        Evaluates a rule based on a given part and its ratings. If a criterion is
        set, it checks if the rating of the part at the specified index meets the
        comparison condition with the given value.

        Args:
            part (Part*): Passed to the `apply` function to be evaluated against
                the function's criteria.

        Returns:
            bool: True if the part meets the specified criterion, false otherwise,
            depending on the comparison operator and the value of the part's rating.

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
        Reverses the order of parentheses in a given rule string by replacing all
        occurrences of '>' with '(' and '<' with ')'.

        Returns:
            Rule: An instance of the Rule class, created by replacing all occurrences
            of ">" with "(" and "<" with ")" in the string stored in the object's
            `str` attribute.

        """
        reversed_rule = Rule(self.str.replace(">", "(").replace("<", ")"))
        return reversed_rule

    def __repr__(self):
        """
        Returns a string representation of the Rule object, indicating whether it
        is a terminal rule or has a criterion, and its destination.

        Returns:
            str: A string describing the object, specifically a rule, including
            the criterion and destination.

        """
        return (
            f"Rule: {self.criterion if self.criterion else 'Terminal'} => {self.dest}"
        )


class Worflow:
    """
    Represents a workflow with a set of rules. It takes a string defining the
    workflow and its rules, applies these rules to a given `part`, and identifies
    the rules that win based on specific criteria.

    Attributes:
        name (str): Set to the string before the first '{' character in the input
            `workflow_str`, which is stripped of trailing '}' characters.
        rules (List[Rule]): Populated with Rule objects during the initialization
            of the Workflow instance.

    """
    def __init__(self, workflow_str: str):
        """
        Initializes an instance of Worflow by parsing a workflow string. It extracts
        the workflow name and a string of rules, then splits the rules string into
        individual rules and creates a list of Rule objects.

        Args:
            workflow_str (str*): Expected to be a string representing a workflow,
                which is a structured format containing a name and a list of rules
                enclosed in curly brackets.

        """
        self.name, rules_str = workflow_str.strip("}").split("{")
        self.rules = [Rule(rule) for rule in rules_str.split(",")]

    def apply(self, part: Part):
        """
        Iterates over a list of rules, applies each rule to a given Part, and
        returns the destination Part if a rule matches.

        Args:
            part (Part*): Represented by the name `part`, indicating it is a part
                of a larger entity.

        Returns:
            Part|None: Defined as the destination Part object of the first rule
            that successfully applies to the given part.

        """
        for rule in self.rules:
            if rule.apply(part):
                return rule.dest

    def rules_that_win(self, rules=List[Rule]):
        """
        Generates all possible combinations of rules that lead to a winning outcome
        by recursively exploring different paths based on the destination of each
        rule.

        Args:
            rules (List[Rule]): Optional, having a default value of an empty list
                of rules. It represents a collection of rules to be processed.

        Returns:
            List[Dict[str,List[Rule]]]: A list of winning rule combinations. Each
            combination is a list of rules that meet the specified criteria.

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
        Provides a string representation of the object, including its name and
        rules, for debugging and logging purposes.

        Returns:
            str: A formatted string representing the Workflow object, including
            its name and rules.

        """
        return f"""
Workflow {self.name}:
Rules:
{self.rules}"""


class Criteria:
    """
    Enables the calculation of possible combinations of characters in a string
    based on given rules. It counts the possible positions of each character in a
    string, considering criteria like "<" and ">" for minimum and maximum values,
    and "(" and ")" for fixed positions.

    Attributes:
        criteria (List[str]): Initialized with a list of strings extracted from
            the `rules` parameter in the `__init__` method, where each string is
            a criterion.

    """
    def __init__(self, rules=List[Rule]):
        self.criteria = [r.criterion for r in rules]

    def count_possible(self, c: chr):
        """
        Calculates the number of possible values for a given character c in a
        criteria set. It determines the minimum and maximum possible values based
        on the criteria set and returns the count of possible values within that
        range.

        Args:
            c (chr*): Used as a character to determine the range of possible values.

        Returns:
            int: The number of possible values for a given character `c`.

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
        counts of each possible character ("s", "a", "m", "x") together.

        Returns:
            int: The product of the counts of four possible strings, namely "s",
            "a", "m", and "x", calculated by the method `count_possible`.

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
