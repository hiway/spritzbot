class dotdictify(dict):
    """
    Code courtesy: Mike DeSimone on StackOverflow
    http://stackoverflow.com/questions/3797957/python-easily-access-deeply-nested-dict-get-and-set
    """
    def __init__(self, value=None):
        if value is None:
            pass
        elif isinstance(value, dict):
            for key in value:
                self.__setitem__(key, value[key])
        else:
            raise TypeError, 'expected dict'

    def __setitem__(self, key, value):
        if '.' in key:
            myKey, restOfKey = key.split('.', 1)
            target = self.setdefault(myKey, dotdictify())
            if not isinstance(target, dotdictify):
                raise KeyError, 'cannot set "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
            target[restOfKey] = value
        else:
            if isinstance(value, dict) and not isinstance(value, dotdictify):
                value = dotdictify(value)
            dict.__setitem__(self, key, value)

    def __getitem__(self, key):
        if '.' not in key:
            return dict.__getitem__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            raise KeyError, 'cannot get "%s" in "%s" (%s)' % (restOfKey, myKey, repr(target))
        return target[restOfKey]

    def __contains__(self, key):
        if '.' not in key:
            return dict.__contains__(self, key)
        myKey, restOfKey = key.split('.', 1)
        target = dict.__getitem__(self, myKey)
        if not isinstance(target, dotdictify):
            return False
        return restOfKey in target

    def setdefault(self, key, default):
        if key not in self:
            self[key] = default
        return self[key]

    __setattr__ = __setitem__
    __getattr__ = __getitem__
