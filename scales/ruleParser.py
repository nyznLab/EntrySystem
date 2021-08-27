class RuleParser(object):
    # 操作字典
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
        '/': 'divide',
    }

    def equals(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
        return float(getattr(answer, args[0])) == float(args[1])

    def not_equals(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
        return float(getattr(answer, args[0])) != float(args[1])

    def grater(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
        return float(getattr(answer, args[0])) > float(args[1])

    def grater_equals(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
        return float(getattr(answer, args[0])) >= float(args[1])

    def lower(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
        return float(getattr(answer, args[0])) < float(args[1])

    def lower_equals(self, answer, *args):
        print("RuleParser")
        print(getattr(answer, args[0]))
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

    # 校验规则是否合法
    def validate(self, rules):
        # 规则表达式必须是列表
        if not isinstance(rules, list):
            raise ValueError('Rule must be a list, got {}'.format(type(rules)))
        # 规则操作数至少三个
        if len(rules) <= 2:
            raise ValueError('Must have at least one argument.')
        # 操作必须是支持的操作类型
        opt = rules[0]
        if str(opt).lower() not in self.ALIAS.keys():
            raise ValueError("option {} invalid".format(opt))
        # 递归判断 因为规则操作数也可以是一个表达式
        for rule in rules[1:]:
            if isinstance(rule, list):
                self.validate(rule)
        return True

    # 计算规则结果
    def evaluate(self, answer, rules):
        # 通过反射取到对应计算的方法
        func = getattr(self, self.ALIAS[rules[0]])
        if not isinstance(rules[1], list) and not isinstance(rules[2], list):
            # 如果后两个操作数都不是列表（说明后面的操作数不是新的表达式）则直接计算 把结果返回
            ans = func(answer, rules[1], rules[2])
            print(func, rules[1:], ans)
            return ans
        # 后面的操作数是表达式 先依次把他们计算出来 再计算
        args = [self.evaluate(answer, x) for x in rules[1:]]
        ans = func(args)
        print(func, args, ans)
        return ans
