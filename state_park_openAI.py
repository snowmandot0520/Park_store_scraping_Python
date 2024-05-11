import os
from dotenv import load_dotenv
import openai
import json


# Set up your OpenAI API key

api_key = os.getenv('API_KEY')
openai.api_key = api_key

def generate_park_info(park_name, park_url):
    # Define the input prompt and parameters
    input_prompt = f'Tell me about "{park_name}" based on "{park_url}"'
    output_template = """
    "name": "{park_name}",
    "url": "{park_url}",
    "content": "",
    "description": "",
    "img": "",
    "map": ""
    """.format(park_name, park_url)

    # Use the OpenAI API to generate the output
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=input_prompt + output_template,
        temperature=0.7,
        max_tokens=400,
        n=1,
    )

    # Extract the generated output from the responseython
    generated_output = response['choices'][0]['text']
    
    # Parse the output as a JSON object
    output_json = "{" + generated_output + "}"

    return output_json

# Example usage
park_name = "Birmingham Civil Rights National Monument"
park_url = "https://www.nationalparks.org/explore/parks/birmingham-civil-rights-national-monument"

generated_json = {""}
generated_json = generate_park_info(park_name, park_url)

# Print the generated JSON
print(generated_json)

# You can also write the JSON to a file if needed
# with open('output.json', 'w') as f:
#     f.write(generated_json)
