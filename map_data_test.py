import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://www.nps.gov"

map_url = "https://www.nps.gov/bicr/index.htm"

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
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the <iframe> element with title="Map Embed"
        iframe = soup.find('iframe', title="Map Embed")
        
        # Check if the iframe element exists
        if iframe:
            # Extract the value of the src attribute
            map_src = iframe.get('src')
            
            return map_src
        else:
            
            return None
    else:

        return None

# Get the map data URL
map_data_url = scrape_map_site(map_url)
print("Map data URL:", map_data_url)

# Scrape map information
map_info = scrape_map_info(map_data_url)

# Print the map information
if map_info:
    print("Map_info:", map_info)