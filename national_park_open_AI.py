import json
import requests
from bs4 import BeautifulSoup
import urllib.parse

# OpenAI setting
import os
from dotenv import load_dotenv
from openai import OpenAI
import time


load_dotenv()

map_key = ""

base_url = "https://www.nps.gov"

client = OpenAI(api_key=os.getenv("API_KEY"))

formated_content = "There is no content"
formated_description = "There is no description"  
map_url = "There is no map url"
image_url = "There is no image url"


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
   
      
    imgurl = "no image"
    
    r = requests.get(park_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    
    formated_content = open_AI_content(park_name, park_url)
    
    # descriptions = soup.find(attrs={"class": "max-w-736 mx-auto text-body-lg text-rich"})
    # for descript in descriptions.children:
    #     description.append(descript.text)
    #     formated_description = ' '.join(description).replace('\n', '').replace("\u2019", "'").replace("\u201c", "“").replace("\u201d", "”")            
    
    formated_description = open_AI_description(park_name, park_url)
        
    img = soup.find(attrs={"class": "absolute h-full inset-0 object-cover w-full"})
    if img:
        imgurl = img['src']
    
    # / ------------- Map ------------- /          
    # map_urls = soup.find_all( "a", class_ =  "button-secondary" ) 
    # map_url = map_urls[10].get('href')  
    # map_data_url = scrape_map_site (map_url)
    # map_info = scrape_map_info (map_data_url)
    
    # map_info = "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"
    
    map_info = scrape_map_info(park_name)
    
    if formated_content and formated_description and imgurl and map_info:
            
        return {
            "content": formated_content,
            "description": formated_description,
            "image": imgurl,
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
with open('national_parks.json', 'r',encoding='utf-8') as file:
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
                with open('data_national_parks.json', 'w') as json_file:
                    json.dump(output_data, json_file, indent=4)
                