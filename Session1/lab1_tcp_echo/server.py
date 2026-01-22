import socket
import logging

HOST = "127.0.0.1"
PORT = 9000
LOG_FILE = "tcp_server.log"

def get_logger():
    logger = logging.getLogger("tcp_echo")
    logger.setLevel(logging.INFO)

    # Tránh add handler nhiều lần nếu chạy lại
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(fmt)

        sh = logging.StreamHandler()
        sh.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger

def main():
    logger = get_logger()
    logger.info("Starting TCP Echo Server")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)

        print(f"[SERVER] Listening on {HOST}:{PORT}")
        logger.info(f"Listening on {HOST}:{PORT}")

        try:
            conn, addr = s.accept()
            print(f"[SERVER] Connected by {addr}")
            logger.info(f"Client connected: {addr}")

            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("[SERVER] Client disconnected")
                        logger.info("Client disconnected")
                        break

                    msg = data.decode(errors="ignore")
                    print(f"[SERVER] Received: {msg}")
                    logger.info(f"Received: {msg}")

                    conn.sendall(data)

        except KeyboardInterrupt:
            print("\n[SERVER] Stopped by user (Ctrl+C)")
            logger.info("Stopped by user (Ctrl+C)")

        finally:
            # ép flush log ra file
            for h in logger.handlers:
                try:
                    h.flush()
                except Exception:
                    pass

if __name__ == "__main__":
    main()
