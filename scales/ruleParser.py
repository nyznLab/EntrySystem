class RuleParser(object):

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

    def equals(self, answer, *args):
        # return args[0] == args[1]
        print(type(answer))
        return float(getattr(answer, args[0])) == float(args[1])

    def not_equals(self, answer, *args):
        return float(getattr(answer, args[0])) != float(args[1])

    def grater(self, answer, *args):
        return float(getattr(answer, args[0])) > float(args[1])

    def grater_equals(self, answer, *args):
        return float(getattr(answer, args[0])) >= float(args[1])

    def lower(self, answer, *args):
        return float(getattr(answer, args[0])) < float(args[1])

    def lower_equals(self, answer, *args):
        return float(getattr(answer, args[0])) <= float(args[1])

    @staticmethod
    def or_(answer, args):
        return any(args)

    @staticmethod
    def and_(answer, args):
        return all(args)

    def plus(self, answer, *args):
        return float(getattr(answer, args[0])) + float(getattr(answer, args[1]))

    def minus(self, answer, *args):
        return float(getattr(answer, args[0])) - float(getattr(answer, args[1]))

    def multiply(self, answer, *args):
        return float(getattr(answer, args[0])) * float(getattr(answer, args[1]))

    def divide(self, answer, *args):
        return float(getattr(answer, args[0])) / float(getattr(answer, args[1]))

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

    def evaluate(self, answer, rules):
        func = getattr(self, self.ALIAS[rules[0]])
        if not isinstance(rules[1], list) and not isinstance(rules[2], list):
            ans = func(answer, rules[1], rules[2])
            print(func, rules[1:], ans)
            return ans
        args = [self.evaluate(answer, x) for x in rules[1:]]
        ans = func(args)
        print(func, args, ans)
        return ans
