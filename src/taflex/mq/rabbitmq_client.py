import json
import time
from typing import Callable

import pika

from taflex.core.config.app_config import AppConfig
from taflex.mq.base_client import BaseMQClient


class RabbitMQClient(BaseMQClient):
    def __init__(self, config: AppConfig):
        self.config = config
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.config.mq_username, self.config.mq_password)
        parameters = pika.ConnectionParameters(
            host=self.config.mq_host,
            port=self.config.mq_port,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def publish(self, destination: str, payload: dict, headers: dict | None = None):
        properties = pika.BasicProperties(headers=headers) if headers else None
        self.channel.basic_publish(
            exchange='',
            routing_key=destination,
            body=json.dumps(payload),
            properties=properties
        )

    def wait_for_message(self, destination: str, timeout: int, condition: Callable) -> dict:
        end_time = time.time() + timeout
        
        # Ensure queue exists
        self.channel.queue_declare(queue=destination, durable=True)
        
        while time.time() < end_time:
            method_frame, header_frame, body = self.channel.basic_get(queue=destination)
            if method_frame:
                msg = json.loads(body.decode('utf-8'))
                if condition(msg):
                    self.channel.basic_ack(method_frame.delivery_tag)
                    return msg
                else:
                    # Not the message we want, reject and requeue
                    self.channel.basic_nack(method_frame.delivery_tag, requeue=True)
            time.sleep(0.5)  # Short polling interval
            
        raise TimeoutError(f"Message matching condition not found in {destination} within {timeout}s")

    def purge_queue(self, destination: str):
        self.channel.queue_purge(queue=destination)
