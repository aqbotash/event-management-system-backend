from celery import shared_task
from . import scrapers
from django.db import transaction
from .models import Event, Date

from django.db.models import Q

@shared_task
def scrape_website_task():
    events_data = scrapers.scrape_website()

    for event_data in events_data:
        with transaction.atomic():
            event, created = Event.objects.get_or_create(
                name=event_data.get('name', ''),
                defaults={
                    'img': event_data.get('image', ''),
                    'address': event_data.get('address', ''),
                    'category': event_data.get('category', ''),
                    'price': event_data.get('price', ''),
                    'contact': event_data.get('contact', ''),
                    'description': event_data.get('description', '')
                }
            )

            if created:
                date_objects = event_data.get('dates', [])
                for date_object in date_objects:
                    date, created_date = Date.objects.get_or_create(date=date_object)
                    event.dates.add(date)
                print(f"New event '{event.name}' with dates has been created.")
            else:
                print(f"Event '{event.name}' already exists.")


@shared_task
def delete_past_events():
    from django.utils import timezone
    today = timezone.now()
    for event in Event.objects.all():
        if event.dates.filter(date__lt=today).exists():
            latest_date = event.dates.latest('date').date
            if latest_date < today:
                event.delete()
                print(f"Deleted event '{event.name}' as its latest date has passed.")