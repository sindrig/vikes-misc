import argparse
import time
import datetime
import pprint

import boto3
import botocore

# We assume that we've already run make upload
REGION = 'us-east-1'
CLOUDFORMATION_STACK_S3 = (
    'https://s3.amazonaws.com/vikes-result-code/match-results.template'
)
CLOUDFORMATION_STACK_NAME = 'vikes-result'
LAMBDA_CODE_S3 = (
    'vikes-result-code', 'code.zip'
)
LAMBDA_FUNCTION_NAME = 'MatchFetcher'

session = boto3.Session(profile_name='irdn')


def update_lambda():
    '''Updates lambda code with code from S3'''
    client = session.client('lambda', region_name=REGION)
    s3_bucket, s3_key = LAMBDA_CODE_S3
    client.update_function_code(
        FunctionName=LAMBDA_FUNCTION_NAME,
        S3Bucket=s3_bucket,
        S3Key=s3_key,
    )
    print('Lambda function %s updated' % (LAMBDA_FUNCTION_NAME, ))


def trigger_lambda():
    client = session.client('lambda', region_name=REGION)
    response = client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
    )
    if response['StatusCode'] == 200:
        print('Lambda function triggered')
    else:
        print('Error triggering lambda')
        pprint.pprint(response)


def update_cloudformation():
    '''Updates cloudformation stack with definition in S3'''
    starttime = datetime.datetime.utcnow()
    client = session.client('cloudformation', region_name=REGION)
    stack_kwargs = dict(
        StackName=CLOUDFORMATION_STACK_NAME,
        TemplateURL=CLOUDFORMATION_STACK_S3,
        Capabilities=['CAPABILITY_IAM'],
    )
    try:
        client.describe_stacks(StackName=CLOUDFORMATION_STACK_NAME)
        client.update_stack(**stack_kwargs)
    except botocore.exceptions.ClientError as e:
        if e.args[0].endswith('does not exist'):
            # todo create stack
            client.create_stack(**stack_kwargs)
        elif e.args[0].endswith('No updates are to be performed.'):
            print('There are no updates to cloudformation stack, bailing out')
            return
        else:
            raise e
    last_status = None
    while True:
        stacks = client.describe_stacks(
            StackName=CLOUDFORMATION_STACK_NAME
        )
        status = stacks['Stacks'][0]['StackStatus']
        if status != last_status:
            print(status)
        last_status = status
        if status.endswith('COMPLETE'):
            if status not in ('CREATE_COMPLETE', 'UPDATE_COMPLETE'):
                print('Something went wrong')
                events = client.describe_stack_events(
                    StackName=CLOUDFORMATION_STACK_NAME
                )
                for event in events['StackEvents']:
                    if event['Timestamp'].replace(tzinfo=None) < starttime:
                        break
                    print(
                        event['ResourceStatus'],
                        event['ResourceType'],
                        event['LogicalResourceId'],
                        event.get('ResourceStatusReason', '')
                    )
            break
        time.sleep(1)


ACTIONS = {
    'lambda': update_lambda,
    'cloudformation': update_cloudformation,
    'trigger': trigger_lambda,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("actions", nargs='+', choices=ACTIONS)
    args = parser.parse_args()
    for action in args.actions:
        ACTIONS[action]()
