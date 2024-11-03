import pika
import json

class EventConsumer:
    def __init__(self) -> None:
        self.connection = None
        self.channel = None

    def initalize_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            "localhost", credentials=pika.PlainCredentials("guest", "guest")))
        channel = connection.channel()
        channel.queue_declare(queue='EmailService')


        channel.basic_consume(queue='EmailService', auto_ack=True, on_message_callback=self.callback)
        channel.start_consuming()
    
    def callback(self, ch, method, properties, body):
            return body






'''
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "localhost", credentials=pika.PlainCredentials("guest", "guest")
    )
)
channel = connection.channel()

channel.exchange_declare(exchange="hello-world", exchange_type="fanout")

channel.queue_declare(queue="hello-consumer-1")

channel.queue_bind(exchange="hello-world", queue="hello-consumer-1")


def callback(ch, method, properties, body):
    print(f" [x] Received from consumer 1 {body}")


channel.basic_consume(
    queue="hello-consumer-1", auto_ack=True, on_message_callback=callback
)

channel.start_consuming()
'''