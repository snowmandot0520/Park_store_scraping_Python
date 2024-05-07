import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL
response = requests.get("https://www.alapark.com/parks/bladon-springs-state-park")

# Get the HTML content from the response
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the image tag with the specified class or attribute
target_url = soup.find('img', {'src': 'sites/default/files/styles/default/public/2018-08'})['src']
# Extract the 'src' attribute value
image_url = target_url['src']

# Print the image URL
print(image_url)