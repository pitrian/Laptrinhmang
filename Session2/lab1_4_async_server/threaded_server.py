import socket
import threading

HOST = "0.0.0.0"
PORT = 9000

def handle_client(conn: socket.socket, addr):
    try:
        _ = conn.recv(1024)
        conn.sendall(b"Hello from threaded server\n")
    except Exception as e:
        print("Client error:", addr, e)
    finally:
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(2000)

    print(f"[Threaded] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

if __name__ == "__main__":
    main()
