import sys
import operator
import enum
import re
import sys
import math
from tkinter import *

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

    
def parseOper(operationsStr):
    mathres = 0;
    exs = operationsStr
    if "sqrt" in operationsStr:
        index1 = operationsStr.find("sqrt(") + 5
        index2 = operationsStr.find(")", index1)
        mathres = int(math.sqrt(int(operationsStr[index1:index2])))
        exs = operationsStr[:index1 - 5] + str(mathres) + operationsStr[index2 + 1:]
        if "sqrt" in operationsStr:
            exs = parseOper(exs)
            
    if "factorial" in operationsStr:
        index1 = operationsStr.find("factorial(") + 10
        index2 = operationsStr.find(")", index1)
        mathres = int(math.factorial(int(operationsStr[index1:index2])))
        exs = operationsStr[:index1 - 10] + str(mathres) + operationsStr[index2 + 1:]
        if "factorial" in operationsStr:
            exs = parseOper(exs)
            
    if "log" in operationsStr:
        index1 = operationsStr.find("log(") + 4
        index2 = operationsStr.find(")", index1)
        mathres = int(math.log10(int(operationsStr[index1:index2])))
        exs = operationsStr[:index1 - 4] + str(mathres) + operationsStr[index2 + 1:]
        if "log" in operationsStr:
            exs = parseOper(exs)
            
    if "mod" in operationsStr:
        index1 = operationsStr.find("mod(") + 4
        index2 = operationsStr.find(")", index1)
        masMod = operationsStr[index1:index2].split(",")
        try:
            mathres = int(math.fmod(int(masMod[0]), int(masMod[1])))
        except ValueError as e:
            print("error")
            
        exs = operationsStr[:index1 - 4] + str(mathres) + operationsStr[index2 + 1:]
        if "mod" in operationsStr:
            exs = parseOper(exs)
            
    if "pow" in operationsStr:
        index1 = operationsStr.find("pow(") + 4
        index2 = operationsStr.find(")", index1)
        masMod = operationsStr[index1:index2].split(",")
        try:
            mathres = int(math.pow(int(masMod[0]), int(masMod[1])))
        except ValueError as e:
            print("error")
            
        exs = operationsStr[:index1 - 4] + str(mathres) + operationsStr[index2 + 1:]
        if "pow" in operationsStr:
            exs = parseOper(exs)
          
    if "|" in operationsStr:
        index1 = operationsStr.find("|") + 1
        index2 = operationsStr.find("|", index1)
        try:
            mathres = abs(int(operationsStr[index1:index2]))
        except ValueError as e:
            print("error")

        exs = operationsStr[:index1 - 1] + str(mathres) + operationsStr[index2 + 1:]
        if "|" in operationsStr:
            exs = parseOper(exs) 
    return exs
        

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
    
#-----------------GUI--------------------------

def iCalc(source, side):
    storeObj = Frame(source, borderwidth=4, bd=4, bg="powder blue")
    storeObj.pack(side=side, expand =YES, fill =BOTH)
    return storeObj
 
def button(source, side, text, command=None):
    storeObj = Button(source, text=text, command=command)
    storeObj.pack(side=side, expand = YES, fill=BOTH)
    return storeObj
 
class app(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.option_add('*Font', 'arial 20 bold')
        self.pack(expand = YES, fill =BOTH)
        self.master.title('Calculator')
 
        display = StringVar()
        Entry(self, relief=RIDGE, textvariable=display,
          justify='right'
          , bd=30, bg="powder blue").pack(side=TOP,
                                          expand=YES, fill=BOTH)
 
        for clearButton in (["C"]):
            erase = iCalc(self, TOP)
            for ichar in clearButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(''))
 
        for numButton in ("789/", "456*", "123-", "0.,+", "()"):
         FunctionNum = iCalc(self, TOP)
         for iEquals in numButton:
            button(FunctionNum, LEFT, iEquals, lambda
                storeObj=display, q=iEquals: storeObj
                   .set(storeObj.get() + q))
 
        EqualButton = iCalc(self, TOP)
        for iEquals in "=":
            if iEquals == '=':
                btniEquals = button(EqualButton, LEFT, iEquals)
                btniEquals.bind('<ButtonRelease-1>', lambda e,s=self,
                                storeObj=display: s.calc(storeObj), '+')


            else:
                btniEquals = button(EqualButton, LEFT, iEquals,
                                    lambda storeObj=display, s=' %s ' % iEquals: storeObj.set
                                    (storeObj.get() + s))
 
        for sqrtButton in (["s"]):
            erase = iCalc(self, LEFT)
            for ichar in sqrtButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + 'sqrt('))
                    
        for silniaButton in (["!"]):
            erase = iCalc(self, LEFT)
            for ichar in silniaButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + 'factorial('))
                    
        for logButton in (["L"]):
            erase = iCalc(self, LEFT)
            for ichar in logButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + 'log('))
 
        for modButton in (["m"]):
            erase = iCalc(self, LEFT)
            for ichar in modButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + 'mod('))
        
        for pButton in (["^"]):
            erase = iCalc(self, LEFT)
            for ichar in pButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + 'pow('))
                    
        for moduleButton in (["|"]):
            erase = iCalc(self, LEFT)
            for ichar in moduleButton:
                button(erase, LEFT, ichar, lambda
                    storeObj=display, q=ichar: storeObj.set(storeObj.get() + '|'))  
                            
    def calc(self, display):
        ex = parseOper(display.get())
        tree = parse(ex)
        result = compute(tree)
        
        try:
            display.set(result)
        except:
            display.set("ERROR")
            
        print(result)
        print(tree)

 
if __name__=='__main__':
 app().mainloop()