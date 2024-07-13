import paho.mqtt.client as mqtt
from django.conf import settings
import json

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe('uprint/kiosk')  # Subscribe to all subtopics
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
    payload = msg.payload.decode()
    try:
        data = json.loads(payload)
        device_id = data['device_id']
        response_topic = f'uprint/kiosk/{device_id}'
        response_message = json.dumps({'response': 'Message received', 'device_id': device_id})
        mqtt_client.publish(response_topic, response_message)
        print(f"Sent return response '{response_message}' to `{response_topic}`")
    except (json.JSONDecodeError, KeyError):
        print("Invalid message format")

def publish_message(mqtt_client, topic, payload):
    result = mqtt_client.publish(topic, payload)
    status = result.rc
    if status == 0:
        print(f"Sent `{payload}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

# Create an MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

# Connect to the MQTT server
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)

# Function to start the loop in a separate thread
def start_mqtt_client():
    client.loop_start()

# Start the MQTT client
start_mqtt_client()

# Continuously take user input and publish it
try:
    while True:
        message = input("Enter a message to publish (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        publish_message(client, 'uprint/kiosk', message)
except KeyboardInterrupt:
    print("\nExited by user")

# Stop the loop and disconnect the client
client.loop_stop()
client.disconnect()
