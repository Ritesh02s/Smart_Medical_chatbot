from apscheduler.schedulers.background import BackgroundScheduler

import feedparser

from modules.knowledge_updater import add_document_to_db


def fetch_medical_updates():

    url = (
        "https://pubmed.ncbi.nlm.nih.gov/rss/search/"
        "?term=diabetes+treatment&format=rss"
    )

    feed = feedparser.parse(url)

    added = 0

    for entry in feed.entries[:5]:

        text = (
            entry.title
            + "\n"
            + getattr(entry, "summary", "")
        )

        chunks = add_document_to_db(text)

        added += chunks

    print(
        f"Added {added} chunks from PubMed updates."
    )


scheduler = BackgroundScheduler()

scheduler.add_job(
    fetch_medical_updates,
    trigger="interval",
    hours=24
)


def start_scheduler():

    if not scheduler.running:

        scheduler.start()

        print("Knowledge update scheduler started.")

    else:

        print("Scheduler already running.")

