import os
import hashlib
import boto3
import botocore

DEBUG = os.getenv('DEBUG')

kwargs = {}
if DEBUG:
    kwargs['profile_name'] = 'irdn'
session = boto3.Session(**kwargs)
client = session.client('s3')


def get_md5sum(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


def upload_file(s3_bucket, key, html, content_type='text/html; charset=utf-8'):
    html = html.encode('utf8')
    md5 = get_md5sum(html)
    head_kwargs = dict(
        Bucket=s3_bucket,
        Key=key,
    )
    kwargs = dict(
        Body=html,
        ContentType=content_type,
        # ContentMD5=md5,
        **head_kwargs
    )
    try:
        client.head_object(IfNoneMatch=md5, **head_kwargs)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '304':
            print('No change in file %s/%s' % (s3_bucket, key, ))
            return
        else:
            raise e
    if DEBUG:
        fn = '/home/sindri/vikes-result/%s' % (key, )
        print('Writing %s/%s to %s' % (s3_bucket, key, fn,))
        with open(fn, 'w') as f:
            f.write(kwargs['Body'].decode('utf8'))
            return
    print('Uploading %s/%s' % (s3_bucket, key, ))
    client.put_object(**kwargs)
