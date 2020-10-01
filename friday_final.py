import pyttsx3
import pyaudio    
import pyautogui
import math
import speech_recognition as sr
import datetime   
import operator
import webbrowser
import subprocess 
import time as t
import pyjokes



engine=pyttsx3.init() #initiating the engine
engine.setProperty('rate',150) #set rate of words per min
engine.setProperty('volume',1.0) #set volume 
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


months = ["january", "february", "march", "april", "may", "june","july", "august", "september","october","november", "december"]
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
day_extends = ["rd", "th", "st", "nd"]

#responsive function used to reply to the user,
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def getAudio():
    commands=sr.Recognizer()
    with sr.Microphone() as source:
        commands.pause_threshold=1
        commands.energy_threshold=50
        
        cds=commands.listen(source,timeout=10)
        text=" "

    try:
        text=commands.recognize_google(cds, language="en-UK")
        
        
    except sr.RequestError: speak('Sorry , did you say something?') 
    
    except sr.UnknownValueError: 
        speak('Sorry,I did not get that')
        t.sleep(5)

    except sr.WaitTimeoutError: speak('You did not say anything.Say "Hey Friday" to start!')

    return text

#To set the precedence of operators in multi-operand expressions
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    elif op == '^':
        return 3
    return 0

# Function to perform arithmetic operations. 
def applyingOperations(a, b, op):
    a,b=float(a),float(b)
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b
    if op == '^':
        return a ** b
    if op == '--':
        return b - a

# Function that returns value of 
# expression after evaluation. 
def evaluate(text):
    txt=text
    question="calculate"
    pl="plus"
    mu="multiplied by"
    di="divided by"
    su="subtracted from"
    po=["raised to the power", "to the power", "to the power of","raised to the power of"]

   #replaces values in string 
    if question in txt.lower():
        text=txt.lower().replace(question, "")
    if pl in text:
        text=text.replace(pl,'+')
    if su in text:
        text=text.replace(su, "--")
    if mu  in text:
        text=text.replace(mu,'*')
    if di in text:
        text=text.replace(di, '/')
    for power in po:
        if power in text:
            text=text.replace(power,"^") 
    
    stack = [] #initialize stack using list for numbers
	
    operatorss = []
    """iterates through string and separates numbers and operators
    converts strings to integers and appends to stack list whereas operators are appended to operator list
    checks for paranthesises; removes last 2 values and applies operator function and appends the new value to the stack.
     process is repeated till the end and a value is returned."""
    i = 0 #counter
    while i < len(text):
        if text[i] == ' ':
            i += 1
            continue
        elif text[i] == '(':
            operatorss.append(text[i])
        elif text[i].isdigit():
            val = 0
            
            while (i < len(text) and text[i].isdigit()):
                val = (val * 10) + int(text[i])
                i += 1
            
            stack.append(val)
        elif text[i] == ')':
            
            while len(operatorss) != 0 and operatorss[-1] != '(':
                val2 = stack.pop()
                val1 = stack.pop()
                op = operatorss.pop()
                
                stack.append(applyingOperations(val1, val2, op))
                
            operatorss.pop()
        else:
            
            while (len(operatorss) != 0 and precedence(operatorss[-1]) >= precedence(text[i])):
                val2 = stack.pop()
                val1 = stack.pop()
                op = operatorss.pop()
                
                stack.append(applyingOperations(val1, val2, op))
            
            operatorss.append(text[i])
            
        i += 1
    while len(operatorss) != 0:
        val2 = stack.pop()
        val1 = stack.pop()
        op = operatorss.pop()
        
        stack.append(applyingOperations(val1, val2, op))
    
    return stack[-1] 



def get_date(text):
    txt = text.lower()
    today = datetime.date.today()

    if txt.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in txt.split():
        if word in months:
            month = months.index(word) + 1
        elif word in days:
            day_of_week = days.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in day_extends:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass


    if month < today.month and month != -1:  # if the month mentioned is before the current month set the year to the next
        year = year+1

    if month == -1 and day != -1:  # if we didn't find a month, but we have a day
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    # if we only found a dta of the week
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if txt.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:  
        return datetime.date(month=month, day=day, year=year)


def note(note_text):
    date = datetime.datetime.now()
    file_name = "mynotes.txt"
    with open(file_name, "a+") as f:
        f.write(f"{date}")
        f.write("\n")         
        f.write(note_text)
        f.write("\n")

    subprocess.Popen(["notepad.exe", file_name])
   


def wake(text):

    wake_keys=["ok friday",'okay friday','hey friday']
    text=text.lower()
    for phrase in wake_keys:
        if phrase == text:
            return True

    return False
   



print("Say 'Okay Friday' to wake up")

while True:

    texting=getAudio()
    if wake(texting)==True:
        speak("What can I do for you?")
        text=getAudio()
        print(text)



        NOTE_STRS = ["make a note", "write this down", "remember this","note", "write a note"]
        for phrase4 in NOTE_STRS:
            if phrase4 in text:
                speak("What would you like me to write down?")
                note_text = getAudio()
                print(note_text)
                note(note_text)
                speak("I've made a note of that.")





        date_keys=['what is today','tell me todays date','what is the date','date','what is the date today']
        for phrase3 in date_keys:
            if phrase3 in text:
                dat=get_date(text)
                speak(dat)

        exit_keys=['exit','bye','quit','goodbye','close', "bye bye"]  #Exit the software
        for phrase6 in exit_keys:
            if phrase6 in text.lower(): 
                pyautogui.keyDown('alt')
                pyautogui.press('F4')
                pyautogui.keyUp('alt')
                pyautogui.keyDown('enter')
                pyautogui.keyUp('enter')




        time_keys=['what is the time','tell the time','tell me the time','whats the time','what time is it']
        for phrase5 in time_keys:
            if phrase5 in text:
                time=datetime.datetime.now()
                speak(time.strftime("%H:%M"))

        intro_keys=['hi','hello','hey'] #salutations
        for phrase8 in intro_keys:
            if phrase8 in text.lower():
                speak('Hello, I\'m Friday')    


        id_keys=['what is your name','who are you','what are you known as','what are you called as'] #identifying itself
        for phrase7 in id_keys:
            if phrase7 in text.lower():
                speak('I am your virtual assistant, Friday')



        if 'search' in text.lower(): #search
            srch=text.replace("search ","")
            url = "https://google.com/search?q=" + srch
            webbrowser.get().open(url)
            speak('Here is what i found for '+ srch + ' on google')


        elif "calculate" in text or any((char.isdigit()>1) for char in text): # calculator
            newval=evaluate(text)
            speak(newval)


        elif 'open google' in text.lower(): #open google
            speak("Opening Google")
            webbrowser.open_new_tab("https://www.google.com")




        elif 'open gmail' in text.lower(): #open gmail
            speak("Opening Gmail")
            webbrowser.open_new_tab("https://www.gmail.com")



        elif 'open youtube' in text.lower(): #open youtube
            speak("Opening youtube")
            webbrowser.open_new_tab("https://www.youtube.com")



        elif 'open wikipedia' in text.lower(): #open wikipedia
            speak("Opening wikipedia")
            webbrowser.open_new_tab("https://www.wikipedia.com")



        elif 'how are you' in text.lower(): 
            speak("I am fine, Thank you")   


        elif 'news' in text.lower(): #news
            webbrowser.open_new_tab('https://timesofindia.indiatimes.com/home/headlines')
            speak('Here are some headlines from the Times of India!')


        elif 'show note' in text.lower(): #show notes
            try:
                file=open("mynotes.txt")
                speak(file.read())

            except Exception as e:
                speak("There are no existing notes.")


        elif 'joke' in text.lower():
            speak(pyjokes.get_joke())



        elif 'what are you doing' in text.lower():
            speak('I am currently assisting you with my remarkable capabilities')


        ko=["who is", "where is"]
        for phrase10 in ko:
            if phrase10 in text.lower():
                newtext=text.replace(phrase10,"")
                speak("Searching for"+ newtext)
                webbrowser.open(newtext)


    else:
        continue











    



        

        


    
    