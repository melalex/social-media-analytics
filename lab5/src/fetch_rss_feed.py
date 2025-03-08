import feedparser
import schedule
import time

from pathlib import Path
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from src.definitions import (
    ES_HOST,
    ES_PASSWORD,
    ES_USERNAME,
    INDEX_NAME,
    EXTERNAL_DATA_FOLDER,
    FETCH_PERIOD_HOURS,
    RSS_FEEDS,
)


def fetch_rss_feeds(feeds: list[str], path: Path):
    all_entries = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            all_entries.append(
                {
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.get("published", "Unknown"),
                    "source": url,
                }
            )

    actions = [{"_index": INDEX_NAME, "_source": doc} for doc in all_entries]

    es = Elasticsearch(
        [ES_HOST], basic_auth=(ES_USERNAME, ES_PASSWORD), verify_certs=False
    )

    bulk(es, actions)


def fetch_rss_feeds_default():
    fetch_rss_feeds(RSS_FEEDS, EXTERNAL_DATA_FOLDER / "rss_feed.csv")


schedule.every(FETCH_PERIOD_HOURS).hours.do(fetch_rss_feeds_default)

if __name__ == "__main__":
    fetch_rss_feeds_default()
    while True:
        schedule.run_pending()
        time.sleep(60)
