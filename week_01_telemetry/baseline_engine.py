import asyncio
from bleak import BleakScanner
import json, time

TARGET_UUID = "1b365d4a-777a-2b2b-2b2b-1b365d4a777a"
OUTPUT_FILE = "telemetry_baseline.jsonl"

def handle_ble_packet(device, advertising_data):
    if TARGET_UUID in advertising_data.service_uuids:
        payload = {
            "timestamp": time.time_ns() // 1_000_000,
            "node_id": "receiver_node_01",
            "rssi": advertising_data.rssi
        }

        with open(OUTPUT_FILE, "a") as f:
            f.write(json.dumps(payload) + "\n")

async def main():
    scanner = BleakScanner(detection_callback=handle_ble_packet)
    await scanner.start()
    while True: 
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass