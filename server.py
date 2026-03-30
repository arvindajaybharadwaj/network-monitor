import socket
import classifier
import security
import config
import time

SERVER_IP = '0.0.0.0'
SERVER_PORT = config.SERVER_PORT
BUFFER_SIZE = 1024

events_log = []
node_status = {}
event_count = 0
total_events = 0
start_time = time.time()

def parse_message(msg):
    """
    Expected format:
    node_id|event_type|value|timestamp|signature
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

def display_dashboard(node_status):
    print("\n===== NETWORK DASHBOARD =====")

    print(f"Active Nodes: {len(node_status)}\n")

    print("Node   | Event        | Value | Class")
    print("--------------------------------------")

    for node, (event, value, cls) in node_status.items():
        print(f"{node:6} | {event:12} | {value:5} | {cls}")

    print("=============================\n")

def main():
    global event_count, total_events

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

            receive_time = time.time()

            print(f"\nPacket received from {addr}")

            node_id, event_type, value, timestamp, signature = parse_message(msg)
            message = f"{node_id}|{event_type}|{value}|{timestamp}"

            event_time = int(timestamp)
            latency = receive_time - event_time

            # check security
            if not security.verify_signature(message, signature):
                print("Invalid Signature! Packet dropped.")
                continue
            # end security

            total_events += 1

            elapsed_time = time.time() - start_time
            throughput = total_events / elapsed_time if elapsed_time > 0 else 0

            classification = classifier.classify_event(event_type, value)

            value_int = int(value)
            events_log.append((node_id, event_type, value_int))

            if len(events_log) > 50:
                events_log.pop(0)

            node_status[node_id] = (event_type, value_int, classification)
            
            aggregate_events(events_log)

            print(f"{node_id} -> {event_type} ({value}) -> {classification} | Latency: {latency:.4f}s | Throughput: {throughput:.2f}/s")

            event_count += 1
            if event_count % 5 == 0:
                display_dashboard(node_status)

        except ValueError as e:
            print("Error: ", e)
        except Exception as e:
            print("Unexpected Error: ", e)

if __name__ == "__main__":
    main()