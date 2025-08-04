# Create an Application instance with Kafka configs
from quixstreams import Application


app = Application(
    broker_address='localhost:31234',
    consumer_group='example'
)

# Define a topic "my_topic" with JSON serialization
topic = app.topic(name='my_topic', value_serializer='json')

#event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

# Create a Producer instance
with app.get_producer() as producer:

    while True:

        event = {"id": "1", "text": "This message is produced every second"}

        # Serialize an event using the defined Topic 
        message = topic.serialize(key=event["id"], value=event)

        # Produce a message into the Kafka topic
        producer.produce(
            topic=topic.name, value=message.value, key=message.key
        )

        import time
        time.sleep(1)  # Sleep for 1 second before producing the next message