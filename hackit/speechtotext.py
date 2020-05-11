import boto3,csv,os,subprocess,shutil,json,pandas as pd
from django.conf import settings
import statistics

inputx = open(os.path.join(settings.MEDIA_ROOT, 'credentials.csv'), 'r')
next(inputx)
reader = csv.reader(inputx)
for line in reader:
    access_key_id = line[2]
    secret_access_key = line[3]
        
transcribe = boto3.client('transcribe',region_name='us-east-2',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      verify=False)

s3 = boto3.client('s3',region_name='us-east-2',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      verify=False)

comprehend = boto3.client('comprehend',region_name='us-east-2',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      verify=False)

def upload_file_to_s3(path,file,bucket_name):
    path = os.path.join(path,file)
    return s3.upload_file(path,bucket_name,file)

def perform(uploaded_file):
    jname = uploaded_file.name[:-4]
    try:
        temp_key = jname + str('.json')
        obj = s3.get_object(Bucket='outputhackathontest', Key=temp_key)
        data = json.loads(obj['Body'].read())
        text = str(data['results']['transcripts'][0]['transcript'])
        datasetx = []
        for each in data['results']['items']:
            datasetx.append(float(each['alternatives'][0]['confidence']))
        meanVal = statistics.mean(datasetx)
        return dict({'text': text, 'mean': meanVal})
    except:
        pass
    while(1):
        to_delete = transcribe.list_transcription_jobs(
            Status='COMPLETED'
        )
        dele = [val['TranscriptionJobName'] for val in to_delete['TranscriptionJobSummaries']]
        if(len(dele)==0):
            break
        else:
            for val in dele:
                transcribe.delete_transcription_job(
                    TranscriptionJobName=val)

    temp_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
    s3.upload_file(temp_path,"hackathonbuckettest",uploaded_file.name)

    response = transcribe.start_transcription_job(
        TranscriptionJobName= jname,
        LanguageCode= 'en-US',
        MediaFormat= 'wav',
        Media={
            'MediaFileUri': 'https://hackathonbuckettest.s3.us-east-2.amazonaws.com/' + str(uploaded_file.name)
        },
        OutputBucketName= "outputhackathontest")

    waiting_var = 1
    while waiting_var :
        Jobs = transcribe.list_transcription_jobs(
            Status='IN_PROGRESS'
        )
        if(len(Jobs['TranscriptionJobSummaries']) == 0):
            waiting_var = 0

    responsex = transcribe.get_transcription_job(
        TranscriptionJobName =jname
    )

    temp_key = jname + str('.json')
    obj = s3.get_object(Bucket='outputhackathontest', Key=temp_key)
    data = json.loads(obj['Body'].read())
    text = str(data['results']['transcripts'][0]['transcript'])
    datasetx = []
    for each in data['results']['items']:
        datasetx.append(float(each['alternatives'][0]['confidence']))
    meanVal = statistics.mean(datasetx)
    return dict({'text': text, 'mean': meanVal})