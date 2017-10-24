from sys import exit
import boto3
from botocore import UNSIGNED
from botocore.client import Config

import os

NATO = 'tiles/29/S/NB/'  #
DATA_FOLDER = 'DATA'  # folder to save the data to
# create if the folder does not exist
if not os.path.exists(DATA_FOLDER):
    os.mkdir(DATA_FOLDER)

# bucket name do sentinel
BUCKET_NAME = 'sentinel-s2-l1c'

client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
result = client.list_objects(Bucket=BUCKET_NAME, Delimiter='/')


def folders(client, bucket, prefix=''):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter='/'):
        for prefix in result.get('CommonPrefixes', []):
            yield prefix.get('Prefix')


def get_files(client, bucket, prefix=''):
    return client.list_objects(Bucket=BUCKET_NAME, Delimiter='/', Prefix=prefix).get('Contents', [])


for year in folders(client, BUCKET_NAME, NATO):
    for month in folders(client, BUCKET_NAME, year):
        for day in folders(client, BUCKET_NAME, month):
            for sequence in folders(client, BUCKET_NAME, day):
                for file_ in get_files(client, BUCKET_NAME, sequence):
                    a, f = os.path.split(file_['Key'])

                    if f == 'tileInfo.json':
                        folder_data = os.path.join(DATA_FOLDER,a)
                        if not os.path.exists(folder_data):
                            os.makedirs(folder_data)
                        client.download_file(BUCKET_NAME,file_['Key'],os.path.join(folder_data, f))




