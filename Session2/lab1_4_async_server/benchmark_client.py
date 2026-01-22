import asyncio
import time
import argparse

async def one_request(host: str, port: int, sem: asyncio.Semaphore):
    async with sem:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(b"ping")
        await writer.drain()
        _ = await reader.readline()
        writer.close()
        await writer.wait_closed()

async def run_benchmark(host: str, port: int, total: int, concurrency: int):
    sem = asyncio.Semaphore(concurrency)
    tasks = [one_request(host, port, sem) for _ in range(total)]

    t0 = time.perf_counter()
    await asyncio.gather(*tasks)
    t1 = time.perf_counter()

    elapsed = t1 - t0
    rps = total / elapsed if elapsed > 0 else 0
    print(f"Target: {host}:{port}")
    print(f"Total connections: {total}")
    print(f"Concurrency: {concurrency}")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Throughput: {rps:.2f} conns/sec")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, required=True)
    p.add_argument("--total", type=int, default=10000)
    p.add_argument("--concurrency", type=int, default=1000)
    args = p.parse_args()

    asyncio.run(run_benchmark(args.host, args.port, args.total, args.concurrency))

if __name__ == "__main__":
    main()
