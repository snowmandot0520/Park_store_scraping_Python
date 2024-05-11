import urllib.parse

# Replace 'YOUR_API_KEY' with your actual API key
api_key = "AIzaSyBclMMx3l1l_RIauGZjoDHCNvb8-cxBqGM"

# Replace 'Birmingham Civil Rights National Monument' with the desired location
location = 'Birmingham Civil Rights National Monument'

# Construct the URL for the Google Maps Embed API request
api_url = f'https://www.google.com/maps/embed/v1/place?key={api_key}&q={urllib.parse.quote(location)}'

# Get the iframe data
iframe_data = f'<iframe src="{api_url}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'

src_data = api_url
print(src_data)
# Print or use the iframe data as needed
# print(iframe_data)
