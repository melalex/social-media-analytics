import feedparser
import schedule
import time

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from src.definitions import (
    DATETIME_FORMATS,
    ES_HOST,
    ES_PASSWORD,
    ES_USERNAME,
    INDEX_NAME,
    EXTERNAL_DATA_FOLDER,
    FETCH_PERIOD_HOURS,
    RSS_FEEDS,
)


def fetch_rss_feeds(feeds: list[str]):
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            published = entry.get("published", "Unknown")
            all_entries.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": published,
                    "source": url,
                    "publication_datetime": parse_datetime(published, DATETIME_FORMATS),
                }
            )

    actions = [{"_index": INDEX_NAME, "_source": doc} for doc in all_entries]

    es = Elasticsearch(
        [ES_HOST], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False
    )

    bulk(es, actions)


def parse_datetime(datetime_str, formats):
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    return None


def fetch_rss_feeds_default():
    fetch_rss_feeds(RSS_FEEDS)


schedule.every(FETCH_PERIOD_HOURS).hours.do(fetch_rss_feeds_default)

if __name__ == "__main__":
    fetch_rss_feeds_default()
    while True:
        schedule.run_pending()
        time.sleep(60)
