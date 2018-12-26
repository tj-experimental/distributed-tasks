import boto3


class BaseSQSConfig(object):
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/141793718810/my-data-ingestor-dev'
    ACCESS_KEY = ''
    SECRET_KEY = ''
    DEFAULT_REGION = 'us-east-1'

    def __init__(self):
        self.sqs = (
            boto3.client(
                'sqs', region_name=self.DEFAULT_REGION,
                aws_access_key_id=self.ACCESS_KEY,
                aws_secret_access_key=self.SECRET_KEY,
            )
        )
