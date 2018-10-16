import time
import random
import web
import threading
import traceback
from kafkaProducer import MyKafkaProducer
import logging
import os

# Generate a set of IPs
ips = [".".join(map(str, (random.randint(0, 255) for _ in range(4)))) for i in range(10)]
methods = ["GET", "GET" "GET", "GET", "PUT", "PUT", "POST", "POST"]

# Set of rest routes
routes = ["/users", "/admin", "/login", "/user", "/health", "/status"]


def do_work(route, ip, method):
    delay = random.uniform(0, 2)
    time.sleep(delay)
    print("%s '/%s' from '%s' took '%s ms'" % (method, route, ip, delay * 1000))
    return "%s:%s:%s:%s" % (method, route, ip, delay)


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
        ip = random.choice(ips)
        return do_work(route, ip, "GET")

    def PUT(self, route):
        ip = random.choice(ips)
        return do_work(route, ip, "PUT")

    def POST(self, route):
        ip = random.choice(ips)
        return do_work(route, ip, "POST")

    # Setup the REST server
    def run(self):
        # starttime = time.time()
        while True:
            data = self.app.request(random.choice(routes), method=random.choice(methods))
            self.logger.info("Successfully polled browser data")
            print(data)
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
