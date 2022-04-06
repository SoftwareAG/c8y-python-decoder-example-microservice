import requests
import logging
import json
import API.authentication as auth


logger = logging.getLogger('Inventory API')
logger.info('Logger for Inventory was initialised')
Auth = auth.Authentication()


def createDevice(externalID):
    try:
        logger.info('Checking for managed object in c8y with external ID %s' + externalID)
        url = '%s/inventory/managedObjects'%(Auth.tenant)
        payload = json.loads('{"com_cumulocity_model_Agent": {},"c8y_IsDevice": {}}')

        payload['name'] = "nbiot_%s"%(externalID)
        response = requests.request("POST", url, headers=Auth.headers, data = json.dumps(payload))
        logger.debug('Requesting the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or 201:
            logger.info('Device created')
            internal_id = json.loads(response.text)['id']
            if createExternalID(externalID,internal_id,'c8y_Serial'):
                logger.debug('Returning the managed Object')
                return internal_id
            else:
                logger.error('Raising Exception, external ID was not registered properly')
                raise Exception
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            logger.error('Device was not created properly')
            raise Exception
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


def checkExternalId(external_id):
    logger.info('Checking if external ID exists')
    try:
        url = f'{Auth.tenant}/identity/externalIds/c8y_Serial/{external_id}'
        response = requests.request("GET", url, headers=Auth.headers)
        logger.debug('Sending data to the following url: ' + str(url))
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Inventory exists')
            logger.info(json.loads(response.text))
            internal_id = json.loads(response.text)['managedObject']['id']
            return internal_id
        elif response.status_code == 404:
            logger.info('Device does not exist, creating it')
            return createDevice(external_id)
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            raise Exception
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))


def createExternalID(deviceID,internalID,type):
    logger.info('Create an external id for an existing managed object')
    try:
        url = "%s/identity/globalIds/%s/externalIds"%(Auth.tenant, internalID)
        payload = "{\n\t\"externalId\": \"%s\",\n    \"type\": \"%s\"\n}"%(deviceID,type)
        response = requests.request("POST", url, headers=Auth.headers, data = payload)
        logger.debug('Response from request: ' + str(response.text))
        logger.debug('Response from request with code : ' + str(response.status_code))
        if response.status_code == 200 or response.status_code == 201:
            logger.info('Serial nummer entered')
            logger.debug('Receiving the following response %s'%(str(response.text)))
            return True
        else:
            logger.warning('Response from request: ' + str(response.text))
            logger.warning('Got response with status_code: ' + str(response.status_code))
            return False
    except Exception as e:
        logger.error('The following error occured: %s' % (str(e)))

if __name__ == '__main__':
    pass

