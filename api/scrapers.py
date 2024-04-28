import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def scrape_website():
    base_url = 'https://sxodim.com/astana/afisha?page={}'
    events = []
    page_number = 1
    all_titles = []
    all_images = []
    all_descriptions = []
    while True:
        url = base_url.format(page_number)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_elements = soup.select('.layout-impression .impression-main .page .page-content .impressions .impression-items .impression-card .impression-card-image img')
            
            image_urls = []
            for image_element in image_elements:
                image_url = urljoin(url, image_element['src'])
                image_urls.append(image_url)
                
            all_images.extend(image_urls)
            titles = soup.select('.layout-impression .impression-main .page .page-content .impressions .impression-items .impression-card .impression-card-title')
            all_titles.extend(titles)

            descriptions = soup.select('.layout-impression .impression-main .page .page-content .impressions .impression-items .impression-card .impression-card-info')
            all_descriptions.extend(descriptions)
            next_page_link = soup.select_one('.next')
            if next_page_link:
                page_number += 1
            else:
                break
        else:
            print(f'Failed to fetch website content for page {page_number}. Status code: {response.status_code}')
            break
    for title, image, description in zip(all_titles, all_images, all_descriptions):
        event = {
            'name': title.text.strip(),
            'image': image,
            'description': description.text.strip()
        }
        events.append(event)
    return events
