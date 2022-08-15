import pika
class RabbitMQConnector:
    _instance = None

    def connect_rabbit_mq(self):

        username = 'rabbitmq'
        password = 'rabbitmq'
        host = '211.195.9.228'

        credentials = pika.PlainCredentials(username=username, password=password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, credentials=credentials))
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host="211.195.9.228"))
        # connection = pika.BlockingConnection(pika.URLParameters('amqp://rabbitmq:rabbitmq@211.195.9.228:5672'))
        return connection


    def __init__(self):
        if not RabbitMQConnector._instance:
            self.connection = self.connect_rabbit_mq()


    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = RabbitMQConnector()
        return cls._instance


    def getConnection(self):
        return self.connection


task_queue_name = 'task'
result_queue_name = 'result'

def task_basic_pubilsh(user_no, message):
    connection = RabbitMQConnector().getInstance().getConnection()
    channel = connection.channel()
    queue_name = f"{task_queue_name}{user_no}"
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)