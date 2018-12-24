import json
import logging
import time

import boto3

from sqs.config import ACCESS_KEY, QUEUE_URL, SECRET_KEY


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class SQSConsumerClient(object):
    def __init__(self):
        self.sqs = (
            boto3.client(
                'sqs',
                region_name='us-east-1',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
            )
        )

    def _delete_message(self, message):
        log.debug(f"Receive Message: {message}")
        log.debug(
            f"Deleting sqs message: {message.get('ReceiptHandle')}",
        )
        return (
            self.sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message.get('ReceiptHandle'),
            )
        )

    def _connect(self):
        log.debug(f"Starting sqs worker listening on {QUEUE_URL}")

        while True:
            response = self.sqs.receive_message(
                QueueUrl=QUEUE_URL,
                AttributeNames=['All'],
                MessageAttributeNames=['string'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            )

            messages = response.get('Messages', [])

            for message in messages:
                try:
                    str_message_body = message.get('Body')
                    log.info(f"Message Body: {str_message_body}")
                    body = json.loads(str_message_body)
                    if not body.get('jobId'):
                        log.warning("No Job ID provided.")
                        self._delete_message(message=message)
                    else:
                        job_id = body['jobId']
                        log.info(f"Running Job ID: {job_id}")
                        self._delete_message(message=message)
                except Exception as e :
                    log.exception(f"An Error occurred {e}")
                    self._delete_message(message=message)

            time.sleep(10)
            log.info("WORKER STOPPED.")



if __name__ == '__main__':
    sqs_client = SQSConsumerClient()
    sqs_client._connect()
