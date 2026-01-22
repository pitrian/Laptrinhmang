import asyncio

HOST = "0.0.0.0"
PORT = 9001

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    try:
        _ = await reader.read(1024)  # đọc dữ liệu client (nếu có)
        writer.write(b"Hello from async server\n")
        await writer.drain()
    except Exception as e:
        print("Client error:", addr, e)
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT, backlog=10000)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"[Async] Listening on {addrs}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
