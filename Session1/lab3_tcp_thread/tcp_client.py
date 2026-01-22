import socket

HOST = "127.0.0.1"
PORT = 9002

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("[CLIENT] Connected. Type message, 'exit' to quit.")

        while True:
            msg = input("> ")
            if msg.lower() == "exit":
                break

            s.sendall(msg.encode())
            data = s.recv(1024)
            print(data.decode(errors="ignore"))

if __name__ == "__main__":
    main()
