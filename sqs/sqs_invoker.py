import json
import logging

import boto3

from sqs.config import ACCESS_KEY, QUEUE_URL, SECRET_KEY


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class SQSInvokerClient(object):
    def __init__(self):
        self.sqs = (
            boto3.client(
                'sqs',
                region_name='us-east-1',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
            )
        )

    def _send_msg(self, **kwargs):
        response = self.sqs.send_message(QueueUrl=QUEUE_URL, **kwargs)
        log.debug(response)
        log.info("Sent message.")
        return response

    def send_report_result(self):
        payload = json.dumps({
            'jobId': 'test01',
            'data': {'topping': [
                {'id':  '5001', 'type': 'Cherry'},
                {'id':  '5002', 'type': 'Glazed'},
                {'id':  '5003', 'type': 'Sugar'},
                {'id':  '5004', 'type': 'Powdered Sugar.'},
                {'id':  '5005', 'type': 'Chocolate with Sprinkles.'},
                {'id':  '5006', 'type': 'Chocolate'},
                {'id':  '5007', 'type': 'Maple'},
            ]}
        })

        return self._send_msg(MessageBody=payload)




if __name__ == '__main__':
    sqs_client = SQSInvokerClient()
    sqs_client.send_report_result()
