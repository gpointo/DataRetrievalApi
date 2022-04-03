from __future__ import print_function  
import json
from datetime import datetime
import requests
import boto3


s3 = boto3.client('s3')
SFN = boto3.client('stepfunctions')
ssm= boto3.client('ssm')

configKeyBase='config/dataload-batch-configs/'
def dateConvert(date):
    print ('date')
    print (date)
    if date == 1:
        date = "January"
    if date == 2:
        date = "February"
    if date == 3:
        date = "Mar"
    if date == 4:
        date = "April"
    if date == 5:
        date = "May"
    if date == 6:
        date = "June"
    if date == 7:
        date = "July"
    if date == 8:
        date = "August"
    if date == 9:
        date = "September"
    if date == 10:
        date = "October"
    if date == 11:
        date = "Novermber"
    if date == 12:
        date = "December"
    return date


def lambda_handler(event,context):
    #configBucket=ssm.get_parameter(Name='acs/common/s3/PrivateBucket').get("Parameter").get('Value')
    print("Loading command-lambda function:",event)
    filecommandResult="Initializing"
    dataloadBatch=event['dataloadBatch']
    TaskToken=event.get('TaskToken','NA')
    EXECUTION_ID=event.get('waitTime',0)
    waitTime=event.get('waitLimit',0)
    priorWaitTimeResult=event.get('commandlambdaResult',None)
    print("dataloadBatch: ", dataloadBatch)
    print("TaskToken: ", TaskToken)
    print("EXECUTION_ID: ", EXECUTION_ID)
    #configKeyBase='config/acs-dataload-batch-configs/'
    #key=configKeyBase+dataloadBatch+".json"
    try:
     #   obj-s3.get_object(Bucket=configBucket,Key=key)
      #  schedulerName
        currentMonth = datetime.now().month
        currentDay = datetime.now().day
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        print(currentMonth)
        url = 'https://www2.illinois.gov/idol/Laws-Rules/CONMED/Documents/2021%20Rates/December_1/Adams.pdf'
        newurl = url.replace('2021',str(currentYear))
        newurl = newurl.replace('1','7')
        date= dateConvert(currentMonth)
        newurl = newurl.replace('December',date)
        print (date)
        print ('hi')
        print (newurl)

        pdfDownload = 'Adams_Illinois_Mar_7.pdf'
        pdfDownload= pdfDownload.replace('Mar',date)
        pdfDownload= pdfDownload.replace('7',str(currentDay))
        print (pdfDownload)
        response = requests.get(newurl)
        if response.status_code == 200:
            r = requests.get(newurl, stream=True)
            session = boto3.Session()
            s3 = session.resource('s3')
            bucket_name = 'file-drop123'
            key = pdfDownload 
            bucket = s3.Bucket(bucket_name)
            bucket.upload_fileobj(r.raw, key)
            print('Web site exists')
            SFN.send_task_success(taskToken=TaskToken,outputs="{\"FileCommandResult\":\FilesFound\"}")
            filecommandResult="FilesFound"
        else:
            print('Web site does not exist') 
            filecommandResult="FileNotFound"
            SFN.send_task_failure(taskToken=TaskToken, error="waitlimit exceeded")
            totalWaitTime= totalWaitTime+1
    except:
        print("Exception Encountered")
        SFN.send_task_failure(taskToken=TaskToken,error="exception encountered in command-lambda")
        raise
        return{
            'taskStatus':filecommandResult,
            'totalWaitTime': totalWaitTime
        }
