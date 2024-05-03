import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from ratelimit import limits, sleep_and_retry

# OpenAI setting
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))

base_url = "https://www.nps.gov"
retry_attempts = 3
retry_delay = 5

# Define the rate limit: 3 requests per minute
@sleep_and_retry
@limits(calls=3, period=60)
def open_AI_description(url):
    input_data = "Tell me about this " + url

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_data}],
        stream=True
    )

    collected_messages = []

    for chunk in response:
        chunk_message = chunk.choices[0].delta.content
        collected_messages.append(chunk_message)

    collected_messages = [m for m in collected_messages if m is not None]
    full_reply_content = ''.join(collected_messages)

    return full_reply_content

def scrape_park_data(url):
    formated_content = []
    formated_description = []
    imgurl = None
    map_info = None

    try:
        for attempt in range(retry_attempts):
            r = requests.get(url)
            if r.status_code == 200:
                break
            time.sleep(retry_delay)

        soup = BeautifulSoup(r.text, 'html.parser')
        meta_tags = soup.find_all('meta')

        for tag in meta_tags:
            content_meta = tag.get('content')
            if tag.get('property') == 'og:description':
                content = content_meta
                formated_content = content.replace("\u2019", "'").replace("\u2026", "")

        formated_description = open_AI_description(url)
        img = soup.find(attrs={"class": "absolute h-full inset-0 object-cover w-full"})
        if img:
            imgurl = img['src']
        map_info = "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"

    except (requests.RequestException, ValueError, AttributeError) as e:
        print(f"An error occurred while scraping {url}: {e}")
        return {
            "content": formated_content,
            "description": formated_description,
            "image": imgurl,
            "map": map_info
        }

    return {
        "content": formated_content,
        "description": formated_description,
        "image": imgurl,
        "map": map_info
    }

# Load input JSON
with open('national_parks.json', 'r', encoding='utf-8') as file:
    input_data = json.load(file)

output_data = {}
index = 0
# Loop through states and parks
for state, parks in input_data.items():
    output_data[state] = {"parks": []}

    
    for park_name, park_url in parks.items():
        print(index)
        index += 1
        if park_url:
            scraped_data = scrape_park_data(park_url)
            output_data[state]["parks"].append({
                "name": park_name,
                "url": park_url,
                **scraped_data
            })

        # Introduce a delay of 20 seconds between consecutive API requests
        time.sleep(20)

    # Save intermediate results to a JSON file
    with open('data_national_parks_intermediate.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

# Final results are already stored in the `output_data` variable

# Write final output JSON
with open('data_national_parks.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)