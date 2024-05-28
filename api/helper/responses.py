from flask import json


OK_RESPONSE = json.dumps({'success':True}), 200, {'ContentType':'application/json'} 