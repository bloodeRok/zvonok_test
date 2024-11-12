import pika
import json
import uuid

from pika.delivery_mode import DeliveryMode

from no_1.constants import SERVICE_A_B_QUEUE, RABBIT_MQ_HOST, RABBIT_MQ_PORT


class ServiceA:
    def __init__(self):
        self.queue_name = SERVICE_A_B_QUEUE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def send_data(self, data: dict[str, int | str]) -> None:
        """
        Проверяет и отправляет данные в очередь RabbitMQ.

        :param data: Словарь с данными для отправки.
        """

        # Как-то валидируем данные, производим какие-то операции, если нужно
        self.__add_request_to_queue(data=data)

    def __add_request_to_queue(self, data: dict[str, int|str]) -> None:
        """
        Непосредственно отправляет сообщение в очередь.

        :param data: Словарь с данными для отправки.
        """
        task_id = str(uuid.uuid4())
        message = {"task_id": task_id, "data": data}

        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=DeliveryMode.Persistent,
            )
        )
