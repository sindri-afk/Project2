from event_consumer import EventConsumer
from mail_sender import MailSender
import threading


def main():
    order_consumer = EventConsumer('order_queue')
    payment_consumer = EventConsumer('payment_queue')
    mail_sender = MailSender()

    order_thread = threading.Thread(target=order_consumer.initalize_connection())
    payment_thread = threading.Thread(target=payment_consumer.initalize_connection())
    order_thread.start()
    payment_thread.start()


    while True:
        try:
            if order_consumer.get_message():
                message = order_consumer.get_message()
                mail_sender.send_email()
            if payment_consumer.get_message():
                message = payment_consumer.get_message()
                mail_sender.send_email()
        except KeyboardInterrupt:
            pass
