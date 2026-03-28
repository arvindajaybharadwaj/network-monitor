import socket
import classifier
import security
import config

SERVER_IP = '0.0.0.0'
SERVER_PORT = config.SERVER_PORT
BUFFER_SIZE = 1024

events_log = []

def parse_message(msg):
    """
    Expected format:
    node_id|event_type|value|timestamp|token
    """ 

    parts = msg.split("|")

    if len(parts) != 5:
        raise ValueError("Malformed Packet")
    
    node_id = parts[0]
    event_type = parts[1]
    value = parts[2]
    timestamp = parts[3]
    token = parts[4]

    return node_id, event_type, value, timestamp, token

def aggregate_events(events_log):
    high_latency = 0
    node_failures = 0

    for _, event_type, value in events_log:
        if event_type == "latency" and value > 150:
            high_latency += 1
        if event_type == "node_down" and value == 1:
            node_failures += 1

    if high_latency >= 3:
        print("ALERT: Network-wide congestion detected!")
    if node_failures >= 2:
        print("ALERT: Multiple node failures detected!")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print("===================================")
    print(f"Server running on {SERVER_IP}:{SERVER_PORT}")
    print("Waiting for network events...")
    print("===================================")

    while True:
        try:
            data, addr = server_socket.recvfrom(BUFFER_SIZE)
            msg = data.decode()

            print(f"\nPacket received from {addr}")

            node_id, event_type, value, timestamp, signature = parse_message(msg)
            message = f"{node_id}|{event_type}|{value}|{timestamp}"

            classification = classifier.classify_event(event_type, value)

            # check security
            if not security.verify_signature(message, signature):
                print("Invalid Signature! Packet dropped.")
                continue
            # end security

            if len(events_log) > 50:
                events_log.pop(0)
            aggregate_events(events_log)

            print("--------- NETWORK EVENT ---------")
            print(f"Node       : {node_id}")
            print(f"Event Type : {event_type}")
            print(f"Value      : {value}")
            print(f"Timestamp  : {timestamp}")
            print(f"Class      : {classification}")
            print("---------------------------------")

        except ValueError as e:
            print("Eror: ", e)
        except Exception as e:
            print("Unexpected Error: ", e)

if __name__ == "__main__":
    main()