a = u"codificación"
print a # u"codificación"
print type(a) # <type 'unicode'>
b = a.encode("utf-8")
print b # codificación # But it depends on your terminal settings
print type(b) # <type 'str'>
c = b.decode("utf-8")
print type(c) # <type 'unicode'>
print c # u"codificación"