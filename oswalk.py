import os

def process_file(f):
  print(json.load(f.read())

for root, dirs, files in os.walk('semeval'):
    """ Find every file in the folder tree that matches **.json
    """
    for file in files:
      if file.endswith(".json"):
        with open(os.path.join(root, file)) as w:
            process_file(w)