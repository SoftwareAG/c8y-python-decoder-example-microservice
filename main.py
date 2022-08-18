#!flask/bin/python
import logging
logger = logging.getLogger('Logger')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.info("Logger was initialized")

from flask import Flask, jsonify, request
import os
import decoder
import sys
from API.measurement import createMeasurement
import json
from API.inventory import checkExternalId

app = Flask(__name__)


@app.route('/decode', methods=['POST'] )
def decode():
    payload = request.get_json(force=True)
    logger.debug('Incoming Message: ' + str(payload))
    dec_payload = decoder.decode(payload['payload'])
    external_id = dec_payload['id']
    logger.debug(f'Thats the external id found in the hex payload: {external_id}')
    internal_id = checkExternalId(external_id)
    logger.debug(f'Thats the internal id found for the device: {internal_id}')
    logger.debug(dec_payload)
    message = []
    message.append(decoder.create_c8y_payload('temperature', 'temperature', dec_payload['temperature'],internal_id))
    message.append(decoder.create_c8y_payload('rssi', 'rssi', dec_payload['rssi'],internal_id))
    message.append(decoder.create_c8y_payload('humidity', 'humidity', dec_payload['humidity'],internal_id))
    message.append(decoder.create_c8y_payload('resistance', 'resistance', dec_payload['resistance'],internal_id))
    message.append(decoder.create_c8y_payload('battery_voltage', 'battery_voltage', dec_payload['battery_voltage'],internal_id))
    payload = {}
    payload['measurements'] = message
    logger.debug(json.dumps(payload))
    createMeasurement(json.dumps(payload))
    return json.dumps(payload)

# Verify the status of the microservice
@app.route('/health')
def health():
    return '{ "status" : "UP" }'

# Get environment details
@app.route('/environment')
def environment():
    environment_data = {
        'platformUrl': os.getenv('C8Y_BASEURL'),
        'mqttPlatformUrl': os.getenv('C8Y_BASEURL_MQTT'),
        'tenant': os.getenv('C8Y_BOOTSTRAP_TENANT'),
        'user': os.getenv('C8Y_BOOTSTRAP_USER'),
        'password': os.getenv('C8Y_BOOTSTRAP_PASSWORD'),
        'microserviceIsolation': os.getenv('C8Y_MICROSERVICE_ISOLATION')
    }
    return jsonify(environment_data)

if __name__ == '__main__':
    logger.info("Starting")
    app.run(host='0.0.0.0', port=80)