import os
import boto3

from .formatter import get_html

DEBUG = os.getenv('DEBUG')

kwargs = {}
if DEBUG:
    kwargs['profile_name'] = 'irdn'
session = boto3.Session(**kwargs)
client = session.client('s3')


def upload_matches(s3_bucket, matches):
    kwargs = dict(
        Body=get_html(matches),
        Bucket=s3_bucket,
        Key='index.html',
        ContentType='text/html; charset=utf-8',
    )
    if DEBUG:
        with open('/home/sindri/vikes-result.html', 'w') as f:
            f.write(kwargs['Body'])
            return
    client.put_object(**kwargs)
