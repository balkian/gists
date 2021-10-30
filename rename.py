import json
import os
from pathlib import Path

index = json.load(open('index.json', 'r'))

repos = Path('repos')

for repo in index:
    path = repos / repo["id"]
    if not os.path.exists(path):
        print(f'Repo {path} does not exist or it has already been moved')
        continue
    if repo['description']:
        print(f'Renaming: {repo["id"]} -> {repo["description"]}')
        os.rename(path, repos/repo["description"].replace('/', ' '))
    else:
        files = os.listdir(path)
        if len(files) == 1:
            onefile = files[0]
            fname = onefile.rsplit(".", 1)[0]
            os.rename(path, repos / fname)
