import pika
from config.base import settings
from loguru import logger

cred = pika.PlainCredentials(
    username=settings.SASMAKA_BROKER_USER,
    password=settings.SASMAKA_BROKER_PASS
)
params = pika.ConnectionParameters(
    host=settings.SASMAKA_BROKER_HOST,
    port=settings.SASMAKA_BROKER_PORT,
    virtual_host=settings.SASMAKA_BROKER_VHOST,
    credentials=cred
)

connection = pika.BlockingConnection(parameters=params)
channel = connection.channel()

channel.exchange_declare(
    'queue-delay',
    exchange_type='x-delayed-message',
    arguments={'x-delayed-type': 'topic'}  # u can use direct or topic
)
channel.queue_declare(
    queue="testing-queue-delay"
)
channel.queue_bind(
    exchange='queue-delay',
    queue='testing-queue-delay',
    routing_key='testing.queue.delay'
)


def callback(ch, method, properties, body):
    data = body.decode('utf-8')
    logger.info(data)


channel.basic_consume(
    queue='testing-queue-delay',
    on_message_callback=callback,
    auto_ack=True
)

try:
    logger.info("Start Consuming ...")
    channel.start_consuming()
except KeyboardInterrupt:
    logger.info("Stop Consuming ...")
    channel.stop_consuming()
finally:
    logger.info("Closed Connection")
    channel.close()
    connection.close()
