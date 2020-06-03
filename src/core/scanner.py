"""
:Author: Theodor A. Dumitrescu
:Date: 03/06/20
:Version: 0.0.1
"""

import logging

from sre_parse import Pattern, SubPattern, parse
from sre_compile import compile as sre_compile
from sre_constants import BRANCH, SUBPATTERN

NULLTOKEN = -1  # token 'nullo'


class Token:

    def __init__(self, t, s):
        self.type = t
        self.name = s

    def __str__(self):
        return "(" + str(self.type) + "," + str(self.name) + ")"


class Scanner(object):

    def __init__(self, rules, flags=0):
        pattern = Pattern()
        pattern.flags = flags
        pattern.groups = len(rules) + 1

        self.rules = [name for name, _ in rules]
        self._scanner = sre_compile(SubPattern(pattern, [
            (BRANCH, (None, [SubPattern(pattern, [
                (SUBPATTERN, (group, parse(regex, flags, pattern))),
            ]) for group, (_, regex) in enumerate(rules, 1)]))
        ])).scanner
        self.at = []  # array dei token
        self.idx = 0  # indice su at del token corrente

    def scan(self, string, skip=False):
        sc = self._scanner(string)

        match = None
        for match in iter(sc.search if skip else sc.match, None):
            yield self.rules[match.lastindex - 1], match

        """
        if not skip and not match or match.end() < len(string):
            raise EOFError(match.end())
        """

    # imposta la stringa da analizzare
    def setString(self, s):
        self.at = []
        self.idx = 0
        # print('settata stringa in scanner--------->',s)
        for token, match in self.scan(s):
            if token != 'SPACES':
                t = Token(token, match.group())
                # print('Scanner:TOK =',t)
                self.at.append(t)
        self.at.append(Token(NULLTOKEN, 'null_token'))  # per chiudere
        # print('TOKENS =',at)

    # token corrente
    def curToken(self):
        return self.at[self.idx]

    # token prossimo
    def nextToken(self):
        if (self.idx + 1) < len(self.at):
            return self.at[self.idx + 1]
        else:
            return Token(NULLTOKEN, 'null_token')

    # avanza al prossimo token e lo ritorna
    def getToken(self):
        if (self.idx + 1) < len(self.at):
            self.idx += 1
        return self.at[self.idx]

    def move(self):
        if (self.idx + 1) < len(self.at):
            self.idx += 1