import json
from utils import *
import time
import random
import keyboard
from datetime import date
from nltk.corpus import words as eng_words
from collections import defaultdict
import subprocess

d_file = "data.json"


class Data:

    def __init__(self) -> None:
        self.datafile = d_file

    
    def get_keys(self) -> list[str]:
        with open(self.datafile, 'r') as f:
            self.data = json.load(f)
    
        key = self.data['data'].keys()
        key = list(key)
        
        return key


    def get_words_char(self, char :chr) -> dict:
        with open(self.datafile, 'r') as f:
            self.data = json.load(f)
        
        words = {}
        for k, v in self.data['data'].items() :
            if k[0].lower() == char.lower():
                words[k] = v

        k = words.keys()
        k = list(k)
        random.shuffle(k)    
        words = {x : self.data['data'][x] for x in k}
        
        return words
    

    def get_words_num(self, cnt :int) -> dict:

        with open(self.datafile, 'r') as f:
            self.data = json.load(f)

        key = self.data['data'].keys()
        key = list(key)
        random.shuffle(key)
        key = key[:cnt]
       
        words = {k : self.data['data'][k] for k in key}
        return words


    def get_data(self, char :chr = None, cnt :int = 10) -> dict:
        if char : 
            return self.get_words_char(char = char)

        elif cnt :
            return self.get_words_num(cnt = cnt)

        else:
            return dict()


    def add_data(self, word: str, meaning:str) -> None :
        with open(self.datafile, 'r') as f:
            json_data = json.load(f)

        json_data['data'][word] = meaning

        with open(self.datafile, 'w') as f:
            json.dump(json_data, f, indent=4)


    def get_config(self) -> dict:
        with open(self.datafile, 'r') as f:
            json_data = json.load(f)

        config = json_data["config"]

        return config


    def change_config(self, conf : str, val : str) -> None:
        with open(self.datafile, 'r') as f:
            json_data = json.load(f)

        json_data["config"][conf] = val

        with open(self.datafile, 'w') as f:
            json.dump(json_data, f, indent=4)


class App:

    def __init__(self) -> None:
                   
        self.data_ins = Data()
        self.config = self.data_ins.get_config()
        self.run = True

        for k, v in self.config.items():
            if k.lower() == "libraries" and v.lower() == "false":
                try:
                    print_message("Installing Libraries", color='green')
                    result = subprocess.run(["pip", "install", "-r", "requirements.txt"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print_message("Libraries installed successfully!", color='green')
                        self.data_ins.change_config(k, 'True')
                    else:
                        print_message("Error occurred during installation!", color='red')
                        self.run = False
                        print(result.stderr)

                except Exception as e:
                    print_message("Exception Occured!", color='red')
                    self.run = False
                    print(e)

        if not self.run:
            print_message("Startup Failed!", color='red')
            exit()
            
        while self.run:
            self.data_ins = Data()
            self.home()


    def home(self) -> None:
        self.print_header("home")
        print_message("⭐  Sky's the Limit! ⭐", color='cyan', centered=True)
        print_message("What's the plan? ", color='magenta')
        print_message("1. ", color='orange', end="")
        print_message("Add New Words")
        print_message("2. ", color='orange', end="")
        print_message("Practice Words")
        print_message("3. ", color='orange', end="")
        print_message('Exit')      
        ch = input(""">> """)

        match ch:
            case '1' : 
                self.add_words_page()
            case '2' : 
                self.practice()
            case '3' : 
                print_message("Exiting...", color='red')
                time.sleep(1)
                self.run = False
            case _ :
                print_message("Invalid Choice!", color='red')
                time.sleep(1)
                return

    
    def add_words_page(self) -> None:
     
        data_words = self.data_ins.get_keys()
        data_words = [x.lower() for x in data_words]
        run = True

        while run:
            w = ""
            while not w:
                self.print_header("add_words")
                print_message("Enter 'stop' to quit!", color='magenta')
                w = input("Enter Word : ")
                if w.lower() == 'stop':
                    run = False

                elif not (w.isalpha() and len(w)>1):
                    print_message("Invalid Word!", color='red')
                    w = ""
                    time.sleep(1)
                elif w.lower() not in set(eng_words.words()):
                    print_message(f"{w} is not a valid English Word!", color='red')
                    w = ""
                    time.sleep(1)
                elif w.lower() in data_words:
                    print_message(f"{w} is already in database!", color='red')
                    w = ""
                    time.sleep(1)
            
            if run :
                print_message("Enter 'stop' to skip!", color='magenta')
                m = input(f"Enter Meaning of {w} : ")
                if m.lower() == "stop":
                    continue
                self.data_ins.add_data(word = w, meaning= m)

                print_message("Word Added Successfully!", color='green')
                time.sleep(1)
            
        print_message("Going Back...", color='green')
        time.sleep(1)


    def practice(self) :
        self.print_header("practice")
        print_message("Choose Practice Options :", color='magenta')
        print_message("1. ", color='orange', end="")
        print_message("Practice Random Words")
        print_message("2. ", color='orange', end="")
        print_message("Practice Alphabetically")
        print_message("3. ", color='orange', end="")
        print_message('Back')
        ch = input(""">> """)

        match ch:
            case '1' :
                self.practice_page(count=True)
            case '2' :
                self.practice_page(alpha=True)
            case '3' :
                print_message("Going Back ...", color='green')
                time.sleep(1)
                return
            case _ :
                print_message("Invalid Choice!", color='red')
                time.sleep(1)
                self.practice()
        
        return 


    def practice_page(self, alpha : bool = False, count :bool = False) -> None :

        def get_alpha_dict():
            data_words = self.data_ins.get_keys()
            data_words = list(data_words)
            data_words = [x.lower() for x in data_words]  

            alpha_dict = dict()

            for w in data_words:
                occ = alpha_dict.get(w[0])
                if not occ : 
                    occ = 0
                alpha_dict[w[0]] = occ + 1

            return alpha_dict

        words = dict()

        if count : 
            cnt = ""
            while not cnt:
                self.print_header("practice")
                print_message("Enter 'stop' to exit!", color='magenta')
                print_message("Enter The Count (10 - 50) :", color='magenta')
                cnt = input(""">> """)
                if cnt.lower() == 'stop':
                    return
                if not (cnt.isdigit() and int(cnt) >= 10 and int(cnt) <= 50) :
                    print_message("Invalid Choice!", color='red')
                    time.sleep(1)
                    cnt = ""
            words = self.data_ins.get_data(cnt = int(cnt))

        elif alpha:
            char = ""
            while not char:
                self.print_header("practice")

                alphabets = [chr(ord('a') + i) for i in range(26)]

                alpha_dict = get_alpha_dict()

                for a in alphabets:
                    print_message(f"{a.upper()} ", color='orange', end= "")
                    occ = alpha_dict.get(a)
                    if not occ:
                        occ = 0
                    print(f" : {occ}")
                
                print_message("Enter 'stop' to exit!", color='magenta')
                print_message("Enter The Character (a-z) :", color='magenta')
                
                char = input(""">> """) 
                
                if char.lower() == 'stop':
                    return

                if not (char.isalpha() and len(char) == 1):
                    print_message("Invalid Choice!", color='red')
                    time.sleep(1)
                    char = ""
                elif not alpha_dict.get(char):
                    print_message(f"Character {char} has Zero Words!", color='red')
                    time.sleep(1)
                    char = ""
                
            
            words = self.data_ins.get_data(char = char)

        self.print_instructions()

        self.test_page(words = words)
    

    def print_instructions(self) -> None:
        self.print_header("inst")  
        print_message("Please read all the instructions carefully before proceeding!", color='red')
        print("** Please use the Right Arrow key to move on to the next word.")
        print("** If there is any word that you could not answer, press the Up Arrow key to mark it.")

        print_message("Press Right Arrow Key to continue -->", color='magenta')
        keyboard.wait("right")

        keyboard.unhook_all()
    

    def test_page(self, words :dict) -> None:
        
        unsolved = []
        c = 0
        
        def markUnsolved(e, w):
            if w not in unsolved:
                unsolved.append(w)
            print_message("Marked Unsolved!", color='green')

        def report() :
            self.print_header('report')  
            
            skipped = len(words)- c
            answered = len(words) - (len(unsolved) + skipped)
            percent = ((answered/len(words))*100)
            print_message("Total Words : ", color='orange', end = "")
            print_message(f"{len(words)}")

            print_message("Questions Answered: ", color='orange', end = "")
            print_message(f"{answered}")

            print_message("Questions Skipped: ", color='orange', end = "")
            print_message(f"{skipped}")
                
            print_message("Questions Unanswered: ", color='orange', end = "")
            print_message(f"{len(unsolved)}")

            print_message("Final Score: ", color='green', end = "")
            print_message(f"{answered} out of {len(words)}")

            print_message("Percentage : ", color='green', end = "")
            print_message(f"{percent:.2F}%")

            print()
            print()   
            if unsolved:  
                print_message("Unanswered Words : ", color='magenta')

                for w in unsolved:
                    print_message(f"{w} ", color='cyan', end="")
                    spaces = 15 - len(w)
                    print_message(" " * spaces + f" :  {words[w]}")
                
                print()
                print()    

            print_message("Press ESC to exit --> ", color='magenta', end = "")
            keyboard.wait('esc')
                
        try : 
            for w in words.keys():
                self.print_header("test_page")
                print_message(f"{w}", color='orange', centered=True)
                for _ in range(10):
                    print()

                print_message("Right Arrow : Next Words      ",color='magenta', centered=True)
                print_message("Up Arrow    : Mark as Unsolved",color='magenta', centered=True)
                print_message("Ctrl + C    : Quit            ",color='magenta', centered=True)
                
                keyboard.block_key('c')
                talk(w)
                keyboard.unblock_key('c')

                keyboard.on_press_key('up', lambda event, val = w : markUnsolved(event, val))
                keyboard.wait('right')
                
                self.print_header("test_page")
                print_message(f"{w}", color= 'orange', centered=True)
                print_message(f"{words[w]} ", centered=True, color='white')

                for _ in range(10):
                    print()
                
                print_message("Right Arrow : Next Words      ",color='magenta', centered=True)
                print_message("Up Arrow    : Mark as Unsolved",color='magenta', centered=True)
                print_message("Ctrl + C    : Quit            ",color='magenta', centered=True)
                
                keyboard.wait('right')
                keyboard.unhook_all()

                c += 1

        except KeyboardInterrupt as e:
            self.print_header("test_page")
            print_message("Quitting...", color='red', centered=True)
            keyboard.unhook_all()
            time.sleep(1)
                
        report()


    def print_header(self, loc : str, text : str = None) : 
        commands = {
            "home" :  lambda : print_message("🚀  Welcome to \"VocaBuilder\" - Your English Tutuor 🚀", color="magenta", centered=True),
            "add_words" : lambda : print_message("⭐ Add Words ⭐", color="blue", centered=True),
            "practice" : lambda : print_message("⭐ Make A Choice ⭐", color='blue', centered=True),
            "inst" : lambda : print_message("🔴 Instructions 🔴", color='red',centered=True),
            "interview" : lambda : print_message("⭐ Give Your Best! ⭐",color="blue", centered=True),
            "test_page" : lambda : print_message(f"⭐ Give Your Best! ⭐", color='green', centered=True),
            "report" : lambda : print_message(f"Performance Report : {date.today()}", color='green', centered=True)
        }
        clear()
        print_br()
        commands[loc]()
        print_br()


if __name__ == '__main__':
    app = App()