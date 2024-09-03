import paho.mqtt.client as mqtt
import json
import sparkplug_b_pb  # Import the generated Sparkplug B protobuf classes
from google.protobuf.json_format import MessageToJson

# Callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("spBv1.0/production/DDATA/line1/device1")
    else:
        print(f"Connect failed with code {rc}")

# Callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload}")

    # Parse Sparkplug B payload
    try:
        sparkplug_b_data = sparkplug_b_pb.Payload()
        sparkplug_b_data.ParseFromString(msg.payload)

        # Convert protobuf message to JSON for easier handling
        sparkplug_b_json = MessageToJson(sparkplug_b_data)
        sparkplug_b_json = json.loads(sparkplug_b_json)

        print(json.loads(sparkplug_b_json['metrics'][0]['stringValue']))

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main(broker_host, broker_port):
    # Create an MQTT client instance
    client = mqtt.Client()

    # Set up callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(broker_host, broker_port, 60)

    # Start the MQTT loop
    client.loop_forever()

if __name__ == "__main__":
    import os
    broker_host = os.getenv('BROKER_HOST', 'broker.emqx.io')
    broker_port = int(os.getenv('BROKER_PORT', '1883'))

    main(broker_host, broker_port)
