import asyncio

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    try:
        data = await reader.read(1024)
        writer.write(b"Hello client\n")
        await writer.drain()
    except Exception as e:
        print("Error with client", addr, e)
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, "0.0.0.0", 9002
    )
    print("Fixed async server running on port 9002")
    async with server:
        await server.serve_forever()

asyncio.run(main())
