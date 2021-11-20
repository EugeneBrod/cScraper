from flask import Flask, jsonify, request
from flask_cors import CORS
from my_cl_scraper import Scraper
from threading import Thread, Event


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'


class DataStore:
    thread = None
    STOP_EVENT = None
    INTERRUPT_EVENT = None
    urls = None
    recipient_emails = None
    owner_ip = None

data = DataStore()

def resetThread():
  data.STOP_EVENT = Event()
  data.INTERRUPT_EVENT = Event()
  data.thread = Scraper(data.STOP_EVENT, data.INTERRUPT_EVENT, data.recipient_emails, data.urls, data.owner_ip)

resetThread()
data.recipient_emails = []
data.urls = []
data.owner_ip = 0


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong dudes!')

@app.route('/setSettings', methods=['POST'])
def setSettings():
    post_data = request.get_json()
    data.recipient_emails = post_data['recipient_emails']
    data.urls = post_data['urls']
    print(data.urls)
    response_object = {"success": "true"}
    return jsonify(response_object)

@app.route('/start', methods = ["GET"])
def start():
    response_object = {"success": ""}
    if data.thread.is_alive():
        response_object["success"] = "false"
        print("thread in use")
    else:
        resetThread()
        data.thread.start()
        response_object["success"] = "true"
        print("good start")
    return jsonify(response_object)

@app.route('/stop', methods = ["GET"])
def stop():
    data.STOP_EVENT.set()
    data.thread.join()
    response_object = {"success": "true"}
    print("good stop")
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
