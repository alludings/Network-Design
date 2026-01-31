import socket
import struct
import argparse
import logging
import random

BUFFER_SIZE = 2048
DATA_SIZE = 1024

def main():
    parser = argparse.ArgumentParser(description="Phase 1b RDT 1.0 Receiver")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--out", required=True)
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
    logging.info(f"Receiver listening on port {args.port}")

    received = {}

    while True:
        packet, _ = sock.recvfrom(BUFFER_SIZE)
        seq = struct.unpack("!I", packet[:4])[0]
        data = packet[4:]

        logging.debug(f"Received packet {seq} ({len(data)} bytes)")
        received[seq] = data

        if len(data) < DATA_SIZE:
            break

    with open(args.out, "wb") as f:
        for seq in sorted(received):
            f.write(received[seq])

    logging.info(f"File written to {args.out}")
    sock.close()

if __name__ == "__main__":
    main()