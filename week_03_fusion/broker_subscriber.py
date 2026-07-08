import json
import time
from paho.mqtt import client as mqtt_client

# MQTT Network Settings
MQTT_BROKER = "localhost"  # Change to your central broker IP if needed
MQTT_PORT = 1883
TOPIC_FUSION = "rtls/telemetry/+"  # Listens to all nodes: e.g., rtls/telemetry/node_01

class NetworkTelemetrySubscriber:
    def __init__(self):
        self.client_id = "ruview_core_hub"
        self.live_topology_buffer = {}

    def connect_mqtt(self):
        """Establishes connection to the central MQTT network broker."""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("[Network Success] Successfully connected to central MQTT Broker!")
                client.subscribe(TOPIC_FUSION)
                print(f"[Network Info] Subscribed to multi-node wildcard topic: {TOPIC_FUSION}")
            else:
                print(f"[Network Error] Connection failed with return code {rc}")

        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, MQTT_PORT)
        return client

    def start_listening(self):
        """Starts the background listening loop for multi-node arrays."""
        client = self.connect_mqtt()
        
        def on_message(client, userdata, msg):
            try:
                # Extract which node sent the message from the topic path
                node_id = msg.topic.split('/')[-1]
                payload = json.loads(msg.payload.decode())
                
                # Update the active topology buffer with the freshest signal reading
                self.live_topology_buffer[node_id] = float(payload.get("rssi", -99.0))
                
                print(f"[Incoming Telemetry] {node_id} reported RSSI: {self.live_topology_buffer[node_id]} dBm")
            except Exception as e:
                print(f"[Network Parsing Error] Failed to decode incoming frame: {e}")

        client.on_message = on_message
        print("[System Active] Hub listening for satellite nodes... Press Ctrl+C to stop.")
        client.loop_forever()

if __name__ == "__main__":
    # Test execution block to verify local connectivity
    subscriber = NetworkTelemetrySubscriber()
    try:
        subscriber.start_listening()
    except KeyboardInterrupt:
        print("\n[System Standby] Background listener terminated cleanly.")