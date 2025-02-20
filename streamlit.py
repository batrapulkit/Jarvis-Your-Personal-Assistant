import streamlit as st
import gTTS
import os
import speech_recognition as sr
import wikipedia
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import cv2
import rich
import markdown_it
import pyttsx3
import time
import markdown

# Function to convert text to speech using gTTS
def speak(text):
    tts = gTTS.gTTS(text=text, lang='en')
    tts.save("assistant.mp3")
    os.system("mpg321 assistant.mp3")

# Function to recognize speech using SpeechRecognition
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I did not understand that"
    except sr.RequestError:
        return "Sorry, I'm having trouble connecting to the service"

# Function to search on Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=1)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "The Wikipedia service timed out. Please try again later."

# Function to take a screenshot using OpenCV
def take_screenshot():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    if ret:
        image = Image.fromarray(frame)
        image.save("screenshot.png")
        camera.release()
        return "screenshot.png"
    else:
        camera.release()
        return None

# Function to scrape a webpage using Selenium
def scrape_website(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    return page_content

# Streamlit app
def main():
    st.title("Jarvis - Your Personal Assistant")
    st.write("This app can perform various tasks like searching Wikipedia, recognizing speech, and more.")

    menu = ["Home", "Wikipedia Search", "Speech Recognition", "Take Screenshot", "Scrape Website", "Exit"]
    choice = st.sidebar.selectbox("Choose an option", menu)

    if choice == "Home":
        st.subheader("Welcome to Jarvis!")
        st.write("You can use this assistant to perform various tasks such as searching Wikipedia, taking screenshots, and scraping websites.")

    elif choice == "Wikipedia Search":
        st.subheader("Wikipedia Search")
        query = st.text_input("Enter a search query:")
        if st.button("Search"):
            if query:
                result = search_wikipedia(query)
                st.write(result)
                speak(result)
            else:
                st.write("Please enter a query.")

    elif choice == "Speech Recognition":
        st.subheader("Speech Recognition")
        if st.button("Start Listening"):
            speech = recognize_speech()
            st.write("You said:", speech)
            speak(speech)

    elif choice == "Take Screenshot":
        st.subheader("Take a Screenshot")
        if st.button("Capture Screenshot"):
            screenshot_path = take_screenshot()
            if screenshot_path:
                st.image(screenshot_path, caption="Captured Screenshot")
                speak("Screenshot captured successfully.")
            else:
                st.write("Failed to capture screenshot.")
                speak("Failed to capture screenshot.")

    elif choice == "Scrape Website":
        st.subheader("Web Scraping")
        url = st.text_input("Enter the website URL:")
        if st.button("Scrape"):
            if url:
                content = scrape_website(url)
                st.write(content[:1000])  # Display first 1000 characters of the content
                speak("Website scraped successfully.")
            else:
                st.write("Please enter a URL.")

    elif choice == "Exit":
        st.write("Goodbye!")
        st.stop()

if __name__ == "__main__":
    main()
