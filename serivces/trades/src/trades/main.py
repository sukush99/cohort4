# Create an Application instance with Kafka configs
from quixstreams import Application
from kraken_api import KrakenAPI, Trade
from loguru import logger

def run(
        broker_address: str,
        kafka_topic_name: str,
        kraken_api: KrakenAPI
):
    app = Application(
        broker_address=broker_address,
    )

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    #event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

    # Create a Producer instance
    with app.get_producer() as producer:

        while True:

            events : list[Trade] = kraken_api.get_trades()

            for event in events:
                # Serialize an event using the defined Topic
                message = topic.serialize(#key=event["id"], 
                                          value=event.to_dict())

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name, value=message.value#, key=message.key
                )

                #beautiful logger
                logger.success(f'Successfully produced message to the topic "{topic.name}" ')

if __name__ == "__main__":

    from config import config
    api = KrakenAPI(product_ids=['BTC/EUR'])

    run(
        broker_address=config.broker_address,
        kafka_topic_name=config.kafka_topic_name,
        kraken_api=api
    )