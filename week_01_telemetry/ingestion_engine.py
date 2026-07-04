import asyncio
import json
import time
from bleak import BleakScanner

TARGET_UUID = "1b365d4a-777a-2b2b-2b2b-1b365d4a777a"
OUTPUT_FILE = "telemetry_raw.jsonl"

# Global references so the synchronous BLE callback can talk to our async queue
event_loop = None
packet_queue = None

def handle_ble_packet(device, advertising_data):
    """
    1. THE PRODUCER: Listens for BLE advertisements.
    If it matches our target UUID, it instantly drops it into the memory queue.
    """
    if TARGET_UUID in advertising_data.service_uuids:
        payload = {
            "timestamp": time.time_ns() // 1_000_000,
            "node_id": "receiver_node_01",
            "rssi": advertising_data.rssi
        }
        
        # Safely push the packet into the async queue without waiting for disk I/O
        if event_loop and packet_queue:
            event_loop.call_soon_threadsafe(packet_queue.put_nowait, payload)

async def flush_worker(queue: asyncio.Queue, filename: str):
    """
    2. THE CONSUMER: Runs in the background. 
    Every 1000 milliseconds (1 second), it wakes up, grabs all packets from 
    the queue, and writes them to the disk in ONE single action.
    """
    while True:
        await asyncio.sleep(1.0) # Wait 1 second
        
        batch = []
        # Gather all packets currently waiting in memory
        while not queue.empty():
            try:
                batch.append(queue.get_nowait())
            except asyncio.QueueEmpty:
                break
        
        # If we found packets, write them all at once
        if batch:
            lines = "".join(json.dumps(packet) + "\n" for packet in batch)
            
            # Offload the disk write to a background thread so the engine never freezes
            def write_to_disk():
                with open(filename, "a") as f:
                    f.write(lines)
            
            await asyncio.to_thread(write_to_disk)

async def main():
    global event_loop, packet_queue
    event_loop = asyncio.get_running_loop()
    packet_queue = asyncio.Queue()
    
    # Start the background writer (Consumer)
    worker_task = asyncio.create_task(flush_worker(packet_queue, OUTPUT_FILE))
    
    # Start the BLE Scanner (Producer)
    print("[INFO] Initializing BleakScanner...")
    scanner = BleakScanner(detection_callback=handle_ble_packet)
    await scanner.start()
    print(f"[SUCCESS] Pipeline operational. Saving data to {OUTPUT_FILE}...")
    
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("[INFO] Shutting down ingestion engine...")
    finally:
        await scanner.stop()
        worker_task.cancel()
        await asyncio.gather(worker_task, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Engine terminated by user.")