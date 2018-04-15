import boto3

client = boto3.client('s3')


def upload_matches(s3_bucket, matches):
    client.put_object(
        Body=str(matches),
        Bucket=s3_bucket,
        Key='index.html',
        ContentType='text/html',
    )
