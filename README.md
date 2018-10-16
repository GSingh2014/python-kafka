# python-kafka
Repo for python and kafka 

# Setup Kafka
docker run -d --net=confluent --name=zookeeper -e ZOOKEEPER_CLIENT_PORT=2182 -p 2182:2182 confluentinc/cp-zookeeper:5.0.0

docker run -d --net=confluent --name=kafka -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2182 -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:29092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -p 29092:29092 confluentinc/cp-kafka:5.0.0

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic browser-topic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --create --topic vehicle-topic --partitions 1 --replication-factor 1 --if-not-exists --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --list --zookeeper zookeeper:2182

docker run --net=confluent --rm confluentinc/cp-kafka:5.0.0 kafka-topics --describe --topic browser-topic --zookeeper zookeeper:2182
