from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    returnDict = {'response': "Make A request Above to get the response"}
    return render_template("index.html", data=returnDict)


@app.route('/request', methods=['POST'])
def requestFunction():
    requestString = "The request you made was: " + request.form['requestValue']
    resultString = "The result of that request was: (Nothing Because I don't have a database setup)"
    returnDict = {'response': requestString, 'result': resultString}
    return render_template("index.html", data=returnDict)


if __name__ == '__main__':
    app.run()
