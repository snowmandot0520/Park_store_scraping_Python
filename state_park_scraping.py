import json
import asyncio
import requests
from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
import urllib.parse
import os
import logging


from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

# Cache configs
PARK_CACHE = TTLCache(maxsize=1000, ttl=3600)  
OPENAI_CACHE = TTLCache(maxsize=100, ttl=86400)

data = []

async def scrape_park(park_name, park_url):

  # Check cache
  if park_name in PARK_CACHE:
    return PARK_CACHE[park_name]

  try:

    # Scrape data concurrently
    html = await asyncio.to_thread(requests.get, park_url)  
    description = OPENAI_CACHE[f"desc-{park_name}"]

    # Process, validate, cache data
    ...

  except Exception as e:
    log_error(e)
    return None

  finally:  
    PARK_CACHE[park_name] = data

  return data


async def main():

  # Validate input 
  try:
    data = json.load(open("input.json")) 
  except FileNotFoundError:
    log_error("Input file not found")
    exit()

  # Scrape concurrently 
  tasks = [
    scrape_park(name, url) 
    for state in data 
    for name, url in state["parks"].items()
  ]

  results = await asyncio.gather(*tasks)

  # Output results
  with open("output.json", "w") as f:
    json.dump(results, f, indent=2)

if __name__ == "__main__":
  asyncio.run(main())