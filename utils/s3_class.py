import sys
import os
from io import BytesIO, BufferedReader
import boto3

from PIL import Image
import numpy as np
sys.path.append('.')
from utils.aws_secrets import *

class S3Functions:

    def __init__(self, bucket_name) -> None:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        self.bucket_name = bucket_name
        self.s3 = session.client('s3')

    def read_image(self, key):
        s3_object = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=key
            )['Body'].read()
        b = BytesIO(s3_object)
        img = Image.open(b)
        return np.array(img)

    def read_object(self, key):
        s3_object = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=key
            )['Body']
        
        return s3_object
    
    def upload_object(self, obj_path, key):
        self.s3.upload_file(
            obj_path,
            self.bucket_name,
            key
        )

    def read_audio(self, key):
        s3_object = self.s3.get_object(
            Bucket=self.bucket_name,
            Key=key
        )['Body'].read()
        b = BufferedReader(BytesIO(s3_object))
        return b

    def list_bucket_objects(self, prefix:str=None):
        if prefix:
            contents = self.s3.list_objects(
                Bucket=self.bucket_name,
                Prefix=prefix
                )['Contents']
        else:
            contents = self.s3.list_objects(Bucket=self.bucket_name)['Contents']

        return [obj['Key'] for obj in contents]