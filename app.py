from flask import Flask, request

from datetime import datetime
import json
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware


app = Flask(__name__)

xray_recorder.configure(service='HelloApplicationSegment')
libraries = (['boto3'])
patch(libraries)
XRayMiddleware(app, xray_recorder)

@app.route('/')
def hello():
    return json.dumps({'message': 'Hello.'})


@app.route('/put', methods=['POST'])
def put():
    message = request.form['message']
    if (message is None) or (message == ''):
        return json.dumps({'message': 'Validation Error.'})
    try:
        put_message(message)
        return json.dumps({'message': 'Success.', 'put_message': message})
    except:
        return json.dumps({'message': 'Unexpected error.'})

def put_message(message):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table = dynamodb.Table('Table')
    response = table.put_item(
        Item={
            'id': str(datetime.now().timestamp()).replace('.',''),
            'message': message
        }
    )
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)