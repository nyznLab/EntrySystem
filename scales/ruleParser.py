
class RuleParser(object):

    def __init__(self, answer):
        self.answer = answer

    ALIAS = {
        '==': 'equals',
        '!=': 'not_equals',
        '>': 'grater',
        '>=': 'grater_equals',
        '<': 'lower',
        '<=': 'lower_equals',
        'and': 'and_',
        'or': 'or_',
        '+': 'plus',
        '-': 'minus',
        '*': 'multiply',
        '/': 'divide'
    }

    @staticmethod
    def equals(*args):
        return args[0] == args[1]
        # return getattr(self.answer, args[0]) == args[1]

    @staticmethod
    def not_equals(*args):
        return args[0] != args[1]

    @staticmethod
    def grater(*args):
        return args[0] > args[1]

    @staticmethod
    def grater_equals(*args):
        return args[0] >= args[1]

    @staticmethod
    def lower(*args):
        return args[0] < args[1]

    @staticmethod
    def lower_equals(*args):
        return args[0] <= args[1]

    @staticmethod
    def or_(args):
        return any(args)

    @staticmethod
    def and_(args):
        return all(args)

    @staticmethod
    def plus(*args):
        return sum(args)

    @staticmethod
    def minus(*args):
        return args[0] - args[1]

    @staticmethod
    def multiply(*args):
        return args[0] * args[1]

    @staticmethod
    def divide(*args):
        return float(args[0]) / float(args[1])

    def validate(self, rules):
        if not isinstance(rules, list):
            raise ValueError('Rule must be a list, got {}'.format(type(rules)))
        if len(rules) <= 2:
            raise ValueError('Must have at least one argument.')

        opt = rules[0]
        if str(opt).lower() not in self.ALIAS.keys():
            raise ValueError("option {} invalid".format(opt))
        for rule in rules[1:]:
            if isinstance(rule, list):
                self.validate(rule)
        return True

    def evaluate(self, rules):
        func = getattr(self, self.ALIAS[rules[0]])
        if not isinstance(rules[1], list) and not isinstance(rules[2], list):
            ans = func(rules[1], rules[2])
            print(func, rules[1:], ans)
            return ans
        args = [self.evaluate(x) for x in rules[1:]]
        ans = func(args)
        print(func, args, ans)
        return ans


if __name__ == "__main__":
    my_rules = [
        "and",
        [">", 5, 3],
        [">", 10, 2],
        [
            "or",
            ["<=", 12, 5],
            ["!=", 12, 11],
            ["==", 13, 13],
        ],
    ]
    rule_parser = RuleParser()
    # print(rule_parser.validate(my_rules))
    print(rule_parser.evaluate(my_rules))
