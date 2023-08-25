import time
import playsound

def play_answer(text = 'you fucking cunt'):
    language = "pl"
    
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("output.mp3")
    print('output saved') 
    time.sleep(0.5)
    playsound('output.mp3')