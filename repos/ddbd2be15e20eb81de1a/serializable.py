cls = self.__class__
property_names=[]

for p in dir(cls):
    if isinstance(getattr(cls, p), property):
        property_names.append(p)
        logging.debug('property names: {}'.format(property_names))
for p in property_names:
    ser['@%s' % p] = getattr(cls, p).fget(self)