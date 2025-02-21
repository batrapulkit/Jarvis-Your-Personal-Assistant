import streamlit as st
import wikipedia
import requests
from PIL import Image

# Function for Wikipedia search
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous query: {e.options}"

# Function to get weather information
def get_weather(city):
    api_key = "YOUR_API_KEY"  # Replace with your own OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temperature = main["temp"] - 273.15  # Convert from Kelvin to Celsius
        return f"The temperature in {city} is {temperature:.2f}°C with {weather_desc}."
    else:
        return "City not found."

# Main Streamlit interface
st.title("Jarvis - Your Personal Assistant")
st.write("Hello, I am Jarvis. How can I assist you today?")

# Text input option for user command
command = st.text_input("Enter your command:")

if command:
    st.write(f"You entered: {command}")
    
    # Processing commands
    if "wikipedia" in command.lower():
        query = command.replace("wikipedia", "").strip()
        result = search_wikipedia(query)
        st.write(result)
    elif "weather" in command.lower():
        city = command.replace("weather", "").strip()
        weather_info = get_weather(city)
        st.write(weather_info)
    else:
        response = "Sorry, I didn't understand the command."
        st.write(response)

# Upload an image for PIL (Pillow) processing
st.write("Upload an image to perform basic operations:")
image_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if image_file is not None:
    # Open the uploaded image
    image = Image.open(image_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert the image to grayscale (using Pillow)
    gray_image = image.convert("L")
    st.image(gray_image, caption="Grayscale Image", use_column_width=True)
