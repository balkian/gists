#!/usr/bin/python
from flask import Flask, request, Markup

app = Flask("prueba")

@app.route("/")
def home():
    args = ("<pre>")
    for i in request.args:
        a = request.args[i]
        args += u"{} [{}]: {}\n".format(i, Markup.escape(str(type(a))), a)
    args += "</pre>"
    return args

app.run(debug=True)
