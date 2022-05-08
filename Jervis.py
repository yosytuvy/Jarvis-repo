import datetime
import json
import os
import smtplib
import time as t
import webbrowser as wb
from urllib.request import urlopen
import psutil
import pyautogui
import pyjokes
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
from secret import passw


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(Time)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(date)
    speak(month)
    speak(year)


def wishme():
    speak("Welcome back sir!")
    speak("the current time is")
    time()
    speak("the current date is")
    date()
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    elif 18 <= hour < 24:
        speak("Good Evening sir!")
    else:
        speak("Good night sir!")
    speak("javris at your service. Please tell me how can i help you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-US")
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"

    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your mail address here...', passw)
    server.sendmail('your mail address here...', to, content)
    server.close()


def screenshot():
    img = pyautogui.screenshot()
    img.save('path where you want to store the screenshot')


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at' + usage)

    battery = psutil.sensors_battery()
    speak('Battery is at ' + str(battery.percent) + 'percent.')


def joke():
    speak(pyjokes.get_joke())


if __name__ == "__main__":
    wishme()

    while True:
        query = takeCommand().lower()

        if 'time' in query:
            time()

        elif 'date' in query:
            date()

        elif 'wikipedia' in query:
            speak("Searching...")
            query = query.replace('wikipedia', '')
            result = wikipedia.summary(str(query), sentences=3)
            speak('According to Wikipedia')
            print(result)
            speak(result)

        elif 'send email' in query:
            try:
                speak("What should i say?")
                mailContent = takeCommand()

                speak("Who is the Receiver?")
                # receiver = input("Enter Receiver's Email :")

                receiver = 'the receiver mail'
                toEmail = receiver
                sendEmail(toEmail, mailContent)
                speak(mailContent)
                speak("Email has been sent.")

            except Exception as e:
                print(e)
                speak("Unable to send Email.")

        elif 'website' in query:
            speak('What should I search?')
            chromepath = 'put here a path to your chrome.exe'

            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')

        elif 'youtube' in query:
            speak('What should I search?')
            search_Term = takeCommand().lower()
            wb.open('https://www.youtube.com/results?search_query=' + search_Term)

        elif 'google' in query:
            speak('What should I search?')
            search_Term = takeCommand().lower()
            speak('Searching...')
            wb.open('https://www.google.com/search?q=' + search_Term)

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'go offline' in query:
            speak('Going Offline sir!')
            quit()

        elif 'word' in query or 'world' in query or 'wallet' in query:
            speak("Opening MS word...")
            ms_word = r'path to your WINWORD.EXE here'
            os.startfile(ms_word)

        elif 'write note' in query:
            speak('What should I write sir?')
            notes = takeCommand()
            file = open('notes.txt', 'a')
            speak("sir should I include Date and Time?")
            ans = takeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                strYear = str(datetime.datetime.now().year)
                strMonth = str(datetime.datetime.now().month)
                strDate = str(datetime.datetime.now().day)
                file.write(str(strYear + '-' + strMonth + '-' + strYear + ' ' + strTime + '\n'))
                file.write(str(notes) + '\n')
                speak('Done Taking Notes Sir!')
            else:
                file.write(notes)

        elif 'show note' in query or 'show no' in query:
            speak('showing notes')
            file = open('notes.txt', 'r')
            print(file.read())
            read = str(file.read())
            speak(read)

        elif 'screenshot' in query:
            screenshot()

        elif 'play music' in query or 'spotify' in query:
            # songs_dir = 'songs path'
            # music = os.listdir(songs_dir)
            # speak("What should I play?")
            # ans = takeCommand()
            # no = int(ans.replace('number', ''))
            # os.startfile(os.path.join(songs_dir + music[no]))

            spotify_path = 'path to your Spotify.exe here '
            speak('opening Spotify')
            os.system(spotify_path)

        elif 'remember that' in query:
            speak("What should I remember?")
            memory = takeCommand()
            speak("You asked me to remember that" + memory)
            remember = open('memory.txt', 'w')
            remember.write(memory)
            remember.close()

        elif 'you remember' in query:
            remember = open('memory.txt', 'r')
            speak('You asked me to remember that ' + remember.read())

        elif 'where is' in query:
            query = query.replace('where is', "")
            location = query
            speak("User asked to locate " + location)
            wb.open_new_tab("https://www.google.com/maps/place/" + location)

        elif 'news' in query:
            try:
                jsonObj = urlopen('http://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=ba36a870b49c4259b72055ec2704b0a2')
                data = json.load(jsonObj)
                i = 1

                speak('Here are some top headlines from the business Industry')
                print('===========TOP HEADLINES===========' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(item['title'])
                    i += 1

            except Exception as e:
                print(str(e))

        elif 'what is' in query or 'who is' in query:
            client = wolframalpha.Client(wolframalpha_app_id)
            res = client.query(query)

            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No Results")

        elif 'stop listening' in query:
            speak("For How many second you want me to stop listening to you commands?")
            ans = int(takeCommand())
            t.sleep(ans)
            print(ans)
            
        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system('shutdown /s /t 1')
