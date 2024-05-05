import urllib.parse
import requests

park_name = "Amache National Historic Site"  # Example park names
api_key = "AIzaSyD5wMutNGsQaLWdYUpH0fqaD1utNIBOmU4"  # Replace with your actual API key
content = []

encoded_name = urllib.parse.quote(park_name)

src = "https://www.google.com/maps/embed/v1/place?key=AIzaSyD5wMutNGsQaLWdYUpH0fqaD1utNIBOmU4&q={encoded_name}"

response = requests.get(src)
content = response.text

print (content) 
# iframes = [create_iframe(park) for park in parks]
# print(iframes)  # Prints iframe HTML strings to the console