from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import openai
import time
import os
import apis
import utils
import communication

### some important things ###
openai.api_key = apis.openai_key
MESSAGES = []
MESSAGES.append({"role": "system", "content": "You are a cool assistant dude. You are a bit sarcastic, use strong language and have your own opinions on user's actions. "})




def record():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            # I don't know what it does but apparently you have to do it
            recognizer.adjust_for_ambient_noise(source)
            # listen for audio
            print("Listening...")
            audio = recognizer.listen(source)
            # try to recognize the speech using Google Web Speech API
            try:
                print("Recognizing...")
                text = recognizer.recognize_google(audio, language="pl")
                # print the recognized text
                print("You said: " + text)
                return text
            # errors bad
            except sr.UnknownValueError:
                play_answer("Sorry, I could not understand what you said.")
                MESSAGES.append({"role": "assistant", "content": "Sorry, I could not understand what you said."})
            except sr.RequestError as e:
                play_answer("Could not request results from Google Web Speech API; {0}".format(e))


def get_ai_answer(input):
    output = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = MESSAGES,
        temperature=0.8,
        max_tokens=1000,
        frequency_penalty=0.0
    )['choices'][0]['message']['content']
    MESSAGES.append({"role": "assistant", "content": output})

    print(f"The AI answers: {output}")

    return output


def main():
    while True:
        user_text = record()
        MESSAGES.append({"role": "user", "content": user_text})
        ai_answer = get_ai_answer(user_text)
        play_answer(ai_answer)
        print(f'MESSAGES: \n {MESSAGES}')
        os.remove('output.mp3')

main()