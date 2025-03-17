from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
    return "<h2>Welcome to Main Page</h2>"

@app.route("/hello/<name>")
def sayHello(name):
    return "Hi {0}".format(name)

if __name__ =="__main__":
    app.run()