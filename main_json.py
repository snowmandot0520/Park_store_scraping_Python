import requests
from bs4 import BeautifulSoup
import json
import csv

scraped_data = []

def scrap_one(url):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    
    data = []
    title = []
    content = []
    description = []
    map_url = []
    
    meta_tags = soup.find_all('meta')
    
    for tag in meta_tags:
        # Extract content attribute of meta tags
        content_meta = tag.get('content')
        
        # Extract title from meta tag with property="og:title" 
          
        if tag.get('property') == 'og:title':
            title = content_meta

        
        if tag.get('property') == 'og:description':
            content = content_meta
    
    descriptions = soup.find(attrs={"class": "max-w-736 mx-auto text-body-lg text-rich"})
    for descript in descriptions.children:
        description.append(descript.text)
        formated_description = ' '.join(description)
        formated_description = formated_description.replace('\n', '')
        
        
    img = soup.find(attrs={"class": "absolute h-full inset-0 object-cover w-full"})
    if img:
        imgurl = img['src']
    
              
    map_urls = soup.find_all( "a", class_ =  "button-secondary" ) 
    map_url = map_urls[10].get('href')    
        
    if title and content and description and imgurl :

        data = {
            "title:": title,
            "url:": url,
            "content:": content,
            "description:": formated_description,
            "img:": imgurl,
            "map" : map_url
        }
        return data

with open('test_sample.json', 'r', encoding='utf-8') as file:
    park_data = json.load(file)               
    
    for state, parks in park_data.items():
        for park, url in parks.items():
            
            data = scrap_one(url)
            print(data)
            
            with open('test_output.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4)
       