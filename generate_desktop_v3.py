import openai
from openai import OpenAI
import requests
import random
import ctypes
from datetime import datetime
import os
from io import BytesIO
from PIL import Image

def read_api_key_from_file(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Read OpenAI API key from the file
api_key_path = 'AI.key'
client = OpenAI(api_key=read_api_key_from_file(api_key_path))

def read_interests_from_file(file_path):
    with open(file_path, 'r') as file:
        interests = file.read().splitlines()
    return interests

def generate_image(category):
    text_response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Describe an interesting desktop background based on the category of {category}",
        max_tokens=600,
        temperature=1
    )
    print(f"Generating an exciting background based on {category}")
    # Provide a prompt for image generation
    prompt = f"{text_response.choices[0].text}"
    print(prompt)

    # Generate images using the DALL-E model
    response = client.images.generate(
        model="dall-e-3",  # Specify the DALL-E model engine
        prompt=prompt,
        size="1792x1024",
        quality="hd"
    )
    print(response.data[0].url)
    return response.data[0].url

def set_wallpaper(image_path):
    # This function sets the wallpaper on Windows using ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    
def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def main():
    current_date = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year
    print("Current date:", current_date)

    interests_file_path = 'interests.txt'
    interests = read_interests_from_file(interests_file_path)
    random_interest = random.choice(interests)

    image_data = generate_image(random_interest)
    image = download_image(image_data)

    image_path = os.path.join(os.getcwd(), f'{current_date}_{current_month}_{current_year}_wallpaper_{random_interest}.bmp')
    image.save(image_path, 'BMP')  # Save as BMP format
    
    set_wallpaper(image_path)

    print(f"Wallpaper set to: {image} (Interest: {random_interest})")

if __name__ == "__main__":
    main()
