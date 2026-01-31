import socket
import argparse
import logging
import random

BUFFER_SIZE = 1024

def main():
    parser = argparse.ArgumentParser(description="Phase 1a UDP Echo Sender")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--log-level", default="info",
                        choices=["debug", "info", "warning", "error"])
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper()),
        format="%(levelname)s: %(message)s"
    )

    random.seed(args.seed)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "HELLO"
    sock.sendto(message.encode(), (args.host, args.port))
    logging.info("Sent HELLO")

    data, _ = sock.recvfrom(BUFFER_SIZE)
    logging.info(f"Received echo: {data.decode()}")

    sock.close()

if __name__ == "__main__":
    main()