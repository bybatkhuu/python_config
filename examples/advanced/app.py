#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

from flask import Flask

from config import config


print("LOADED CONFIG:")
pprint(config.to_dict())
print()


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(host=config.app.host, port=config.app.port)
