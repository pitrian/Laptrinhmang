import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9001

def recv_loop(sock):
    while True:
        try:
            data, _ = sock.recvfrom(2048)
            print("\n[RECV]", data.decode(errors="ignore"))
            print("> ", end="", flush=True)
        except OSError:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # bind để nhận tin nhắn (OS tự chọn port)
        s.bind(("0.0.0.0", 0))
        print(f"[UDP CLIENT] Your addr: {s.getsockname()}")

        t = threading.Thread(target=recv_loop, args=(s,), daemon=True)
        t.start()

        print("Type message, 'exit' to quit.")
        while True:
            msg = input("> ")
            if msg.lower() == "exit":
                break
            s.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))

if __name__ == "__main__":
    main()
