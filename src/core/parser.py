"""
:Author: Theodor A. Dumitrescu
:Date: 03/06/20
:Version: 0.0.1
"""
from __future__ import print_function

import logging

import scanner as lex

NULLTOKEN = -1

LITERAL = 0

NOT = 30
AND = 31
OR = 32
IMP = 33
EQ = 34

LPAREN = 50
RPAREN = 51

ATOM = 1000
UNARY = 1001
BINARY = 1002

u_operators = (NOT,)
b_operators = (AND, OR, IMP, EQ,)

FIRST = (LITERAL, LPAREN, NOT, )

rules = ([
    ('SPACES', r'\s+'),

    (AND, r'and'),
    (OR, r'or'),
    (NOT, r'not'),
    (IMP, r'=>'),
    (EQ, r'<=>'),

    (LITERAL, r'[a-zA-Z][a-zA-Z0-9]*'),

    (LPAREN, r'\('),
    (RPAREN, r'\)'),

    (NULLTOKEN, r'null_token')
])


def isUnitary(op):
    return op in u_operators


def isBinary(op):
    return op in b_operators


def isOperator(op):
    return isBinary(op) or isUnitary(op)


class TokenizerException(Exception):
    pass


class ParserException(Exception):
    def __init__(self, str):
        super(Exception, self).__init__('ParserException: ' + str)


class Exp(object):
    """
    The pars tree of an expression.
    A node could be of two forms unitary or binary.
    If the operation is binary, the related information is stored in the left and right attributes.
    If the operation is unitary the related information is stored in the child attribute.
    """
    __hash__ = None

    def __init__(self, str_exp=None, kind=None, scanner=None):
        """
        Generate the tree from the tokenized expression.
        If the expression is specified then it will create an empty node.
        """
        self.kind = None
        self.name = 'undef'
        self.attr = None
        self.child = None
        self.left = None
        self.right = None
        self.code = None

        if str_exp is not None:
            logging.debug('========== EXP in init(NODE): SEXP = [' + str_exp + ']')
            scanner = lex.Scanner(rules)
            scanner.setString(str_exp)

        if kind is not None:  # create an empty node
            self.kind = kind
            return

        if scanner is None:
            raise Exception('Fatal Error: scanner not defined')

        while scanner.curToken().type in FIRST:

            if scanner.curToken().type == LITERAL:
                self.name = scanner.curToken().name
                self.code = LITERAL
                self.kind = ATOM
                scanner.move()

            elif scanner.curToken().type == LPAREN:
                scanner.move()  # skip the parentheses

                tmp = Exp(scanner=scanner)  # tree of the expression between parentheses
                self.kind = tmp.kind
                self.attr = tmp.attr
                self.name = tmp.name
                self.left = tmp.left
                self.right = tmp.right
                self.child = tmp.child

                if scanner.curToken().type != RPAREN:
                    raise ParserException("')' expected")
                scanner.move()

            elif isUnitary(scanner.curToken().type):
                self.kind = UNARY
                self.name = scanner.curToken().name
                self.code = scanner.curToken().type

                # if token_type == ATTRIB # this is for existence and foreach

                scanner.move()
                self.child = Exp(scanner=scanner)

            # the scanner has been moved to a successive token
            if scanner.curToken().type == NULLTOKEN:
                break

            # check for infix operators
            if isBinary(scanner.curToken().type):
                operator_name = scanner.curToken().name
                operator_type = scanner.curToken().type
                scanner.move()

                # move the current node to the left of the tree
                lnode = Exp(kind=self.kind)
                lnode.name = self.name
                lnode.attr = self.attr
                lnode.child = self.child
                lnode.left = self.left
                lnode.right = self.right
                lnode.code = self.code

                # this node became the handler aka the binary operator
                self.code = operator_type
                self.name = operator_name
                self.kind = BINARY
                self.left = lnode
                # lookup the second child of the operator
                self.right = Exp(scanner=scanner)

    def __str__(self):
        if self.code == LITERAL:
            return self.name
        elif self.kind == UNARY:
            return self.name + " (" + self.child.__str__() + ")"
        elif self.kind == BINARY:
            le = self.left.__str__()
            re = self.right.__str__()

            return le + ' ' + self.name + ' ' + re


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    s = '(A <=> not B)'
    exp = Exp(str_exp=s)
    print(exp)

'''
s = lex.Scanner(rules)
s.setString('A and B')

while s.curToken().type != NULLTOKEN:
    print('TOKEN =', str(s.curToken()))
    s.getToken()
'''
