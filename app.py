from flask import Flask, request, render_template, redirect
from modules.requester import Requester
import asyncio

loop = asyncio.get_event_loop()

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('base.html')

@app.route('/', methods=['POST', "GET"])
def getter():
    quot_id = request.form['text']
    transaction = Requester(quot_id)
    resp = loop.run_until_complete(transaction.do_req())
    # print(resp) # = HEHE minor debugging
    return resp

@app.route('/success', methods=['POST', "GET"])
def succ():
    return "hi"

app.run(debug=True)