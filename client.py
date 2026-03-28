import socket
import time
import events
import security
import config

SERVER_IP = config.SERVER_IP
SERVER_PORT = config.SERVER_PORT


def main(node_id):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Client {node_id} started")

    while True:

        node_id, event_type, value, timestamp = events.generate_event(node_id)

        message = f"{node_id}|{event_type}|{value}|{timestamp}"

        signature = security.generate_signature(message)

        packet = message + "|" + signature

        sock.sendto(packet.encode(), (SERVER_IP, SERVER_PORT))

        print("Sent:", packet)

        time.sleep(5)


if __name__ == "__main__":

    node_id = input("Enter node id: ")

    main(node_id)