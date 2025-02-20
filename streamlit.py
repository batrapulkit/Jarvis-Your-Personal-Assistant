import pyttsx3
import datetime
import speech_recognition as sr
import streamlit as st
import webbrowser
import requests

# Initialize pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def get_weather(city_name):
    api_key = "your_api_key"  # Replace with your actual WeatherAPI key
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=no"  
    response = requests.get(base_url)
    
    try:
        data = response.json()

        if "error" in data:
            return "City not found."
        else:
            location = data["location"]["name"]
            temperature = data["current"]["temp_c"]
            condition = data["current"]["condition"]["text"]
            return f"The weather in {location} is {condition}. The temperature is {temperature}°C."
    except Exception as e:
        return "Sorry, I couldn't fetch the weather information."

def main():
    st.title("Jarvis - Your Personal Voice Assistant")
    st.write("### Interact with Jarvis using voice commands!")

    # Weather Input
    city = st.text_input("Enter the city for weather:", "")
    if city:
        weather_info = get_weather(city)
        st.write(weather_info)
    
    # Button to start voice interaction
    if st.button("Start Voice Interaction"):
        speak("Hello, I am Jarvis. What can I do for you today?")
        query = takeCommand()
        if query == "none":
            st.write("I didn't hear anything. Please try again.")
        else:
            st.write(f"Jarvis heard: {query}")
            if "wikipedia" in query:
                st.write("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = "Wikipedia result placeholder"
                st.write(results)
                speak(results)
            elif "open youtube" in query:
                webbrowser.open("https://youtube.com")
                st.write("Opening YouTube")
                speak("Opening YouTube")
            elif "weather" in query:
                st.write(f"The weather in {city} is: {get_weather(city)}")
            elif "exit" in query:
                speak("Goodbye, have a nice day!")
                st.write("Goodbye!")

if __name__ == "__main__":
    main()
