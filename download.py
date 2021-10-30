#!/usr/bin/env python -B

from github import Github	# pip install PyGithub
import json
import os
from pathlib import Path

all = []

g = Github(open(os.path.expanduser(".gist")).read().strip())

repos = Path("repos")

for gist in g.get_user().get_gists():
    if not gist.public:
        print(f"Not cloning secret gist: {gist.id} - {gist.description}")
        continue

    path = repos / gist.id
    if os.path.exists(path):
        print(f"Repository exists already: {path}")
        continue

    all.append({
        "id"            : gist.id,
        "description"   : gist.description,
        "public"        : gist.public,
        "clone"         : gist.git_pull_url,
        "updated"       : gist.updated_at.isoformat(),
        "url"           : gist.url,
    })

    # yuck
    os.system(f"git remote add '{gist.id}' '{gist.git_pull_url}'")
    cmd = f"git subtree add --prefix '{path}' '{gist.id}' master"
    print(f'Running {cmd}')
    os.system(cmd)
    #os.system(f"git submodule add '{0}' repos/{1}".format(gist.git_pull_url, gist.id))
    #import pdb;pdb.set_trace()


with open("index.json", "w") as f:
    f.write(json.dumps(all, indent=4) + "\n")
