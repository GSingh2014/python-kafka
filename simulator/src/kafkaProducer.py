from kafka import KafkaProducer


class MyKafkaProducer(object):
    def __init__(self, kafka_brokers, topic):
        self.topic = topic
        self.producer = KafkaProducer(
            value_serializer=lambda v: str(v).encode('utf-8'),
            bootstrap_servers=kafka_brokers
        )

    def send_raw_data(self, topic, data):
        self.producer.send(topic, data)
        self.producer.flush()
