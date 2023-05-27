import json

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exchange_type import ExchangeType

RMQ_HOST = 'localhost'
RMQ_USER = 'rabbit'
RMQ_PASS = '1234'
EXCHANGE_NAME = 'amq.topic'
ROUTING_KEY = 'co2.*'


def callback(channel, method, properties, body):
    log_file = open('receiver.log', 'a')
    log_file.write(body.decode() + '\n')

    message = json.loads(body)
    status = 'OK'
    if message['value'] > 500:
        status = 'WARNING'
    print(f"{message['time']}: {status}")

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

        print('[*] Waiting for CO2 data. Press CTRL+C to exit')

        channel.start_consuming()

        connection.close()
    except KeyboardInterrupt:
        connection.close()
        print('Interrupted by user. Shutting down...')


if __name__ == '__main__':
    main()
