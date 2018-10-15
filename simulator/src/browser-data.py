import time
import random
import web
# import thread
import threading
import traceback

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
app = web.application(("/(.*)", "echo"), globals())


###################
# Client Simulator
###################


def client_simulator(client_id):
    print("Starting Client %s" % client_id)
    while True:
        time.sleep(random.uniform(0, 2))
        response = app.request(random.choice(routes), method=random.choice(methods))


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
