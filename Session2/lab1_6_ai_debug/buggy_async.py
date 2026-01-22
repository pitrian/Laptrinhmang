import asyncio

async def handle_client(reader, writer):
    # BUG: thiếu await
    data = reader.read(1024)

    # BUG: writer không drain, không close
    writer.write(b"Hello client\n")

async def main():
    server = await asyncio.start_server(
        handle_client, "0.0.0.0", 9002
    )
    print("Buggy async server running on port 9002")
    async with server:
        await server.serve_forever()

asyncio.run(main())
