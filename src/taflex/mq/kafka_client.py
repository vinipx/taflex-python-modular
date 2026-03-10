import json
import time
from typing import Callable, Any

from confluent_kafka import Producer, Consumer, KafkaException

from taflex.core.config.app_config import AppConfig
from taflex.mq.base_client import BaseMQClient


class KafkaClient(BaseMQClient):
    def __init__(self, config: AppConfig):
        self.config = config
        self.producer = None
        self.consumer = None

    def connect(self):
        conf = {
            'bootstrap.servers': f"{self.config.mq_host}:{self.config.mq_port}",
        }
        
        # If credentials provided, assuming SASL_PLAINTEXT for simplicity (can be enhanced)
        if self.config.mq_username and self.config.mq_password:
            conf.update({
                'security.protocol': 'SASL_PLAINTEXT',
                'sasl.mechanisms': 'PLAIN',
                'sasl.username': self.config.mq_username,
                'sasl.password': self.config.mq_password
            })

        self.producer = Producer(conf)
        
        # Consumer needs a group.id, creating a dynamic one for testing
        consumer_conf = conf.copy()
        consumer_conf.update({
            'group.id': f"taflex_test_group_{int(time.time())}",
            'auto.offset.reset': 'earliest'
        })
        self.consumer = Consumer(consumer_conf)

    def disconnect(self):
        if self.producer:
            self.producer.flush()
        if self.consumer:
            self.consumer.close()

    def publish(self, destination: str, payload: dict, headers: dict | None = None):
        # Kafka headers expect a list of tuples or dict with bytes
        kafka_headers = []
        if headers:
            for k, v in headers.items():
                kafka_headers.append((k, str(v).encode('utf-8')))

        self.producer.produce(
            topic=destination,
            value=json.dumps(payload).encode('utf-8'),
            headers=kafka_headers if kafka_headers else None
        )
        self.producer.poll(0)

    def wait_for_message(self, destination: str, timeout: int, condition: Callable[[Any], bool]) -> dict:
        self.consumer.subscribe([destination])
        
        end_time = time.time() + timeout
        
        while time.time() < end_time:
            msg = self.consumer.poll(timeout=0.5)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            
            try:
                msg_val = json.loads(msg.value().decode('utf-8'))
                if condition(msg_val):
                    self.consumer.commit(asynchronous=False)
                    self.consumer.unsubscribe()
                    return msg_val
            except Exception:
                pass  # Skip messages that fail parsing or condition evaluation
                
        self.consumer.unsubscribe()
        raise TimeoutError(f"Message matching condition not found in {destination} within {timeout}s")

    def purge_queue(self, destination: str):
        # Kafka doesn't have a direct "purge queue" like RabbitMQ.
        # Best effort for testing: seek to end.
        pass
