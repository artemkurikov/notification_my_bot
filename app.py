from flask import Flask, request, jsonify
from json import load as js_load, dump as js_dump, dumps as js_dumps, loads as js_loads
import sys

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/new_notif', methods=['POST'])
def new_notif():
    with open('notif.json', 'r') as file:
        file_js = js_load(file)
        file.close()

    file_js.append(request.json)
    with open('notif.json', 'w') as file:
        js_dump(file_js, file, indent=1,ensure_ascii=False)
        file.close()
    
    return '200'

@app.route('/notif_list', methods=['GET'])
def return_notif_list():
    with open('notif.json', 'r') as file:
        file_js = js_load(file)
        file.close()
    
    return jsonify(file_js), 200

@app.route('/del_notif', methods=['PUT'])
def delete_notif():
    with open('notif.json', 'r') as file:
        file_js = js_load(file)
        file.close()
    file_js.remove(js_loads(request.json()))

    with open('notif.json', 'w') as file:
        js_dump(file_js, file, indent=1,ensure_ascii=False)
        file.close()
    return '',200
