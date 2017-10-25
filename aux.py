import boto3
from botocore import UNSIGNED
from botocore.client import Config
import os

BUCKET_NAME = 'sentinel-s2-l1c'
DATA_FOLDER = 'DATA'
client = boto3.client('s3', config=Config(signature_version=UNSIGNED))


def download_file(key):
    key_dir, key_filename = os.path.split(key)
    out_dir = os.path.join(DATA_FOLDER, key_dir)
    out_filename = os.path.join(out_dir, key_filename)
    if not os.path.exists(out_filename):
        client.download_file(BUCKET_NAME, key, out_filename)
