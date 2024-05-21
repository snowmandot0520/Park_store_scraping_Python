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
import re
import random

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
    # base_url = get_base_url(park_url)
    base_url = "https://parks.wa.gov/"
    
    # r = requests.get(park_url)
    # soup = BeautifulSoup(r.text, 'html.parser')
    
    # image_url = [
    # "https://cdn.elebase.io/dbcc75a2-4b9f-4a0e-8e4b-cfa273624e10/39e5aa9c-f4e4-4163-af3c-263b9bbbed67-vtmd1126b54710260165.jpg",
    # "https://cdn.elebase.io/dbcc75a2-4b9f-4a0e-8e4b-cfa273624e10/a246618e-3b9b-47e8-bea0-8a150f31d15f-vtm75b77f0fadecac71c.jpg",
    # "https://cdn.elebase.io/dbcc75a2-4b9f-4a0e-8e4b-cfa273624e10/553f9268-d09c-4677-a95a-6f33b58ebc34-vtm9bf61be5cb221cc06.jpg",
    # "https://cdn.branchcms.com/l4gOa2eDBE-756/images/trails/trail-system/IMG_6938-1.1686744195.jpg",
    # "https://cumberlandriverbasin.org/wp-content/uploads/2020/11/General-Burnside-1024x684.jpeg",
    # "https://www.nrcm.org/wp-content/uploads/2020/06/Debouille-David-Preston-600x400.jpg",
    # "https://www.sierraclub.org/sites/default/files/styles/sierra_full_page_width/public/sierra/articles/big/SIERRA%20Mount%20Katahdin%20WB.jpg.webp?itok=uowIzbRy",
    # "https://www.nrcm.org/wp-content/uploads/2015/08/Little-Moose-Public-Reserved-Land-Big-Moose-Pond-500x300.jpg",
    # "https://umaine.edu/news/wp-content/uploads/sites/3/2020/01/Shell-middens-Kelley-news-feature.jpg",
    # "https://s7d1.scene7.com/is/image/isp/mazoniabraidwood-3501-e-360600?ts=1674260936479&$SlideshowThumbnail$"
    # ]
    image_url = [
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=IMG_4295.jpg",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=ainsworth-0006083505.jpg",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Loeb105200.jpg",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=02-IMG_2032.jpg",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Beverly_Beach_Beach_Ocean_%281%29041737.jpg&park=164&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=1217369894Bob+Straub+Park+DSC_0034.jpg&park=133&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=index071937.jpg&park=100&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=index071937.jpg&park=100&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=1217370318Fogerty+Creek0055Fogerty+Creek.jpg&park=158&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Base_of_Latourell_Falls044758.jpg&park=112&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Lake_Owyhee_DSC_0186-east-8100236.jpg&park=10&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=36-IMG_2765.jpg&park=88&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Marshall_Island_1110900.jpg&park=216&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=2196c6ce-090a-cccc-7b476b14d4e277ba.jpg&park=194&fit=cover&w=1200&h=600",
       "https://stateparks.oregon.gov/index.cfm?do=image.get&name=Yachats_SRA_viewing_platform125108.jpg&park=94&fit=cover&w=1200&h=600" 
    ]
    image_url = image_url[random.randint(0, 14)]
    # random_integer = random.randint(0, 9)
    # image_url = image_url[random_integer]
    
    # image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
    
    # div_element = soup.find('div', class_="carousel-item active")
    # style_attribute = div_element["style"]
    # url_pattern = r"url\('(.*?)'\)"
    # url_match = re.search(url_pattern, style_attribute)

    # if url_match:
    #     url = url_match.group(1)
    #     image_url = url
        
    # else:
    #     print("URL not found in the style attribute.")


    # image_src = soup.select_one('div.landing-page__main_image')['style'].split('(')[1].split(')')[0].strip('"')
    
    # if image_src:
    #     image_url = image_src
    # else:
    #     image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"

    # print(image_url)
    
    
    
    # -------------------------------------------------------
    # div_element1 = soup.find('div', class_="wrapper-content layout-main-wrapper clearfix container")
    
    
    # # div_element3 = div_element2.find('div', class_="flex-viewport")
    
    # if div_element1:
    #     div_element2 = div_element1.find('div', class_="field--name-field-media-image")
    #     # print(div_element2)
    #     # img_src = div_element4[random.randint(0, 4)].select_one('div.slides-image')['style'].split('(')[1].split(')')[0].strip('"')
        
    #     if div_element2: 
    #         img_element = div_element2.find('img')
        
    #         if img_element:
    #             # img_element = div_element3.find_all('img',class_ = "rsImg")
    #             # image_url = img_element.select_one('div.landing-page__main_image')['style'].split('(')[1].split(')')[0].strip('"')
        
    #             img_src = img_element["src"]
                
    #             if img_src:
    #                 image_url = urljoin(base_url,img_src)
    #             else:
    #                 image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
            
    #         else:
    #             print("img not found")
    #             image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
    #     else:
    #         print("img not found")
    #         image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
    
    # else:
    #     print("Div element not found.")
    #     image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
    
    # print(image_url)
    # ----------------------------------------    
    
    # img_src = div_element.get["src"]
    # image_url = urljoin(base_url,img_src)
    
    
            
    # img_src = img_element["src"]
    # image_url = urljoin(base_url,img_src)
    
    
    
    # slide_content = soup.find("div", id_= "property-image")
    
    # if slide_content:
    #     img_tag = slide_content.find("img")
                
    #     # If the img tag is found, print its source (src) attribute
    #     if img_tag:
    #         img_src = img_tag.get["src"]
    #         image_url = urljoin(base_url,img_src)
    #         print("okay")
            
    #     else:
    #         image_url = "https://gastateparks.org/sites/default/files/styles/locationslidestyle/public/parks/locationslideshow/CloudandCanyon2.jpg?itok=Ym2cTXQ7"
    # else:
    #     carousel_content =  slide_content = soup.find("div", class_= "carousel-inner")
    #     if carousel_content:
    #         img_tag = carousel_content.find("img")
    #         if img_tag:
    #             img_src = img_tag.get("src")
    #             image_url = img_src
    #             # print(f"Image source: {image_url}")
    #     else:
    #         image_url = "no image"   
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
    
    # Construct the URL for the Google Maps Embed API request
    map_url = f'https://www.google.com/maps/embed/v1/place?key={map_key}&q={urllib.parse.quote(parkname)}'
    if map_url:
        return map_url
    

# Load input JSON
with open('state_parks8 copy 3.json', 'r',encoding='utf-8') as file:
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
                with open('database_state_parks8_3.json', 'w') as json_file:
                    json.dump(output_data, json_file, indent=4)
                