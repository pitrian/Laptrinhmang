import socket
import threading
import logging

HOST = "127.0.0.1"
PORT = 9002
LOG_FILE = "tcp_server.log"

def setup_logger():
    logger = logging.getLogger("tcp_mt")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(fmt)

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger

logger = setup_logger()

def handle_client(conn: socket.socket, addr):
    logger.info(f"Client connected: {addr}")
    print(f"[SERVER] New client: {addr}", flush=True)

    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    logger.info(f"Client disconnected: {addr}")
                    print(f"[SERVER] Client disconnected: {addr}", flush=True)
                    break

                msg = data.decode(errors="ignore")
                logger.info(f"From {addr}: {msg}")
                print(f"[SERVER] From {addr}: {msg}", flush=True)

                conn.sendall(b"[echo] " + data)

            except ConnectionResetError:
                logger.warning(f"Client reset: {addr}")
                print(f"[SERVER] Client reset: {addr}", flush=True)
                break
            except OSError as e:
                logger.error(f"Socket error {addr}: {e}")
                print(f"[SERVER] Socket error {addr}: {e}", flush=True)
                break

def main():
    logger.info("Starting multi-threaded TCP server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        print(f"[SERVER] Listening on {HOST}:{PORT}", flush=True)
        logger.info(f"Listening on {HOST}:{PORT}")

        while True:
            try:
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
            except KeyboardInterrupt:
                print("\n[SERVER] Stopped by user (Ctrl+C)", flush=True)
                logger.info("Stopped by user (Ctrl+C)")
                break

if __name__ == "__main__":
    main()
