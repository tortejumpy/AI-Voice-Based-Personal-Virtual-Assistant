import requests
from functions.online_ops import (
    find_my_ip,
    get_random_advice,
    get_random_joke,
    play_on_youtube,
    search_on_google,
    search_on_wikipedia,
    send_whatsapp_message,
    get_weather_report,
    get_trending_movies
)
from functions.os_ops import (
    open_notepad,
    open_cmd,
    open_camera,
    open_calculator
)
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from utils import opening_text

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def greet_user():
    """Greet the user based on the current time."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning, {USERNAME}.")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon, {USERNAME}.")
    elif 16 <= hour < 19:
        speak(f"Good Evening, {USERNAME}.")
    speak(f"I am {BOTNAME}. How may I assist you today?")


def take_user_input():
    """Take user input via the microphone and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        if 'exit' not in query and 'stop' not in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 or hour < 6:
                speak("Good night, take care!")
            else:
                speak("Have a good day!")
            exit()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return "None"
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting. Please try again later.")
        return "None"
    return query.lower()


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input()

        if 'wikipedia' in query:
            speak("What should I search on Wikipedia?")
            search_query = take_user_input()
            if search_query != "None":
                results = search_on_wikipedia(search_query)
                speak(f"According to Wikipedia: {results}")
                print(results)

        elif 'youtube' in query:
            speak("What do you want to play on YouTube?")
            video = take_user_input()
            if video != "None":
                play_on_youtube(video)

        elif 'search on google' in query:
            speak("What do you want to search on Google?")
            google_query = take_user_input()
            if google_query != "None":
                search_on_google(google_query)

        elif "send whatsapp message" in query:
            speak("To which number should I send the message? Please include the country code.")
            number = take_user_input()
            if number != "None":
                speak("What message should I send?")
                message = take_user_input()
                if message != "None":
                    send_whatsapp_message(number, message)
                    speak("Message sent successfully.")

        elif 'joke' in query:
            speak("Here's a joke for you!")
            joke = get_random_joke()
            speak(joke)
            print(joke)

        elif 'advice' in query:
            speak("Here's some advice for you.")
            advice = get_random_advice()
            speak(advice)
            print(advice)

        elif 'weather' in query:
            speak("For which city do you need the weather report?")
            city = take_user_input()
            if city != "None":
                weather = get_weather_report(city)
                speak(f"The weather in {city} is {weather[0]} with a temperature of {weather[1]} and feels like {weather[2]}.")
                print(weather)

        elif 'trending movies' in query:
            speak("Fetching the latest trending movies...")
            movies = get_trending_movies()
            speak(f"Here are the trending movies: {', '.join(movies)}.")
            print(movies)

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f"Your IP address is {ip_address}")
            print(ip_address)

        elif 'open notepad' in query:
            speak("Opening Notepad.")
            open_notepad()

        elif 'open command prompt' in query or 'open cmd' in query:
            speak("Opening Command Prompt.")
            open_cmd()

        elif 'open camera' in query:
            speak("Opening Camera.")
            open_camera()

        elif 'open calculator' in query:
            speak("Opening Calculator.")
            open_calculator()

        elif 'exit' in query or 'stop' in query:
            speak("Shutting down. Have a great day!")
            break

        else:
            speak("Sorry, I didn't understand that. Please try again.")

