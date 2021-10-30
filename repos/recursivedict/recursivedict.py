class RecursiveDict(UserDict):

    def __getitem__(self, k):
        if not isinstance(k, Iterable):
            return self.data[k]
        dest = self.data
        for j in k:
            dest = dest[j]
        return dest

    def __setitem__(self, k, v):
        if not isinstance(k, Iterable):
            return self.data[k] = v
        levels = len(k)
        dest = self.data
        for j in range(levels-1):
            if k[j] not in dest:
                dest[k[j]] = {}
            dest = dest[k[j]]
        dest[levels-1] = v
