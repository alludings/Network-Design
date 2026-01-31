import socket
import argparse
import logging
import random

BUFFER_SIZE = 1024

def main():
    parser = argparse.ArgumentParser(description="Phase 1a UDP Echo Receiver")
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
    sock.bind(("", args.port))

    logging.info(f"Echo receiver listening on port {args.port}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        message = data.decode()
        logging.info(f"Received '{message}' from {addr}")

        sock.sendto(data, addr)
        logging.debug("Echoed message back")

if __name__ == "__main__":
    main()
