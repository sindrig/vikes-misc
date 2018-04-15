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
        kwargs['Bucket'] = 'vikes-result.irdn.is'
    client.put_object(**kwargs)
