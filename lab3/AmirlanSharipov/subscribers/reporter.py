import json
import os
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exchange_type import ExchangeType

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'rep.*'


def extract_value(dict_line):
    return dict_line['value']


def callback(channel, method, properties, body):
    log_file = open('receiver.log', 'r')
    lines = log_file.readlines()
    dict_lines = list(map(json.loads, lines))
    if body == b'current':
        print(f"{datetime.utcnow()}: Latest CO2 level is {dict_lines[-1]['value']}")
    else:
        values = list(map(extract_value, dict_lines))
        avg = sum(values) / len(values)
        print(f"{datetime.utcnow()}: Average CO2 level is {avg}")

    log_file.close()
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = BlockingConnection(
            ConnectionParameters(
                host=RMQ_HOST,
                credentials=PlainCredentials(RMQ_USER, RMQ_PASS)
                )
            )
    try:
        channel = connection.channel()
        result = channel.queue_declare(queue=ROUTING_KEY)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=result.method.queue)

        channel.basic_consume(queue=ROUTING_KEY,
                              on_message_callback=callback)

        print('[*] Waiting for queries from the control tower. Press CTRL+C to exit')

        channel.start_consuming()

        connection.close()
    except KeyboardInterrupt:
        connection.close()
        print('Interrupted by user. Shutting down...')


if __name__ == '__main__':
    main()
