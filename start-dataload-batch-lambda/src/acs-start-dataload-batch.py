from __future__ import print_function  
import json
from datetime import datetime
import requests
import boto3
import uuid
import time


s3 = boto3.client('s3')
sfn = boto3.client('stepfunctions')
ssm= boto3.client('ssm')

def lambda_handler(event,context):
    print("acs-start-dataload-batch invoked for Event: ", event)
    EXECUTION_ID=event['EXECUTION_ID']
    dataloadBatch=event['dataloadBatch']
    print("dataloadBatch:", dataloadBatch)
    print("EXECUTION_ID:", EXECUTION_ID)

    configKeyBase='config/dataload-batch-configs/'
    origJsonKey=configKeyBase+dataloadBatch+EXECUTION_ID+'.json'
    obj=s3.get_object(Bucket=configKeyBase,Key=origJsonKey)
    request_payload=json.loads(obj['Body'].read().decode('utf-8'))['DataloadBatch']
    response = requests.post('path/to/api',json=request_payload,verify=False)
    result=response.headers['result']
    if result =="success":
        sfn.send_task_failure(error='Exception encountered in dataloadBatch')
    return "success"
