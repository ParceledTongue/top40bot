import sys
from collections import OrderedDict

DEFAULT_SIZE = 1500

class History(object):
    def __init__(self, size = DEFAULT_SIZE):
        self.size = size
        self.hist = OrderedDict()

    def __contains__(self, item):
        return (item in self.hist)

    def __repr__(self):
        return 'History(' + self.hist.keys().__repr__() + ')'

    def __str__(self):
        return 'History(' + self.hist.keys().__str__() + ')'
  
    def add(self, item):
        """
        If item is already in history, just move it to the front.
        (One of the main purposes of this class is to have constant-time
        access to items in the history, so we need a hash. Ergo, we don't
        support duplicate entries.)
        """
        if item in self.hist:
            self.hist.pop(item)
        self.hist[item] = None
        if len(self.hist) > self.size:
            self.hist.popitem(last = False)

    def delete(self, item):
        try:
            self.hist.pop(item)
        except KeyError as e:
            raise e(item)

    def clear(self):
        self.hist = OrderedDict()

