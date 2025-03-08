import pika
import json

from elasticsearch import Elasticsearch

from src.definitions import (
    ES_HOST,
    ES_PASSWORD,
    ES_USERNAME,
    INDEX_NAME,
    QUEUE_NAME,
    RABBITMQ_HOST,
)


def publish_rss_feed():
    es = Elasticsearch(
        [ES_HOST], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False
    )

    response = es.search(
        index=INDEX_NAME,
        body={
            "size": 0,
            "aggs": {
                "articles_per_day": {
                    "date_histogram": {
                        "field": "publication_datetime",
                        "calendar_interval": "day",
                    }
                }
            },
        },
    )

    print("Aggregated data: " + str(response))

    aggregated_data = response["aggregations"]["articles_per_day"]["buckets"]
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    message = json.dumps(aggregated_data, ensure_ascii=False)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )


if __name__ == "__main__":
    publish_rss_feed()
