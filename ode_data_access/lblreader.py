from __future__ import unicode_literals, print_function, absolute_import, division


class LBLReader:
    def __init__(self):
        self._map = {}

    def read(self, fname):
        """reads in a lbl file named fname to a list"""
        lines = open(fname, 'r').readlines()
        if len(lines) == 0:
            raise ValueError('This lbl file is empty')
        stringpairs = []
        for line in lines:
            tokens = line.split('=')
            if len(tokens) >= 2:
                stringpairs.append([])
            for token in tokens:
                if token.strip().startswith('/*'):
                    continue
                stringpair = stringpairs[-1]
                if len(stringpair) <= 1:
                    stringpair.append(token.strip())
                else:
                    stringpair[-1] += ' ' + token.strip()

        self.process(stringpairs)

    def process(self, stringpairs):
        for stringpair in stringpairs:
            self._map[stringpair[0]] = stringpair[1] if len(stringpair) > 1 else ''

    def get(self, key):
        return self._map[key] if key in self._map else None
