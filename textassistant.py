import clipboard
import datetime
import os
import psutil
import pyautogui
import pyjokes
import pyttsx3
import pywhatkit
import requests
import smtplib
import speech_recognition as sr
import time as ti
import webbrowser as we
from email.message import EmailMessage
from newsapi import NewsApiClient
from secrets import senderemail, password
from time import sleep


user = "ProjectU"
assistant= "Zoom" 
engine = pyttsx3.init()
voices = engine.getProperty("voices")

engine.setProperty("voice", voices[0].id)
# For Female voice
# engine.setProperty("voice", voices[1].id)

def output(audio):
    # print(audio) # For printing out the output
    engine.say(audio)
    engine.runAndWait()

# For getting the device index you can execute this code So if you want to change the device you can do that.
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(
#         index, name))

def inputCommand():
    # query = input() # For getting input from CLI
    r = sr.Recognizer()
    query = ""
    with sr.Microphone(device_index=2) as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            query = r.recognize_google(r.listen(source), language="en-IN")
        except Exception as e:
            output("Say that again Please...")
    return query

def greet():
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        output(f"Good Morning {user}")
    elif (hour >= 12) and (hour < 18):
        output(f"Good afternoon {user}")
    elif (hour >= 18) and (hour < 21):
        output(f"Good Evening {user}")
    output("How may I assist you?")
    
def sendEmail():
    senderemail = "rdhoka@hotmail.com"
    password = "r"
    email_list = {
        "test1": "bojole7513@httptuan.com", # Temporary Email
        "test2": "<Your Friends, family or business email here>"
    }
    try:
        email = EmailMessage()
        output("To whom you want to send the mail?")
        name = inputCommand().lower()
        email['To'] = email_list[name]
        output("What is the subject of the mail?")
        email["Subject"] = inputCommand()
        email['From'] = senderemail
        output("What should i Say?")
        email.set_content(inputCommand())
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(senderemail, password)
        s.send_message(email)
        s.close()
        output("Email has sent")
    except Exception as e:
        print(e)
        output("Unable to send the Email")
        
def weather():
    city = "San Francisco"
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=16f0afad2fd9e18b7aee9582e8ce650b&units=metric").json()
    temp1 = res["weather"][0]["description"]
    temp2 = res["main"]["temp"]
    output(
        f"Temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}")
def idea():
    output("What is your idea?")
    data = inputCommand().title()
    output("You Said me to remember this idea: " + data)
    with open("data.txt", "a", encoding="utf-8") as r:
        print(data, file=r)
        
greet()
# Then with while true we can make it a infinite loop on command
while True:
    # Getting input from the user
    query = inputCommand().lower()
    # According to the query if query have respective word we will execute the respective command
    if ("time" in query):
        output("Current time is " +
               datetime.datetime.now().strftime("%I:%M"))

    elif ('date' in query):
        output("Current date is " + str(datetime.datetime.now().day)
               + " " + str(datetime.datetime.now().month)
               + " " + str(datetime.datetime.now().year))

    elif ('email' in query):
        sendEmail()

    elif ('message' in query):
        print("Sending...")
        sendWhatMsg()

    elif ("search" in query):
        output("what you want to search?")
        we.open("https://www.google.com/search?q="+inputCommand())

    elif ("youtube" in query):
        output("What you want to search on Youtube?")
        pywhatkit.playonyt(inputCommand())

    elif ('weather' in query):
        weather()

    elif ("news" in query):
        news()

    elif ("read" in query):
        output(clipboard.paste())

    elif ("covid" in query):
        r = requests.get(
            'https://coronavirus-19-api.herokuapp.com/all').json()
        output(
            f'Confirmed Cases: {r["cases"]} \nDeaths: {r["deaths"]} \nRecovered {r["recovered"]}')

    elif ("workspace" in query):
        output("Which workspace you want to work on")
        os.startfile("D:\\Work Spaces\\" +
                     inputCommand()+".code-workspace")

    elif ("joke" in query):
        output(pyjokes.get_joke())

    elif ("idea" in query):
        idea()

    elif ("do you know" in query):
        ideas = open("data.txt", "r")
        output(f"You said me to remember these ideas:\n{ideas.read()}")

    elif ("screenshot" in query):
        pyautogui.screenshot(str(ti.time()) + ".png").show()

    elif "cpu" in query:
        output(f"Cpu is at {str(psutil.cpu_percent())}")

    elif "offline" in query:
        hour = datetime.datetime.now().hour
        if (hour >= 21) and (hour < 6):
            output(f"Good Night {user}! Have a nice Sleep")
        else:
            output(f"By {user}")
        quit()