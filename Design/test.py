from google.cloud import pubsub_v1
import json

project_id = "lab1-413419"
topic_id = "smartMeterTopic"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

test_messages = [
    {"time": "2024-02-18T12:34:56Z", "temperature": 20.5, "pressure": 101.3},
    {"time": "2024-02-18T12:35:56Z", "temperature": 21.0, "pressure": 100.8},
]

for message in test_messages:
    message_str = json.dumps(message)
    publisher.publish(topic_path, data=message_str.encode("utf-8"))
    print(f"Published test message to {topic_id}.")
