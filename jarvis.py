import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import subprocess
import smtplib
import requests
import PyDictionary
from PyDictionary import PyDictionary
import time
import re
import tkinter as tk
import cv2
import threading

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening")
    
    speak("Hello Pulkit")
    speak("I am Jarvis")
    speak("What can i do for you sir?")

def takeCommand():
    # It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def set_reminder(reminder_time, reminder_message):
    reminder[reminder_time] = reminder_message
    speak(f"Reminder set for {reminder_time}")
reminder = {}


# Function to get weather details from WeatherAPI
def get_weather(city_name):
    api_key = ""  
    base_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_name}&aqi=no"  
    response = requests.get(base_url)   
    print(response.text)

    try:
        data = response.json()

        if "error" in data:
            speak("City not found.")
        else:
            # Extract weather details
            location = data["location"]["name"]
            region = data["location"]["region"]
            country = data["location"]["country"]
            temperature = data["current"]["temp_c"]  
            condition = data["current"]["condition"]["text"]
            humidity = data["current"]["humidity"]
            wind_speed = data["current"]["wind_kph"]

            speak(f"The weather in {location}, {region}, {country} is {condition}. The temperature is {temperature}°C, humidity is {humidity}%, and the wind speed is {wind_speed} km/h.")

    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information.")
        print(f"Error: {e}")

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# to send email to the user
# def sendEmail(to, content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login('mrhacker2077@gmail.com', 'pulkit@123')
#     server.sendmail('mrhacker2077@gmail.com , to, content)
#     server.close()



def check_reminders():
    """Function to check and notify reminders."""
    current_time = datetime.datetime.now().strftime("%H:%M")
    if current_time in reminder:
        speak(f"Reminder: {reminder[current_time]}")
        del reminder[current_time]


# dictionary=PyDictionary()
# def define(query):
#     """Function to define a word using PyDictionary."""
#     if "define" in query:
#         word = query.replace("define", "").strip()
#         definition = dictionary.meaning(word)
#         if definition:
#             meanings = ", ".join([f"{key}: {', '.join(value)}" for key, value in definition.items()])
#             speak(f"The definition of {word} is: {meanings}")
#         else:
#             speak(f"Sorry, I couldn't find the definition of {word}. Please try again later.")




if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif "Hi jarvis" in query:
            speak("Hello sir, How can I help you?")
            
        elif "how are you" in query:
            speak("I am good, sir. How can I assist you today?")
        
        
        elif "What's your name?" in query:
            speak("I am Jarvis, your personal assistant.")

        elif "open youtube" in query:
            speak("Opening Youtube")
            webbrowser.open("youtube.com")
        
        elif "open linkedin" in query:
            speak("Opening Linkedin")
            webbrowser.open("linkedin.com")
        
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("google.com")
        
        elif "open chatgpt" in query:
            speak("Opening ChatGPT")
            webbrowser.open("chatgpt.com")

        
        elif "open github" in query:
            speak("Opening Github")
            webbrowser.open("github.com")

        elif "open camera" in query:
            speak("Sorry , I Can not open the camera .")
            open_camera()

        # to play 1st song from the list 
        # elif 'play music' in query:
        #music_dir = "C:\\Users\\Pulkit\\Music"
        #songs = os.listdir(music_dir)
        #print(songs)
        #os.startfile(os.path.join(music_dir, songs[0]))
        
        elif "play music" in query:
            music_dir = "C:\\Users\\Pulkit\\Music"
            songs = [f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav", ".aac"))]
            speak("Playing music Sir")

            if songs:
                random_song = random.choice(songs)
                song_path = os.path.join(music_dir, random_song)
                speak(f"Playing {random_song}")
                print(f"Playing: {random_song}")
                os.startfile(song_path)  # Open the song with the default media player

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "search" in query:
            query = query.replace("search", "")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Here are the search results for {query}.")

        elif "open code" in query:
            codePath = "D:\obs-studio\Microsoft VS Code\Code.exe"
            os.startfile(codePath)

        # elif 'email to pulkit' in query:
        #     try:
        #         speak("What is my Order sir?")
        #         content = takeCommand()
        #         to = "bugcrowd1103@gmail.com"
        #         sendEmail(to, content)
        #         speak("Email has been sent!")
        #     except Exception as e:
        #         print(e)
        #         speak("Sorry, I am not able to send this email")

        elif "set reminder" in query:
            speak("At what time do you want to set the reminder? Please use the format HH:MM.")
            reminder_time = takeCommand().lower()  # Get time from the user, e.g., "12:30"
            speak("What is the reminder?")
            reminder_message = takeCommand().lower()  # Get the reminder message, e.g., "Take a break"
            set_reminder(reminder_time, reminder_message)
            speak("Reminder set successfully.")

        elif "what is my reminder" in query:
            # Display all reminders
            for time, reminder in reminder.items():
                speak(f"At {time}, you have to: {reminder}")

        elif "what is my reminder" in query:
            if reminder:
                for time, msg in reminder.items():
                    speak(f"At {time}, you have to: {msg}")
            else:
                speak("You have no reminders set.")

                
        elif "calculate" in query:
            query = query.replace("calculate", "")
            try:
                result = eval(query)
                speak(f"The result is {result}")    
            except Exception as e:
                speak("Sorry, I couldn't calculate that.")

        elif "weather"  in query:
            speak("Which city do you want the weather for?")
            city = takeCommand().lower()  # Get the city name from user
            get_weather(city)  # Fetch and speak the weather details

        
        # elif "define" in query:
        #     word = query.replace("define", "").strip()
        #     definition = dictionary.meaning(word)
        #     if definition:
        #         speak(f"The definition of {word} is: {definition}")
        #     else:
        #         speak(f"Sorry, I couldn't find the definition of {word}.")

        elif "exit" in query:
            speak("Goodbye sir. Have a nice day.")

        






                