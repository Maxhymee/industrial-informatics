from flask import Flask
import controller

app = Flask(__name__)


@app.route('/hello', methods=['GET'])
def helloWorld():
    print("Hello world endpoint")
    return "Hello World"


@app.route('/start', methods=['GET'])
def startThreads():
    return controller.startThreads()


if __name__ == '__main__':
    app.run()
