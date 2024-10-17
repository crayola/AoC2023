from typing import List

INPUT = "input"


class Part:
    """
    Represents a part with ratings and a value, calculated as the sum of ratings.
    It has methods to apply the part to workflows and get the destination, and a
    string representation of the part's ratings.

    Attributes:
        ratings (Dict[str,int]): Populated with key-value pairs representing ratings
            from a string of comma-separated key-value pairs enclosed in curly brackets.
        value (int): Calculated by summing the values of all ratings in the `ratings`
            dictionary.

    """
    def __init__(self, part_str: str):
        """
        Extracts ratings from a given string and calculates a total value. The
        string is expected to be a comma-separated list of key-value pairs enclosed
        in curly brackets, where each pair represents a rating with its value.

        Args:
            part_str (str): Expected to be a string containing key-value pairs of
                ratings, enclosed in curly brackets and separated by commas.

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
        Traverses a workflow graph by recursively applying the `apply` method to
        each destination node until a node with a destination of either 'A' or 'R'
        is reached, returning the last node's destination.

        Args:
            workflows (Dict[str, Workflow]): Expected to be a dictionary mapping
                destination nodes to their respective workflow objects.

        Returns:
            str: Either the string "A" or "R", depending on the result of the
            recursive call to `apply` on the workflow associated with the destination.

        """
        dest = "in"
        while dest not in ["A", "R"]:
            dest = workflows[dest].apply(self)
        return dest

    def __repr__(self):
        """
        Returns a string representation of the Part object, including its ratings,
        which is used to provide a human-readable description of the object when
        it is printed or converted to a string.

        Returns:
            str: A string representation of the object, specifically in the format
            "Part: ratings", where ratings are the values stored in the object's
            ratings attribute.

        """
        return f"Part: {self.ratings}"


class Rule:
    """
    Represents a conditional rule with a criterion and a destination. It can be
    initialized from a string, applied to a `Part` object, reversed, and represented
    as a string.

    Attributes:
        str (str): Initialized with the `rule_str` parameter passed to the `__init__`
            method. It stores the original string representation of the rule.
        criterion (str|None): Constructed by splitting a string containing a rule
            into three parts: a rating, a comparison operator, and a value.
        dest (str|None): Initialized from the `rule_str` parameter in the `__init__`
            method when the rule string contains a colon, in which case it is set
            to the right-hand side of the colon. It is also set to the entire
            `rule_str` when the string does not contain a colon.
        rating (str): Extracted from the `criterion` string, specifically the first
            character.
        comp (str|None): Set to the comparison operator of the rule's criterion,
            either ">" (greater than) or "<" (less than), indicating the relationship
            between the rating and the value specified in the rule.
        value (int): Extracted from the `criterion` string, specifically from the
            third character onwards, representing a numerical value to be compared
            with the part's rating.

    """
    def __init__(self, rule_str: str):
        """
        Initializes the Rule object based on the provided rule string. If the
        string contains a colon, it extracts specific criteria (rating, comp,
        value) and a destination; otherwise, it sets the destination to the entire
        string and leaves other attributes undefined.

        Args:
            rule_str (str): Used to initialize the object with a string that may
                represent a rule.

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
        Evaluates a rule based on a part's rating. If a criterion exists, it checks
        if the rating value meets the specified comparison (greater than or less
        than) with the given value. If no criterion exists, it returns True.

        Args:
            part (Part): Referenced as an instance of the Part class, which
                presumably has a `ratings` attribute, a dictionary or similar data
                structure containing ratings for different criteria.

        Returns:
            bool: True if the part meets the specified criteria, False otherwise,
            indicating whether the part should be included in a collection based
            on its ratings.

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
        Reverses the logical operators in a given rule by replacing '>' with '('
        and '<' with ')'.

        Returns:
            Rule: Created by replacing all occurrences of '>' with '(' and '<'
            with ')' in the original string.

        """
        reversed_rule = Rule(self.str.replace(">", "(").replace("<", ")"))
        return reversed_rule

    def __repr__(self):
        """
        Returns a string representation of the rule, which includes the criterion
        and the destination, or the string 'Terminal' if the criterion is None.

        Returns:
            str: A string representation of the object, specifically a rule in the
            format "Rule: <criterion> => <dest>", where <criterion> is the rule's
            criterion and <dest> is its destination.

        """
        return (
            f"Rule: {self.criterion if self.criterion else 'Terminal'} => {self.dest}"
        )


class Worflow:
    """
    Represents a workflow with a set of rules. It initializes a workflow from a
    string, applies the rules to a part, and determines winning rules based on
    their criteria and destinations.

    Attributes:
        name (str): Derived from the input string `workflow_str` by splitting it
            at the first occurrence of '{' and taking the part before it.
        rules (List[Rule]): Initialized with a list comprehension in the `__init__`
            method, where each rule is an instance of the `Rule` class, created
            from a string split by commas.

    """
    def __init__(self, workflow_str: str):
        """
        Initializes a Worflow object from a given string representation of a
        workflow. The string is expected to be in the format '{name}{rules}', where
        'name' is the workflow name and 'rules' are comma-separated rule strings.

        Args:
            workflow_str (str): Expected to contain a string representation of a
                workflow that is formatted as '{ rules }' where rules are
                comma-separated rule strings enclosed within a pair of curly braces.

        """
        self.name, rules_str = workflow_str.strip("}").split("{")
        self.rules = [Rule(rule) for rule in rules_str.split(",")]

    def apply(self, part: Part):
        """
        Matches a given `part` against a set of rules, returning the destination
        of the first matching rule.

        Args:
            part (Part): Passed to the `apply` method of each rule in the `self.rules`
                list.

        Returns:
            Ruledestinationtype: Destinatetyperepresented by the attribute `dest`
            of the rule that successfully applies to the given `part`.

        """
        for rule in self.rules:
            if rule.apply(part):
                return rule.dest

    def rules_that_win(self, rules=List[Rule]):
        """
        Generates all possible combinations of rules that can lead to a win in a
        workflow, considering the destination and criterion of each rule.

        Args:
            rules (List[Rule]): Optional, with a default value.

        Returns:
            List[List[Rule]]: A list of lists of rules that satisfy certain conditions.

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
        Returns a string representation of the Worflow object, including its name
        and a list of rules. This string can be used for debugging or logging purposes.

        Returns:
            str: A string representation of the object, specifically a formatted
            string describing a workflow and its rules.

        """
        return f"""
Workflow {self.name}:
Rules:
{self.rules}"""


class Criteria:
    """
    Calculates the number of possible values for a set of criteria based on given
    rules. It counts the possible values for each criterion and returns the total
    number of possible combinations.

    Attributes:
        criteria (List[str]): Initialized with a list of strings, each representing
            a criterion.

    """
    def __init__(self, rules=List[Rule]):
        """
        Initializes the object with a list of rules. It extracts the criterion
        from each rule and stores them in the `criteria` attribute, which is a
        list of criterion values.

        Args:
            rules (List[Rule]): Optional, defaulting to an empty list if not
                provided. It is expected to contain one or more Rule objects.

        """
        self.criteria = [r.criterion for r in rules]

    def count_possible(self, c: chr):
        """
        Calculates the number of possible values for a given character c, based
        on predefined criteria stored in the `self.criteria` list. The criteria
        define minimum and maximum values for each character, bounded by '>' and
        '<' symbols.

        Args:
            c (chr): Described as a character.

        Returns:
            int: The number of possible values for a given character `c`, based
            on a set of predefined criteria stored in `self.criteria`.

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
        count of each character ("s", "a", "m", "x") separately.

        Returns:
            int: The product of the number of possible ways to form each character
            in the string "samx".

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
