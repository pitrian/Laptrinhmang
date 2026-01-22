import socket

HOST = "0.0.0.0"
PORT = 9001

def main():
    clients = set()  # lưu (ip, port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"[UDP SERVER] Listening on {HOST}:{PORT}")

        while True:
            data, addr = s.recvfrom(2048)
            msg = data.decode(errors="ignore").strip()
            if not msg:
                continue

            # ghi nhận client
            clients.add(addr)
            print(f"[UDP SERVER] {addr}: {msg}")

            out = f"{addr[0]}:{addr[1]} says: {msg}".encode()

            # broadcast cho mọi client khác
            dead = []
            for c in clients:
                if c == addr:
                    continue
                try:
                    s.sendto(out, c)
                except OSError:
                    dead.append(c)

            # dọn client lỗi
            for c in dead:
                clients.discard(c)

if __name__ == "__main__":
    main()
