 # -*- coding: utf-8 -*-
from rdflib import Graph, plugin
from rdflib.serializer import Serializer
import sys

g = Graph().parse(sys.argv[1], format='json-ld')
print "Hooray! It seems to be a valid json-ld file!"