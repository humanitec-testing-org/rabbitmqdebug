from flask import Flask, Request
import pika
import os

app = Flask(__name__)
rabbit_host = os.getenv("Rabbit_Host")
rabbit_port = os.getenv("Rabbit_Port")


@app.route('/')
def main():
    return f"RABBIT HOST --> {rabbit_host}\nRABBIT PORT --> {rabbit_port}"


@app.route('/<parameter>')
def hello_world(parameter=None):
    try:
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
    except Exception as e:
        return f"Possibly no RabbitMQ connection \nException : {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
