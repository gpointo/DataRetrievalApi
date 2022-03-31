from __future__ import print_function  
import json
from datetime import datetime
import requests
import boto3
import uuid
import time


s3 = boto3.client('s3')
ssm= boto3.client('ssm')
sfn=boto3.client('stepfunction')

def lambd_handler(event,context):
    print("acs-schedule-state-machine invoked for Event: ", event)
    EXECUTION_ID = str(uuid.uuid4())
    accountId=ssm.get_parameter(Name='/gloabl/AccountId').get('Parameter').get('Value')
    region='us-east-1'
    dataloadBatch=event['dataloadBatch']
    configKeyBase='config/dataload-batch-configs/'
    origJsonKey=configKeyBase+dataloadBatch+EXECUTION_ID+'.json'
    obj=s3.get_object(Bucket=configKeyBase,Key=origJsonKey)
    scheduleParameters=json.loads(obj['Body'].read().decode('utf-8'))['Schedule']
    stateMachineName=scheduleParameters.get('stateMachineName')
    stateMachineArn='arn::aws::states:'+region+':'+accountId+':stateMachine:'+stateMachineName
    stateMachinePayload=scheduleParameters.get(stateMachinePayload,{})
    scheduleType=scheduleParameters.get('scheduleType')
    if scheduleType == 'BD':
        startDate=get_calender_days()
    startTime=scheduleParameters.get('dtartTime')
    utcOffset="-4:00"
    startTimeStamp=startDate+"T"+startTime+utcOffset
    stateMachinePayload.update({'startTimeStamp':startTimeStamp})
    stateMachinePayload.update({'EXECUTION_ID':EXECUTION_ID})
    response=sfn.start_execution(
        stateMachineArn=stateMachineArn,
        input=json.dumps(stateMachinePayload)
    )
    return

   
def get_calender_days():
    currDoW=time.strftime('%A')
    currYear=time.strftime('%Y')
    currMon=time.strftime('%m')
    currDay=time.strftime('%d')
    if currDoW == 'Saturday':
        currDay=currDay+2
    elif currDoW == 'Sunday':
        currDay=currDay+1
    startDate=currYear+"-"+currMon+"-"+currDay
    return startDate

    