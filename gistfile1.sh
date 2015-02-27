git clone <your_project> <your_submodule>
cd <your_submodule>
git filter-branch --subdirectory-filter 'path/to/your/submodule' --prune-empty -- --all