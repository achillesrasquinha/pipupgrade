from flask import Flask

from pipupgrade import __name__
from pipupgrade.app.response import Response

app = Flask(__name__)

@app.route("/")
def index():
    response = Response()
    return response.json