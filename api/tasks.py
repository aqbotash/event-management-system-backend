# tasks.py

from celery import shared_task
from . import scrapers

@shared_task
def scrape_website_task():
    from .models import Event
    # Call your scraping function
    events = scrapers.scrape_website()

    # Save scraped events to the database
    for event_data in events:
        Event.objects.create(
            name=event_data['name'],
            img=event_data['image'],
            description=event_data['description']
        )
