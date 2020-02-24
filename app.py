from flask import Flask, Request
import pika

app = Flask(__name__)


@app.route('/<parameter>')
def hello_world(parameter=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=parameter)
    channel.basic_publish(exchange='',
                          routing_key=parameter,
                          body=f'Hello World from {parameter}!')

    method_frame, header_frame, body = channel.basic_get(parameter)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        channel.queue_delete(queue=parameter)
        connection.close()
        return body
    else:
        channel.queue_delete(queue=parameter)
        connection.close()
        return 'No message returned'


if __name__ == '__main__':
    app.run()
