#!/usr/bin/python3
""" runs site Application """
from App.v1 import app


if __name__ == "__main__":
    """ main function """
    app.run(host="0.0.0.0", port=5000)
