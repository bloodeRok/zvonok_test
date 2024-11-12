import pika
import json

from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from no_1.constants import SERVICE_A_B_QUEUE, RABBIT_MQ_HOST


class ServiceB:
    def __init__(self):
        self.queue_name = SERVICE_A_B_QUEUE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_MQ_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_qos(prefetch_count=1)

    def get_data_from_mq(
            self,
            ch: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes
    ) -> None:
        """
        Получает сообщение из очереди, обрабатывает данные и подтверждает
        получение (удаляя его из очереди).

        :param ch: Канал сообщения.
        :param method: Информация о доставке.
        :param properties: Свойства сообщения.
        :param body: Данные в битовом формате.
        """

        task = json.loads(body)
        task_id = task["task_id"]
        data = task["data"]
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # Производим операции над полученными данными

        print(
            f"Проделал операцию над данными по задаче {task_id}: "
            f"user_id={data['user_id']}, "
            f"user_data={data['user_data']}."
        )

    def run_listening(self) -> None:
        """Запуск "прослушки" брокера."""

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.get_data_from_mq
        )
        self.channel.start_consuming()

    def stop_listening(self):
        """Конец "прослушки" брокера."""

        if self.channel.is_open:
            self.channel.stop_consuming()
