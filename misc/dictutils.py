class DictWrapper(object):
    """
        DictWrapper allow syntax vDict.key to get value or
            vDict.key = value to set value:

            vDict = DictWrapper(original_dict)

            As private member _dict has original dict
    """

    # original dict
    _dict = None

    # constructor takes source dict, lowercase and uppercase
    # are modificators to key names
    def __init__(self, d, lowercase=False, uppercase=False):

        self._dict = d

        for a, b in self._dict.items():

            if lowercase:
                a = str(a).lower()
            elif uppercase:
                a = str(a).upper()
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [self.__class__(x)
                                      if isinstance(x, dict)
                                      else x for x in b])
            else:
                setattr(
                    self, a, self.__class__(b) if isinstance(b, dict) else b
                )

    # makes DictWrapper instance to iterable
    def __iter__(self):
        return self

    # string representation
    def __str__(self):
        return str(self._dict)
