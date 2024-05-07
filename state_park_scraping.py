import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://www.alapark.com/"

def scrape_park_data(url):   
    formated_content = []
    description = []
    formated_description = []   
    imgurl = "no image"
    
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
     
    meta_tags = soup.find_all('meta')
    
    for tag in meta_tags:
        content_meta = tag.get('content')
  
        if tag.get('property') == 'og:description':
            content = content_meta
            formated_content = content.replace("\u2019", "'").replace("\u2026", "")
    
    descriptions = soup.find(attrs={"class": "max-w-736 mx-auto text-body-lg text-rich"})
    for descript in descriptions.children:
        description.append(descript.text)
    
    formated_description = ' '.join(description).replace('\n', '').replace("\u2019", "'").replace("\u201c", "“").replace("\u201d", "”")             
        
    img = soup.find(attrs={"class": "absolute h-full inset-0 object-cover w-full"})
    if img:
        imgurl = img['src']
    
    map_info = "/maps/embed.html?alpha=tuai&mapId=d227494d-87cc-489c-ad4e-7a861cec6ca6"
    
    if formated_content and formated_description and imgurl and map_info:
        return {
            "content": formated_content,
            "description": formated_description,
            "image": imgurl,
            "map": map_info
        }

with open('state_parks.json', 'r', encoding='utf-8') as file:
    input_data = json.load(file)

output_data = {}

for state, parks in input_data.items():
    index = 0
    output_data[state] = {"parks": []}  
    
    for park_name, park_url in parks.items():
        print(index) 
        if park_url:
            index += 1
            if index >= 1:
                scraped_data = scrape_park_data(park_url)
                output_data[state]["parks"].append({
                    "name": park_name,
                    "url": park_url,
                    **scraped_data
                })

                with open('data_state_parks.json', 'w') as json_file:
                    json.dump(output_data, json_file, indent=4)