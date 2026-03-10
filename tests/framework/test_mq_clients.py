import json
from unittest.mock import MagicMock, patch

import pytest

from taflex.core.config.app_config import AppConfig
from taflex.mq.kafka_client import KafkaClient
from taflex.mq.rabbitmq_client import RabbitMQClient

@pytest.fixture
def mq_config():
    return AppConfig(
        mq_host="testhost",
        mq_port=1234,
        mq_username="user",
        mq_password="password",
        mq_protocol="rabbitmq"
    )

class TestRabbitMQClient:
    def test_init(self, mq_config):
        client = RabbitMQClient(mq_config)
        assert client.config == mq_config
        assert client.connection is None
        assert client.channel is None

    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    @patch('pika.PlainCredentials')
    def test_connect(self, mock_creds, mock_params, mock_conn, mq_config):
        client = RabbitMQClient(mq_config)
        mock_conn_instance = MagicMock()
        mock_conn.return_value = mock_conn_instance
        
        client.connect()
        
        mock_creds.assert_called_once_with("user", "password")
        mock_params.assert_called_once_with(
            host="testhost",
            port=1234,
            credentials=mock_creds.return_value
        )
        mock_conn.assert_called_once_with(mock_params.return_value)
        assert client.connection == mock_conn_instance
        assert client.channel == mock_conn_instance.channel()

    def test_disconnect(self, mq_config):
        client = RabbitMQClient(mq_config)
        mock_conn = MagicMock()
        mock_conn.is_open = True
        client.connection = mock_conn
        
        client.disconnect()
        mock_conn.close.assert_called_once()

    @patch('pika.BasicProperties')
    def test_publish(self, mock_props, mq_config):
        client = RabbitMQClient(mq_config)
        client.channel = MagicMock()
        
        payload = {"data": "test"}
        client.publish("my_queue", payload, headers={"h1": "v1"})
        
        mock_props.assert_called_once_with(headers={"h1": "v1"})
        client.channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='my_queue',
            body=json.dumps(payload),
            properties=mock_props.return_value
        )

    def test_wait_for_message_success(self, mq_config):
        client = RabbitMQClient(mq_config)
        client.channel = MagicMock()
        
        mock_method_frame = MagicMock()
        mock_method_frame.delivery_tag = 1
        mock_body = json.dumps({"target": "found"}).encode('utf-8')
        
        # basic_get returns (method_frame, header_frame, body)
        client.channel.basic_get.return_value = (mock_method_frame, None, mock_body)
        
        msg = client.wait_for_message(
            "my_queue", 
            timeout=1, 
            condition=lambda m: m.get("target") == "found"
        )
        
        assert msg == {"target": "found"}
        client.channel.basic_ack.assert_called_once_with(1)

    def test_wait_for_message_timeout(self, mq_config):
        client = RabbitMQClient(mq_config)
        client.channel = MagicMock()
        client.channel.basic_get.return_value = (None, None, None)
        
        with pytest.raises(TimeoutError, match="Message matching condition not found"):
            client.wait_for_message("my_queue", timeout=1, condition=lambda m: True)

    def test_purge_queue(self, mq_config):
        client = RabbitMQClient(mq_config)
        client.channel = MagicMock()
        client.purge_queue("my_queue")
        client.channel.queue_purge.assert_called_once_with(queue="my_queue")


class TestKafkaClient:
    def test_init(self, mq_config):
        mq_config.mq_protocol = "kafka"
        client = KafkaClient(mq_config)
        assert client.config == mq_config
        assert client.producer is None
        assert client.consumer is None

    @patch('taflex.mq.kafka_client.Consumer')
    @patch('taflex.mq.kafka_client.Producer')
    def test_connect(self, mock_producer, mock_consumer, mq_config):
        mq_config.mq_protocol = "kafka"
        client = KafkaClient(mq_config)
        
        client.connect()
        
        mock_producer.assert_called_once()
        mock_consumer.assert_called_once()
        assert client.producer == mock_producer.return_value
        assert client.consumer == mock_consumer.return_value

    def test_disconnect(self, mq_config):
        client = KafkaClient(mq_config)
        client.producer = MagicMock()
        client.consumer = MagicMock()
        
        client.disconnect()
        
        client.producer.flush.assert_called_once()
        client.consumer.close.assert_called_once()

    def test_publish(self, mq_config):
        client = KafkaClient(mq_config)
        client.producer = MagicMock()
        
        payload = {"data": "test"}
        client.publish("my_topic", payload, headers={"h1": "v1"})
        
        client.producer.produce.assert_called_once_with(
            topic="my_topic",
            value=json.dumps(payload).encode('utf-8'),
            headers=[("h1", b"v1")]
        )
        client.producer.poll.assert_called_once_with(0)

    def test_wait_for_message_success(self, mq_config):
        client = KafkaClient(mq_config)
        client.consumer = MagicMock()
        
        mock_msg = MagicMock()
        mock_msg.error.return_value = None
        mock_msg.value.return_value = json.dumps({"target": "found"}).encode('utf-8')
        
        client.consumer.poll.return_value = mock_msg
        
        msg = client.wait_for_message(
            "my_topic", 
            timeout=1, 
            condition=lambda m: m.get("target") == "found"
        )
        
        assert msg == {"target": "found"}
        client.consumer.commit.assert_called_once_with(asynchronous=False)
        client.consumer.unsubscribe.assert_called_once()

    def test_wait_for_message_timeout(self, mq_config):
        client = KafkaClient(mq_config)
        client.consumer = MagicMock()
        client.consumer.poll.return_value = None
        
        with pytest.raises(TimeoutError, match="Message matching condition not found"):
            client.wait_for_message("my_topic", timeout=1, condition=lambda m: True)
