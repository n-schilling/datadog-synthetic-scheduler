import json
import logging
import os
import sys

import boto3
import urllib3

urllib3.disable_warnings()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

http_pool = urllib3.PoolManager()

secretsmanager_client = boto3.client('secretsmanager')


def changeSyntheticStatus(new_status):
    logger.info(f"Start changing Datadog Synthetic status to {new_status}")
    try:
        datadog_secret_name = os.getenv('datadogSecretName', 'Datadog_API_Key')
    except:
        logger.error("One of the environmet variable is missing")
        raise
    try:
        get_secret_value_response = secretsmanager_client.get_secret_value(
            SecretId=datadog_secret_name
        )
        if 'SecretString' in get_secret_value_response:
            secret_value_str = get_secret_value_response['SecretString']
        else:
            logger.error(
                f"Could not extract secret {datadog_secret_name} from Secrets Manager")
            raise
        secret_value = json.loads(secret_value_str)
        dd_api_key = secret_value['datadog']['api_key']
        dd_app_key = secret_value['datadog']['app_key']
    except:
        logger.error(
            "There was an error while getting the parameter from the parameter store")
        raise

    synthetic_public_id = os.getenv('syntheticPublicId')
    datadog_api_endpoint = os.getenv('datadogApiEndpoint')

    datadog_endpoint_url = datadog_api_endpoint + \
        'synthetics/tests/' + synthetic_public_id + '/status'

    logger.info(
        f"Changing status to {new_status} for Datadog Synthetic with ID {synthetic_public_id} against endpoint {datadog_endpoint_url}")

    body_json = json.dumps({
        "new_status": new_status,
    })

    put_response = http_pool.request('PUT', datadog_endpoint_url,
                                     headers={
                                         'Content-Type': 'application/json',
                                         'DD-API-KEY': dd_api_key,
                                         'DD-APPLICATION-KEY': dd_app_key
                                     },
                                     body=body_json)
    if (put_response.status) != 200:
        logger.error(
            f"HTTP Call to change the status of Datadog Synthetic {synthetic_public_id} to {new_status} failed.")
        logger.error(f"HTTP status is {put_response.status}")
        raise
    else:
        decoded_response = json.loads(put_response.data.decode('utf-8'))
        if decoded_response:  # HTTP response is either true or false
            logger.info(
                f"Status of Datadog Synthetic {synthetic_public_id} was successfully changed to {new_status}")
        else:
            logger.error(
                f"HTTP Call was successfull but the status of Datadog Synthetic {synthetic_public_id} was NOT changed to {new_status}. Response was {decoded_response}")
            raise


def handler(event, context):
    logger.info("Start with Datadog Synthetic Scheduler")
    try:
        synthetic_set_status = event['syntheticSetStatus']
    except:
        logger.error("Could not extract Synthetic destination status from event")
        raise
    changeSyntheticStatus(synthetic_set_status)
    logger.info("End of Datadog Synthetic Scheduler")


if __name__ == "__main__":
    handler(0, 0)
