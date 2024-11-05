import pika
import json
import os
from card_validation import CardValidator, CreditCard



class PaymentProducer:
    def __init__(self, rabbitmq_host='rabbitmq', order_queue='order_created', payment_result_queue='payment_result', json_file='./PaymentService/card_validations.json'):
        self.rabbitmq_host = rabbitmq_host
        self.order_queue = order_queue
        self.payment_result_queue = payment_result_queue
        self.json_file = json_file
        self.order_id = 1
        
        #RabbitMQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue)
        self.channel.queue_declare(queue=self.payment_result_queue)
    
    def load_payments(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []
    
    def save_payments(self, order_id, status):
        payment_results = self.load_payments()
        new_payment = {
            'order_id': order_id,
            'status': status
        }
        payment_results.append(new_payment)
        with open(self.json_file, 'w') as file:
            json.dump(payment_results, file, indent=4)
    
    def validate_card(self, credit_card: CreditCard):
        validator = CardValidator()
        result = validator.validate_card(credit_card)
        return result

    def publish_payment(self, order_id, status):
        result_event = json.dumps({'order_id': order_id, 'status':status})
        self.channel.basic_publish(exchange='', routing_key=self.payment_result_queue, body=result_event)
    
    def process_order_payment(self, ch, method, properties, body):
        event = body.decoded()
        try:
            data = json.loads(event)
            credit_card = data.get('creditCard', {})
            cardNumber = credit_card.get('cardNumber')
            expirationMonth = credit_card.get('expirationMonth')
            expirationYear = credit_card.get('expirationYear')
            cvc = credit_card.get('cvc')

            card_checker = CreditCard(cardNumber, expirationMonth, expirationYear, cvc)
            self.order_id += 1
            if self.validate_card(card_checker) == True:
                self.save_payments(self.order_id, 'success')
                self.publish_payment(self.order_id, 'success')
            else:
                self.save_payments(self.order_id, 'failure')
                self.publish_payment(self.order_id, 'failure')
        except json.JSONDecodeError:
            pass
        except KeyError as e:
            pass
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def start_consuming(self):
        self.channel.basic_consume(queue=self.order_queue, on_message_callback=self.process_order_payment())
        self.channel.start_consuming()

    def close_connection(self):
        if self.connection.is_open():
            self.connection.close()