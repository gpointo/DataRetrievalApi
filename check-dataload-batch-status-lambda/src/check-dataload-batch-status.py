from __future__ import print_function  
import json
import requests
import boto3
import os

def lambda_handler(event,context):
    print("check-dataload-batch-status invoced with Event:",event)
    TaskToken=event.get('TaskToken','NA')
    transactionStatusResourcePath=event['startDataloadBatchResult']['transactionStatusResourcePath']
    dataloadServiceBaseUri=os.environ['DataloadServiceBaseUri']
    response=response.json()['requestStatus']['taskStatus']
    print("Response taskStatus: ",taskStatus)
    if taskStatus =='Completed' and TaskToken != 'NA':
        print('sendTaskSuccess')
    elif taskStatus =='Failed' and TaskToken != 'NA':
        print('sendTaskSduccess')
        SNF.send_task_failure(taskToken=TaskToken,error=str(response.status_code))
    except:
        print("Exception Encountered")
        if TaskToken != 'NA'
          print('sendTaskFailure')
          SFN.send_task_failure(taskToken=TaskToken,error='Exception Encountered in check-dataload-batch-status')
        raise
    return{
        'taskStatus': taskStatus
    }