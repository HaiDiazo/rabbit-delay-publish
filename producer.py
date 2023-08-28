import pika
import json
from datetime import datetime
from config.base import settings
from loguru import logger
from argparse import ArgumentParser


def generate_time():
    dt_now = datetime.now()
    return dt_now.strftime("%Y %m %d %H:%M:%S")


def producer(message: dict, exchange: str, routing_key: str):
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

    channel.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=json.dumps(message).encode('utf-8'),
        properties=pika.BasicProperties(
            headers={"x-delay": 60_000}
        ))
    logger.success("Sent data: {}", message)

    channel.close()
    connection.close()


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--delay", "-d", default="true", required=True)
    arg_obj = args.parse_args()

    if arg_obj.delay == "true":
        data = {
            'status': 'OK',
            'message': 'testing with delay',
            'time': generate_time()
        }
        logger.info("Using delay")
        producer(message=data, exchange='queue-delay', routing_key='testing.queue.delay')
    else:
        data = {
            'status': 'OK',
            'message': 'testing without delay',
            'time': generate_time()
        }
        logger.info("Without delay")
        producer(message=data, exchange='queue', routing_key='testing.queue.another')
