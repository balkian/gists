import glob
import json

def process_file(f):
  print(json.load(f.read())

for f in glob.glob('semeval/*.json'):
    """ Find every file in the semeval folder that matches **.json
    """

    with open(f) as w:
        process_file(w)