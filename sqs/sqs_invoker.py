import json
import logging

import boto3

from sqs.config import BaseSQSConfig


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SQSInvokerClient(BaseSQSConfig):

    def _send_msg(self, **kwargs):
        response = self.sqs.send_message(QueueUrl=self.QUEUE_URL, **kwargs)
        log.info(response)
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

        return self._send_msg(MessageBody="This will raise an exception!")




if __name__ == '__main__':
    sqs_client = SQSInvokerClient()
    sqs_client.send_report_result()
