import json
import logging
import time

from sqs.config import BaseSQSConfig

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class SQSConsumerClient(BaseSQSConfig):
    start_msg = 'Starting sqs worker listening on {queue_url}'

    def _delete_message(self, message):
        log.info(f"Receive Message: {message}")
        log.info(
            f"Deleting sqs message: {message.get('ReceiptHandle')}",
        )
        return (
            self.sqs.delete_message(
                QueueUrl=self.QUEUE_URL,
                ReceiptHandle=message.get('ReceiptHandle'),
            )
        )

    def _handle_message(self, message):
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
        except Exception as e:
            log.exception(f"An Error occurred {e}")
            # self._delete_message(message=message)

    def connect(self):
        log.info(self.start_msg.format(queue_url=self.QUEUE_URL))

        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.QUEUE_URL,
                AttributeNames=['All'],
                MessageAttributeNames=['string'],
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10,
            )

            messages = response.get('Messages', [])

            for message in messages:
                self._handle_message(message)

            time.sleep(10)
            log.info("WORKER STOPPED.")


if __name__ == '__main__':
    sqs_client = SQSConsumerClient()
    sqs_client.connect()
