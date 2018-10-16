import time
import random
import web
import threading
import traceback
from kafkaProducer import MyKafkaProducer
import logging
import os

# Generate a set of vehicle health
healths = [{"vehicle_id": i,
            "vehicle_speed": ".".join(map(str, (random.randint(0, 255) for _ in range(2)))),
            "engine_speed": random.randint(0, 2500),
            "tire_pressure": random.randint(30, 35)} for i in range(10)]
methods = ["GET"]

# Set of rest routes
routes = ["/vehicle_health"]


def do_work(route, health, method):
    delay = random.uniform(0, 2)
    time.sleep(delay)
    print("%s '/%s' from '%s' took '%s ms'" % (method, route, health, delay * 1000))
    # print(json.dumps(health))
    return "%s:%s:%s:%s" % (method, route, health, delay)


class echo:
    def __init__(self):
        self.logger = logging.getLogger()
        self.app = web.application(("/(.*)", "echo"), globals())
        if 'KAFKA_BROKERS' in os.environ:
            kafka_brokers = os.environ['KAFKA_BROKERS'].split(',')
        else:
            raise ValueError('KAFKA_BROKERS environment variable not set')

        if 'TOPIC' in os.environ:
            topic = os.environ['TOPIC'].split(',')
        else:
            raise ValueError('TOPIC environment variable not set')

        self.logger.info("Initializing Kafka Producer")
        self.logger.info("KAFKA_BROKERS={0}".format(kafka_brokers))
        self.myKafka = MyKafkaProducer(kafka_brokers=kafka_brokers, topic=topic)

    def GET(self, route):
        health = random.choice(healths)
        return do_work(route, health, "GET")

    # Setup the REST server
    def run(self):
        # starttime = time.time()
        while True:
            data = self.app.request(random.choice(routes), method=random.choice(methods))
            self.logger.info("Successfully polled browser data")
            # print(data['data'].decode("utf-8"))
            self.myKafka.send_raw_data("".join(self.myKafka.topic),
                                       data=data['data'].decode("utf-8") + ":" + data['status'])
            # time.sleep(10.0 - ((time.time() - starttime) % 300.0))


###################
# Client Simulator
###################


def client_simulator(client_id):
    print("Starting Client %s" % client_id)
    main = echo()
    while True:
        time.sleep(random.uniform(0, 2))
        main.run()


threads = []
try:
    for cid in range(10):
        t = threading.Thread(target=client_simulator, args=(cid,))
        threads.append(t)
        t.start()
except Exception as e:
    print("Error: unable to start thread" + str(e))
    print(traceback.format_exc())

for t in threads:
    t.join()
