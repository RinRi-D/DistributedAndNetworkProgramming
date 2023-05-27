import json
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exchange_type import ExchangeType

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'co2.sensor'


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

        while True:
            co2 = int(input('Enter CO2 level: '))
            message = json.dumps({'time': str(datetime.utcnow()), 'value': co2})
            print(message)
            channel.basic_publish(exchange=EXCHANGE_NAME,
                                  routing_key=ROUTING_KEY,
                                  body=message)
        connection.close()
    except KeyboardInterrupt:
        connection.close()
        print('Interrupted by user. Shutting down...')


if __name__ == '__main__':
    main()
