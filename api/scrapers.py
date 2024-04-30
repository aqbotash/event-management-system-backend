import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import pytz

def scrape_website():
    base_url = 'https://sxodim.com/astana/afisha?page={}'
    events = []
    page_number = 1

    while True:
        url = base_url.format(page_number)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            link_to_details = soup.select('.layout-impression .impression-main .page .page-content .impressions .impression-items .impression-card > a')
            for link in link_to_details:
                sub_url = link['href']
                sub_response = requests.get(sub_url)
                if sub_response.status_code == 200:
                    sub_soup = BeautifulSoup(sub_response.content, 'html.parser')
                    # img done
                    image = sub_soup.select_one('.layout-impression .impression-main .container .full_news_top .post-article-images .post-article-images-single img')
                    prepared_img = urljoin(url, image['src'])
                    # date done  / need to be formatted !!!
                    dates = sub_soup.select('.layout-impression .impression-main .container .full_news_wrapper .right_side .post-info .premier_info .event_date_block')
                    prepared_dates = []
                    for date in dates:
                        date_obj = datetime.strptime(date['data-date'], '%d.%m.%Y %H:%M:%S')
                        formatted_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        date_obj = datetime.strptime(formatted_date_str, '%Y-%m-%d %H:%M:%S')
                        utc5_timezone = pytz.timezone('Etc/GMT+5')
                        date_obj_aware = utc5_timezone.localize(date_obj)
                        prepared_dates.append(date_obj_aware)
                    
                    # address done 
                    address = sub_soup.select_one('.layout-impression .impression-main .container .full_news_wrapper .right_side .post-info .premier_info .event_date_block .more_info .group .svg-icon--location + .text').text.strip()
                    # title done
                    title = sub_soup.select_one('.layout-impression .impression-main .container .full_news_top .info_wrapper .info .title').text.strip()
                    # category done
                    category = sub_soup.select_one('.layout-impression .impression-main .container .full_news_top .info_wrapper .info .category_wrapper .category').text.strip()
                    # price done / check if exists
                    price = sub_soup.select_one('.layout-impression .impression-main .container .full_news_wrapper .right_side .post-info .premier_info .event_date_block .more_info .group .svg-icon--tenge + .text')
                    if price:
                        price = price.text.strip()
                    # contact info done
                    contact_info = sub_soup.select_one('.layout-impression .impression-main .container .full_news_wrapper .right_side .post-info .premier_info .event_date_block .more_info .group .svg-icon--phone + .text')
                    if contact_info:
                        contact_info = contact_info.text.strip()
                        contact_info = contact_info.replace('Показать', '')
                    # description done / desc with newlines
                    description_element = sub_soup.select_one('.layout-impression .impression-main .container .full_news_wrapper .left_side .content_wrapper')
                    description = description_element.find_all(['p', 'ul'])

                    desc_with_newlines = ''
                    for element in description:
                        if element.name == 'ul':
                            lis = element.find_all('li')
                            for li in lis:
                                desc_with_newlines += li.text.strip() + '\n'
                        else:
                            desc_with_newlines += element.text.strip() + '\n'
                    event = {
                        'name': title,
                        'image': prepared_img,
                        'address': address,
                        'category': category,
                        'dates': prepared_dates,
                        'price': price,
                        'contact': contact_info,
                        'description': desc_with_newlines
                    }
                    events.append(event)
            next_page_link = soup.select_one('.next')
            if next_page_link:
                page_number += 1
            else:
                break
        else:
            print(f'Failed to fetch website content for page {page_number}. Status code: {response.status_code}')
            break
    return events
