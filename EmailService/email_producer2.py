import pika
import json
import os
from mail_sender import MailSender

class EmailOrderProducer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_queue', payment_queue='payment_queue') -> None:
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_queue = payment_queue
        self.missing_ids = []

        #Rabbitmq
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=payment_queue)
    
    def process_order(self, ch, method, properties, body):
        event = body.decoded()
        try:
            data = json.loads(event)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    
    
    
    
    def process_payment(self, ch, method, properties, body):
        event = body.decoded()
        try:
            data = json.loads(event)
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)


