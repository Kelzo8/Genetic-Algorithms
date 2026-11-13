import operator


def protected_div(a, b):
    return a / b if abs(b) > 1e-6 else 1.0


FUNCTIONS = {
    '+': (operator.add, 2),
    '-': (operator.sub, 2),
    '*': (operator.mul, 2),
    '/': (protected_div, 2),
    'neg': (operator.neg, 1),
}

TERMINALS = ['x', 1, 2]