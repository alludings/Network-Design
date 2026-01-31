import socket
import struct
import argparse
import logging
import random
import socket
import struct
import argparse
import logging
import random

DATA_SIZE = 1024

def main():
    parser = argparse.ArgumentParser(description="Phase 1b RDT 1.0 Sender")
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--file", required=True)
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

    seq = 0
    with open(args.file, "rb") as f:
        while True:
            data = f.read(DATA_SIZE)
            if not data:
                break

            packet = struct.pack("!I", seq) + data
            sock.sendto(packet, (args.host, args.port))
            logging.debug(f"Sent packet {seq} ({len(data)} bytes)")
            seq += 1

    logging.info("File transfer complete")
    sock.close()

if __name__ == "__main__":
    main()
