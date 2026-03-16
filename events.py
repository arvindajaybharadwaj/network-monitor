import random
import time

EVENT_TYPES = ["packet_loss", "latency", "node_down", "cpu_usage"]

def generate_event(node_id):
    event_type = random.choice(EVENT_TYPES)

    if event_type == "packet_loss":
        value = random.randint(0, 20)
    elif event_type == "latency":
        value = random.randint(50, 400)
    elif event_type == "cpu_usage":
        value = random.randint(10, 100)
    elif event_type == "node_down":
        value = random.choice([0, 1])

    timestamp = int(time.time())

    return node_id, event_type, value, timestamp