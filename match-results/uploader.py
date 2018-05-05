import os
import boto3

DEBUG = os.getenv('DEBUG')

kwargs = {}
if DEBUG:
    kwargs['profile_name'] = 'irdn'
session = boto3.Session(**kwargs)
client = session.client('s3')


def upload_file(s3_bucket, key, html, content_type='text/html; charset=utf-8'):
    kwargs = dict(
        Body=html,
        Bucket=s3_bucket,
        Key=key,
        ContentType=content_type,
    )
    if DEBUG:
        with open('/home/sindri/vikes-result/%s' % (key, ), 'w') as f:
            f.write(kwargs['Body'])
            return
    client.put_object(**kwargs)
