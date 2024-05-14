import json
import requests
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import urlparse
from urllib.parse import urljoin

# OpenAI setting
import os
from dotenv import load_dotenv
from openai import OpenAI
import time


load_dotenv()

map_key = ""

# base_url = "https://www.nps.gov"

client = OpenAI(api_key=os.getenv("API_KEY"))

formated_content = "no content"
formated_description = "no description"  
map_url = "no map"
image_url = "no image"


def get_base_url (url):
    
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def open_AI_description(park_name, park_url):
    
    time.sleep(1)
    inputdata = "Tell me about this " + park_name +  "with 4 or 5 detailed and interesting sentences for visitors" + "based on the" + park_url

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": inputdata},
    ],
    stream=True
    )

    collected_messages = []

    for chunk in response:
        # chunk_time = time.time() - start_time             # calculate the time delay of the chunk
        chunk_message = chunk.choices[0].delta.content    # extract the message
        collected_messages.append(chunk_message)          # save the message
        # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
    
    collected_messages = [m for m in collected_messages if m is not None]
    full_reply_description = ''.join(collected_messages)

    
    return full_reply_description


def open_AI_content(park_name, park_url):
    
    time.sleep(1)
    inputdata = "Tell me about this " + park_name + "with representitive simple one sentence" + "based on" + park_url
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": inputdata},
    ],
    stream=True
    )

    collected_messages = []

    for chunk in response:
        # chunk_time = time.time() - start_time             # calculate the time delay of the chunk
        chunk_message = chunk.choices[0].delta.content    # extract the message
        collected_messages.append(chunk_message)          # save the message
        # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
    
    collected_messages = [m for m in collected_messages if m is not None]
    full_reply_content = ''.join(collected_messages)

    return full_reply_content


def scrape_park_data(park_name,park_url):   
    
    
    
    formated_content = open_AI_content(park_name, park_url)
    
    formated_description = open_AI_description(park_name, park_url)
    
    
    # / ------------- Image URL ------------- /
    base_url = get_base_url(park_url)
    r = requests.get(park_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    slide_content = soup.find("div", class_= "slide__content")
    image_url = "no image"
    if slide_content:
        img_tag = slide_content.find("img")
        
        # If the img tag is found, print its source (src) attribute
        if img_tag:
            img_src = img_tag.get("data-src")
            image_url = urljoin(base_url,img_src)
            # print(f"Image source: {image_url}")
        else:
            image_url = "no image"
                
    # map_info = "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"
    
    map_info = scrape_map_info(park_name)
    
    if formated_content and formated_description and image_url and map_info:
            
        return {
            "content": formated_content,
            "description": formated_description,
            "image": image_url,
            "map": map_info
        }

def scrape_map_info(parkname):
    
    # Replace 'YOUR_API_KEY' with your actual API key
    

    # Replace 'Birmingham Civil Rights National Monument' with the desired location
    location = 'Birmingham Civil Rights National Monument'

    # Construct the URL for the Google Maps Embed API request
    map_url = f'https://www.google.com/maps/embed/v1/place?key={map_key}&q={urllib.parse.quote(parkname)}'
    if map_url:
        return map_url
    

# Load input JSON
with open('test_state_input.json', 'r',encoding='utf-8') as file:
    input_data = json.load(file)

output_data = {}

# Loop through states and parks
for state, parks in input_data.items():
    output_data[state] = {"parks": []}  
    index = 0
    
    for park_name, park_url in parks.items():
        
        print (index)
        
        if park_url and park_name:
            index += 1
            
            if index >= 1 :
                # Scrape park data
                scraped_data = scrape_park_data(park_name,park_url)

                # Add scraped data to output
                output_data[state]["parks"].append({
                 "name": park_name,
                  "url": park_url,
                 **scraped_data
                })
                # Write output JSON
                with open('data_state_parks_0.json', 'w') as json_file:
                    json.dump(output_data, json_file, indent=4)
                