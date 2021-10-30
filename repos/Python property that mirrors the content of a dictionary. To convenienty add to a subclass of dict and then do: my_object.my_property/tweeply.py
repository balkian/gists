class MessageProperty(property):
    def __init__(self, path, *args, **kwargs):
        property.__init__(self, *args, **kwargs)
        self.path = path

    def _target(self, dic):
        path = self.path
        dest = dic
        lastkey = path[-1]
        for p in path[:-1]:
            if p not in dest or not dest[p]:
                dest[p] = {}
            dest = dest[p]
        return dest, lastkey

    def __get__(self, container, _type=None):
        dest, lastkey = self._target(container)
        return dest[lastkey]


    def __set__(self, container, value):
        dest, lastkey = self._target(container)
        dest[lastkey] = value

    def __delete__(self, container):
        dest, lastkey = self._target(container)
        del dest[lastkey]
