from typing import List

INPUT = "input"


class Part:
    def __init__(self, part_str: str):
        self.ratings = {
            k: int(v)
            for k, v in dict(
                [x.split("=") for x in part_str.strip("{}").split(",")]
            ).items()
        }
        self.value = sum(self.ratings.values())

    def apply(self, workflows):
        dest = "in"
        while dest not in ["A", "R"]:
            dest = workflows[dest].apply(self)
        return dest

    def __repr__(self):
        return f"Part: {self.ratings}"


class Rule:
    def __init__(self, rule_str: str):
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
    def __init__(self, workflow_str: str):
        self.name, rules_str = workflow_str.strip("}").split("{")
        self.rules = [Rule(rule) for rule in rules_str.split(",")]

    def apply(self, part: Part):
        for rule in self.rules:
            if rule.apply(part):
                return rule.dest

    def rules_that_win(self, rules=List[Rule]):
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
        return f"""
Workflow {self.name}:
Rules:
{self.rules}"""


class Criteria:
    def __init__(self, rules=List[Rule]):
        self.criteria = [r.criterion for r in rules]

    def count_possible(self, c: chr):
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
