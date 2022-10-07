import io
import json
import logging
from datetime import datetime
from fdk import response
from onug_decorator import onug

## to be moved 
LOGGER = logging.getLogger()
LOGGER.setLevel(level=logging.WARNING)
LOGGER.info("Inside Event Logging Function")

def get_function_config(ctx):
    config = dict(ctx.Config())
    # Getting LOG_LEVEL from function config
    try:
        log_level = getattr(logging,config["LOG_LEVEL"].upper(),None)
        if isinstance(log_level, int):
            LOGGER.setLevel(level=log_level)
        else:
            LOGGER.warning("Invalid LOG_LEVEL in function configuration.")    
    except KeyError:
        LOGGER.warning("LOG_LEVEL not defined in function configuration.")

    # Getting LOG_LEVEL from function config
    global provider_json
    try:
        provider_json = config["PROVIDER_JSON_URL"]
        LOGGER.debug("get_function_config: Provider JSON URL is set to: " + config["PROVIDER_JSON_URL"])

    except KeyError:
        LOGGER.warning("Provider JSON URL is not defined in function configuration.")
        # provider_json = 'https://objectstorage.us-ashburn-1.oraclecloud.com/n/orasenatdpltsecitom01/b/HammerPublic/o/oci_output.json'
        provider_json = 'https://raw.githubusercontent.com/onug/CSNF/main/tools/provider-csv-to-provider-json-script/output_file.json'


    # Getting LOGGING_OCID from function config
    global LOGGING_OCID
    try:
        LOGGER.info("get_function_config: Logging OCID set to: " + config["LOGGING_OCID"])
        LOGGING_OCID = config["LOGGING_OCID"]
    except:
        LOGGER.info("get_function_config: No LOGGING OCID Provided")
        LOGGING_OCID = None

def handler(ctx, data: io.BytesIO = None):

    global LOGGER
    LOGGER = logging.getLogger()
    #LOGGER.setLevel(level=logging.DEBUG)
    LOGGER.info("Inside Event Logging Function")

    # Getting function configuration
    get_function_config(ctx)
    
    # Getting Event Message
    try:
        message = json.loads(data.getvalue())
        LOGGER.debug("Handler: message is: " + str(message))
    except (Exception) as ex:
        raise Exception("Event type not properly formatted." + str(ex))
    

    try:
        my_onug = onug(provider_json, message)
        payload = my_onug.get_finding()
        logging.debug("Handler: My onug object is: " + str(payload))

        LOGGER.info("Handler: returning mapped ONUG finding")
        return response.Response(
            ctx, response_data=json.dumps(payload), 
            headers={"Content-Type": "application/json"})
    except (Exception) as ex:
        raise Exception("Handler: Event type not properly formatted." + str(ex))
