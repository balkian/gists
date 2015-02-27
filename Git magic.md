#GIT MAGIC

## Create a submodule from a specific folder
```
git clone <your_project> <your_submodule>
cd <your_submodule>
git filter-branch --subdirectory-filter 'path/to/your/submodule' --prune-empty -- --all
```

## Remove a file from history

```
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch \#web40.tex\#' \
--prune-empty --tag-name-filter cat -- --all
```