import requests
from flask import Flask, jsonify, request
import logging
from datetime import datetime, date, time, timedelta
from base64 import b64encode
import API.authentication as auth


logger = logging.getLogger('Measurement API')
logger.info('Logger for Measurements was initialised')
Auth = auth.Authentication()

def createMeasurement(payload):
    logger.info('Creating measurements in c8y')
    try:
        url = "%s/measurement/measurements"%(Auth.tenant)
        Auth.headers['Accept'] = 'application/vnd.com.nsn.cumulocity.measurementCollection+json'            
        response = requests.request("POST", url, headers=Auth.headers, data = payload)
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or 201:
            logger.info('Measurment send')
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' +
                           str(response.status_code))
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

if __name__ == '__main__':
    pass

