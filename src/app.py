from flask import Flask
from Blockchains import get_all_liquidity_by_user
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
@cross_origin()
def helloWorld():
  return {"key": "Hello, cross-origin-world!"}


@app.route("/userInfo/<address>")
@cross_origin()
def get_liquidity_by_user(address):
    return get_all_liquidity_by_user(address)


