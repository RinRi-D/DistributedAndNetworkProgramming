import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exchange_type import ExchangeType

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY_CURRENT = 'rep.current'
ROUTING_KEY_AVG = 'rep.average'


def main():
    connection = BlockingConnection(
            ConnectionParameters(
                host=RMQ_HOST,
                credentials=PlainCredentials(RMQ_USER, RMQ_PASS)
                )
            )
    try:
        channel = connection.channel()
        result = channel.queue_declare(queue=ROUTING_KEY_CURRENT)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=result.method.queue)
        result = channel.queue_declare(queue=ROUTING_KEY_AVG)
        channel.queue_bind(exchange=EXCHANGE_NAME, queue=result.method.queue)

        while True:
            query = input('Enter Query: ')
            if query == 'current':
                channel.basic_publish(exchange=EXCHANGE_NAME,
                                      routing_key=ROUTING_KEY_CURRENT,
                                      body=query)
            if query == 'average':
                channel.basic_publish(exchange=EXCHANGE_NAME,
                                      routing_key=ROUTING_KEY_AVG,
                                      body=query)

    except KeyboardInterrupt:
        connection.close()
        print('Interrupted by user. Shutting down...')


if __name__ == '__main__':
    main()
