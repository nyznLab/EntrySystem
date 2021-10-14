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
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 == opt2

    def not_equals(self, answer, *args):
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 != opt2

    def grater(self, answer, *args):
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 > opt2

    def grater_equals(self, answer, *args):
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 >= opt2

    def lower(self, answer, *args):
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 < opt2

    def lower_equals(self, answer, *args):
        opt1 = args[0]
        opt2 = args[1]
        if isinstance(args[0], str):
            opt1 = float(getattr(answer, args[0]))
        if isinstance(args[0], str):
            opt2 = float(getattr(answer, args[1]))
        return opt1 <= opt2

    @staticmethod
    def or_(answer, *args):
        return any(args)

    @staticmethod
    def and_(answer, *args):
        return all(args)

    def plus(self, answer, *args):
        ans = 0
        for arg in args:
            if isinstance(arg, str):
                ans += getattr(answer, arg)
            else:
                ans += arg
        return float(ans)

    def minus(self, answer, *args):
        ans = args[0]
        if isinstance(args[0], str):
            ans = float(getattr(answer, args[0]))
        for arg in args[1:]:
            if isinstance(arg, str):
                ans -= getattr(answer, arg)
            else:
                ans -= arg
        return float(ans)

    def multiply(self, answer, *args):
        ans = 0
        for arg in args:
            if isinstance(arg, str):
                ans *= getattr(answer, arg)
            else:
                ans *= arg
        return float(ans)

    def divide(self, answer, *args):
        ans = args[0]
        if isinstance(args[0], str):
            ans = float(getattr(answer, args[0]))
        for arg in args[1:]:
            if isinstance(arg, str):
                ans /= getattr(answer, arg)
            else:
                ans /= arg
        return float(ans)

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
        for index, expression in enumerate(rules[1:]):
            # 遍历后面的操作数 如果操作数也是一个表达式 则先计算子表达式
            if isinstance(expression, list):
                expression_answer = self.evaluate(answer, expression)
                rules[index + 1] = expression_answer
        ans = func(answer, *rules[1:])
        return ans
