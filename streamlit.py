import streamlit as st
import pyttsx3
import speech_recognition as sr
import wikipedia
import requests
from PIL import Image

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set up voice property
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to your desired voice index

# Function for text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, I couldn't reach the Google API.")
            return None

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

# Speech input option
if st.button("Start Voice Interaction"):
    command = recognize_speech()
    if command:
        speak(f"You said: {command}")
        
        # Processing commands
        if "wikipedia" in command.lower():
            query = command.replace("wikipedia", "")
            result = search_wikipedia(query)
            st.write(result)
            speak(result)
        elif "weather" in command.lower():
            city = command.replace("weather", "").strip()
            weather_info = get_weather(city)
            st.write(weather_info)
            speak(weather_info)
        else:
            response = "Sorry, I didn't understand the command."
            st.write(response)
            speak(response)

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

    speak("I have processed the image and converted it to grayscale.")

# Simple text-to-speech input/output
st.text_input("Enter text to hear it spoken:", key="text_input")
if st.session_state.text_input:
    text = st.session_state.text_input
    speak(text)
    st.write(f"Text: {text}")
