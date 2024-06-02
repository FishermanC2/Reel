from flask import json

# Prepared var to return 200
OK_RESPONSE = json.dumps({'success':True}), 200, {'ContentType':'application/json'} 