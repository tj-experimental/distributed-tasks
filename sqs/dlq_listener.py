import logging
from sqs.sqs_consumer import SQSConsumerClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class DLQConsumer(SQSConsumerClient):
    start_msg = 'Starting dead letter queue worker listening on {queue_url}'
    QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/141793718810/my-data-ingestor-dead-letter-queue-dev'

    def _handle_message(self, message):
        str_message_body = message.get('Body')
        log.info(f"Message Body: {str_message_body}")
        self._delete_message(message=message)


if __name__ == '__main__':
    dlq_consumer = DLQConsumer()
    dlq_consumer.connect()
