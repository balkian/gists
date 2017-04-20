Clone the repo
```
git clone https://github.com/gsi-upm/sitc
```

Run jupyter either through the `jupyter notebook` command, or with docker:

```
docker run -v $PWD/:/home/jovyan/work/ -p 8888:8888 jupyter/scipy-notebook
```

Visit the URL you'll get, or copy the code.