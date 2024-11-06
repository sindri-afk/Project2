import pika
import time


'''Hægt að gera instance af hvaða queue consumerinn á að consuma frá'''
class EventConsumer:
    def __init__(self, queue_name) -> None:
        self.queue_name = queue_name
        self.last_message = None

    #Competing consumer
    def initalize_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials("guest", "guest")))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_qos(prefetch_count=1)


        def callback(a_channel, method, properties, body):
            time.sleep(body.count(b'.'))
            self.last_message = {
                'body': body,
                'properties': properties,
                'method': method
            }
            a_channel.basic_ack(delivery_tag=method.delivery_tag)
        
        channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        channel.start_consuming()
    
    def get_message(self):
        return self.last_message