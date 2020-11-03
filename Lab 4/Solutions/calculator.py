import sys
import operator
import enum
import re

class SymbolType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_LPAR = 5
    T_RPAR = 6
    T_END = 7

operations = {
    SymbolType.T_PLUS: operator.add,
    SymbolType.T_MINUS: operator.sub,
    SymbolType.T_MULT: operator.mul,
    SymbolType.T_DIV: operator.truediv
}

class Node:
    def __init__(self, symbol_type, value=None):
        self.symbol_type = symbol_type
        self.value = value
        self.children = []
     
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret


def lexical_analysis(s):
    mappings = {
        '+': SymbolType.T_PLUS,
        '-': SymbolType.T_MINUS,
        '*': SymbolType.T_MULT,
        '/': SymbolType.T_DIV,
        '(': SymbolType.T_LPAR,
        ')': SymbolType.T_RPAR}

    tokens = []
    for c in s:
        if c in mappings:
            symbol_type = mappings[c]
            token = Node(symbol_type, value=c)
        elif re.match(r'\d', c):
            token = Node(SymbolType.T_NUM, value=int(c))
        else:
            raise Exception('Invalid token: {}'.format(c))
        tokens.append(token)
    tokens.append(Node(SymbolType.T_END))
    return tokens


def match(tokens, token):
    if tokens[0].symbol_type == token:
        return tokens.pop(0)


def parse_e(tokens):
    return parse_ea(tokens, parse_e2(tokens))


def parse_ea(tokens, left_node):
    if tokens[0].symbol_type in [SymbolType.T_PLUS, SymbolType.T_MINUS]:
        node = tokens.pop(0)
        node.children.append(left_node)
        next_node = parse_e(tokens)

        if next_node.symbol_type in [SymbolType.T_PLUS, SymbolType.T_MINUS]:
            next_left_node = next_node.children[0]
            node.children.append(next_left_node)
            next_node.children[0] = node
            return next_node

        node.children.append(next_node)
        return node
    elif tokens[0].symbol_type in [SymbolType.T_RPAR, SymbolType.T_END]:
        return left_node


def parse_e2(tokens):
    return parse_e2a(tokens, parse_e3(tokens))


def parse_e2a(tokens, left_node):
    if tokens[0].symbol_type in [SymbolType.T_MULT, SymbolType.T_DIV]:
        node = tokens.pop(0)
        node.children.append(left_node)
        next_node = parse_e(tokens)

        if next_node.symbol_type in [SymbolType.T_MULT, SymbolType.T_DIV]:
            next_left_node = next_node.children[0]
            node.children.append(next_left_node)
            next_node.children[0] = node
            return next_node

        node.children.append(next_node)
        return node
    elif tokens[0].symbol_type in [SymbolType.T_PLUS, SymbolType.T_MINUS, SymbolType.T_END, SymbolType.T_RPAR]:
        return left_node


def parse_e3(tokens):
    if tokens[0].symbol_type == SymbolType.T_NUM:
        return tokens.pop(0)
    match(tokens, SymbolType.T_LPAR)
    e_node = parse_e(tokens)
    match(tokens, SymbolType.T_RPAR)
    return e_node


def parse(inputstring):
    tokens = lexical_analysis(inputstring)
    ast = parse_e(tokens)
    match(tokens, SymbolType.T_END)
    return ast


def compute(node):
    if node.symbol_type == SymbolType.T_NUM:
        return node.value
    left_result = compute(node.children[0])
    right_result = compute(node.children[1])
    operation = operations[node.symbol_type]
    return operation(left_result, right_result)

    
if __name__ == '__main__':
    #tree = parser.parse(sys.argv[1])
    tree = parse('(1+7)*(9+2)')
    result = compute(tree)
    print(result)
    print(tree)