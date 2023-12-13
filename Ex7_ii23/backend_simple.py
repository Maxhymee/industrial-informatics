from flask import Flask, render_template
import json
import datetime

app = Flask(__name__)

@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('%s.html' % page_name)


@app.route('/conveyors/<id>/state', methods=['GET'])
def getState(id):
    print ("Retrieving the state of conveyor ID:"+id)
    now = datetime.datetime.now()
    time= now.isoformat();
    cnvMsg = {'conveyorID': 5, 'state': "working", "serverTime":time}
    cnvMsg_str = json.dumps(cnvMsg)
    return cnvMsg_str


if __name__ == '__main__':
    app.run()