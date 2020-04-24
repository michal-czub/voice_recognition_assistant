import webbrowser
import datetime
import wikipedia
import gtts
import speech_recognition as sr
import random
import os
import playsound
import time
import subprocess
from googletrans import Translator
from googlesearch import search
import wolframalpha
from fbchat import Client
from fbchat.models import *

# input your wolfram-alpha api key
client = wolframalpha.Client('')


def speak(msg):
    print(f"[ASSISTANT]: {msg}")
    tts = gtts.gTTS(text=msg, lang="pl")
    temp_file = "voice.mp3"
    tts.save(temp_file)
    playsound.playsound(temp_file)
    os.remove(temp_file)


def speak_ENG(msg):
    print(f"[ENGLISH_ASSISTANT]: {msg}")
    tts = gtts.gTTS(text=msg, lang="en")
    temp_file = "eng_voice.mp3"
    tts.save(temp_file)
    playsound.playsound(temp_file)
    os.remove(temp_file)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Słucham...")
        # r.pause_threshold = 1
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language='pl-PL')
            print(f"[USER]: {said}")
        except sr.UnknownValueError as ex:
            print(f"[EXCEPTION]: {ex}")

        return said


def take_note(msg):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-notatka.txt"
    with open(file_name, 'w') as file:
        file.write(msg)
        file.close()

    subprocess.Popen(["notepad.exe", file_name])


speak("Witam tu Twój asystent głosowy!")
speak("Co mam zrobić?")

if __name__ == '__main__':
    while True:
        query = get_audio()
        query = query.lower()

        if 'youtube' in query:
            speak('Otwieram YouTube')
            webbrowser.open('www.youtube.com')

        elif 'google' in query:
            speak('Otwieram Google')
            webbrowser.open('www.google.pl')

        elif 'gmail' in query:
            speak('Otwieram Gmaila')
            webbrowser.open('www.gmail.com')

        elif 'onet' in query:
            speak('Otwieram onet')
            webbrowser.open('www.onet.pl')

        #################################################################################
        elif 'co tam' in query or 'jak leci' in query:
            response = ['Spoko', 'W porządku', 'Wszystko dobrze']
            speak(random.choice(response))

        elif 'spać' in query:
            speak('wstrzymuję działanie asystenta')
            while True:
                time.sleep(2)
                call = get_audio()
                if 'obudź się' in call or 'wstawaj' in call:
                    break

        elif 'wyślij' in query or 'messenger' in query or 'chat' in query:
            speak('Uzupełnij dane logowania oraz ID użytkownika/grupy do której chcesz napisać')
            """
            mess_client = Client('', '')
            print(mess_client.isLoggedIn())
            
            # find ID by giving users name as parameter
            # print(mess_client.searchForUsers(''))
            
            while True:
                speak('Co mam wysłać?')
                answer = get_audio()
                mess_client.send(Message(text=answer), thread_id='', thread_type=ThreadType.USER)
                speak('Wysłać ponownie?')
                choice = get_audio()
                if 'tak' in choice:
                    continue
                else:
                    break

            mess_client.logout()
            # print(mess_client.isLoggedIn())
            """

        elif 'szukaj' in query:
            speak('Proszę podaj co mam wyszukać:')
            q = get_audio()
            links_list = []
            for info in search(q, tld='com', lang='pl', num=2, start=0, stop=5,
                               pause=2.0):
                links_list.append(info)
                print(info)
            speak('Który link otworzyć?')
            result = get_audio()
            if 'obojętnie' in result:
                webbrowser.open(random.choice(links_list))
            elif 'pierwszy' in result:
                webbrowser.open(links_list[0])
            else:
                pass

        elif 'zrób notatke' in query or 'zapisz to' in query:
            speak('Co mam zapisać?')
            msg = get_audio().lower()
            take_note(msg)
            speak('Notatka zapisana!')

        elif 'koniec' in query:
            speak('Do zobaczenia!')
            exit()

        else:
            query = query
            speak('Szukam odpowiedzi w Internecie')

            try:
                try:
                    # translation pl -> eng
                    # doesn't work really well
                    # need api-key to work
                    translator = Translator()
                    q = translator.translate(query)
                    print(q.text)
                    res = client.query(q.text)
                    results = next(res.results).text
                    speak('Znalazłem odpowiedź po angielsku:')
                    speak_ENG(results)
                except:
                    wikipedia.set_lang("pl")
                    result = wikipedia.summary(query, sentences=1)
                    speak('Znalazłem odpowiedź na Wikipedii:')
                    speak(result)
            except:
                links_list = []
                speak('Nie znalazłem odpowiedzi, szukam w Google')
                for info in search(query, tld='com', lang='pl', num=2, start=0, stop=5,
                                   pause=2.0):
                    links_list.append(info)
                    print(info)
                if len(links_list) > 0:
                    webbrowser.open(random.choice(links_list))

        speak("Proszę o następną komendę")