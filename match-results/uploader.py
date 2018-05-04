import os
import boto3

DEBUG = os.getenv('DEBUG')

kwargs = {}
if DEBUG:
    kwargs['profile_name'] = 'irdn'
session = boto3.Session(**kwargs)
client = session.client('s3')


def upload_file(s3_bucket, key, html):
    kwargs = dict(
        Body=html,
        Bucket=s3_bucket,
        Key=key,
        ContentType='text/html; charset=utf-8',
    )
    if DEBUG:
        with open('/home/sindri/vikes-result/%s.html' % (key, ), 'w') as f:
            f.write(kwargs['Body'])
            return
    client.put_object(**kwargs)
