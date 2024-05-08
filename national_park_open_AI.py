import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# OpenAI setting
import os
from dotenv import load_dotenv
from openai import OpenAI
import time


load_dotenv()
start_time = time.time()
client = OpenAI(api_key=os.getenv('API_KEY')) 

base_url = "https://www.nps.gov"

# def open_AI_description(url):
#     rl = "https://www.nationalparks.org/explore/parks/birmingham-civil-rights-national-monument"

#     inputdata = "Tell me about this " + url

#     response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": inputdata},
#     ],
#     stream=True
#     )

#     collected_messages = []

#     for chunk in response:
#         # chunk_time = time.time() - start_time             # calculate the time delay of the chunk
#         chunk_message = chunk.choices[0].delta.content    # extract the message
#         collected_messages.append(chunk_message)          # save the message
#         # print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
    
#     collected_messages = [m for m in collected_messages if m is not None]
#     full_reply_content = ''.join(collected_messages)

    
#     return full_reply_content


def open_AI_content(url):
    
    inputdata = "Tell me about this " + url + "with representitive simple one sentence"
    
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


def scrape_park_data(url):   
   
    description = []
    formated_content = []
    formated_description = []   
    imgurl = "no image"
    
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
     
    # meta_tags = soup.find_all('meta')
    
    # for tag in meta_tags:
      
    #     # Extract content attribute of meta tags
    #     content_meta = tag.get('content')
  
    #     if tag.get('property') == 'og:description':
    #         content = content_meta
    #         formated_content = content
    #         formated_content = formated_content.replace("\u2019", "'").replace("\u2026", "")
    
    formated_content = open_AI_content(url)
    
    descriptions = soup.find(attrs={"class": "max-w-736 mx-auto text-body-lg text-rich"})
    for descript in descriptions.children:
        description.append(descript.text)
        formated_description = ' '.join(description).replace('\n', '').replace("\u2019", "'").replace("\u201c", "“").replace("\u201d", "”")            
    
    # formated_description = open_AI_description(url)
        
    img = soup.find(attrs={"class": "absolute h-full inset-0 object-cover w-full"})
    if img:
        imgurl = img['src']
    
    # / ------------- Map ------------- /          
    # map_urls = soup.find_all( "a", class_ =  "button-secondary" ) 
    # map_url = map_urls[10].get('href')  
    # map_data_url = scrape_map_site (map_url)
    # map_info = scrape_map_info (map_data_url)
    
    map_info = "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"
    
    if formated_content and formated_description and imgurl and map_info:
            
        return {
            "content": formated_content,
            "description": formated_description,
            "image": imgurl,
            "map": map_info
        }

def scrape_map_site(url):
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Find the UtilityNav div
    utility_nav = soup.find("div", id="UtilityNav")

    # Find all li elements within the UtilityNav div
    nav_items = utility_nav.find_all("li")

    # Loop through the li elements to find the maps link
    map_data_url = None
    
    for item in nav_items:
        # Find the 'a' tag within the 'li' element
        a_tag = item.find("a")
        if a_tag and "maps.htm" in a_tag.get("href"):
            map_data_url = urljoin(base_url, a_tag.get("href"))
            break

    return map_data_url

def scrape_map_info(url):
    return "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"
    # # Send a GET request to the URL
    # response = requests.get(url)

    # # Check if the request was successful
    # if response.status_code == 200:
    #     # Parse the HTML content
    #     soup = BeautifulSoup(response.content, 'html.parser')
        
    #     # Find the <iframe> element with title="Map Embed"
    #     iframe = soup.find('iframe', title="Map Embed")
        
    #     # Check if the iframe element exists
    #     if iframe:
    #         # Extract the value of the src attribute
    #         map_src = iframe.get('src')
            
    #         return map_src
    #     else:
            
    #         return None
    # else:

    #     return None

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
        
        if park_url :
            index += 1
            
            if index >= 1 :
                # Scrape park data
                scraped_data = scrape_park_data(park_url)

                # Add scraped data to output
                output_data[state]["parks"].append({
                 "name": park_name,
                  "url": park_url,
                 **scraped_data
                })
                # Write output JSON
                with open('data_national_parks.json', 'w') as json_file:
                    json.dump(output_data, json_file, indent=4)
                time.sleep(3)