try:
    import urllib2
except ImportError:
    from urllib.request import urlopen
response = urlopen('http://v4.ifconfig.co/ip')
HOSTNAME = response.read()
