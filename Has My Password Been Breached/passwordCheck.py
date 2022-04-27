import hashlib
import tkinter
import tkinter.messagebox
from hashlib import sha1
from tkinter import *
from tkinter import filedialog

try: 
    import requests
except ModuleNotFoundError:
    tkinter.messagebox.showerror(title='Missing Module!', text="You are missing the: requests module.")
    raise

def pwned_API_query(user_input):
    sha1hash = hashlib.sha1(user_input.encode('utf-8')).hexdigest().upper()
    first_five = sha1hash[:5] #First 5 indicies in the Hash
    last_five = sha1hash[5:] #Last 5 indicies in the Hash
    api_url = 'https://api.pwnedpasswords.com/range/' + first_five #Parsing the first five 
    #print(api_response)
    api_response = requests.get(api_url) #API Reponse Code
    #print(api_response)
    hashes = (line.split(':') for line in api_response.text.splitlines())
    #print(hashes)
    num_breaches = next((int(num_breaches) for t, num_breaches in hashes if t == last_five), 0)
    #print (num_breaches)
    return sha1hash, num_breaches

def password_check(password_input):
    string_password = password_input.strip()
    finalHash, num_breaches = pwned_API_query(string_password)
    if num_breaches:
        foundmsg = "Password Entered: {0}\nThis was found in {1} different occurances!\n\nThe Hash is: {2}\n\nIf you are using this password, it is highly recommended to change your password now!"
        badalert = foundmsg.format(string_password, num_breaches, finalHash)
        tkinter.messagebox.showerror(title='Password Has Been Breached!',message=badalert)
    else:
        safemsg = "Password Entered: {}\n\nThis password was not found in the database and is deemed safe."
        safealert = safemsg.format(string_password)
        tkinter.messagebox.showinfo(title='Password Not Found!',message=safealert)
    return

def on_submit_button():
    toCheck = entryText.get()
    password_check(toCheck)

def read_file_content():
    filetypes = (
        ('text files', '*.txt'),
    )

    file_name = filedialog.askopenfilename(
        title='Load A File To Check Passwords',
        initialdir='./',
        filetypes=filetypes)
    
    file_object = open(file_name)
    all_text = file_object.readlines()
    for individual in range(len(all_text)):
        password_check(all_text[individual])

gui = Tk() #Initiate Tk GUI
gui.geometry("400x200")
gui.resizable(False, False)
gui.title("Have I Been Pwned Checker")
gui.config(background="black")

firstLabel = Label(gui, 
                text="To find out if a password,\n in plaintext form, has ever been\n breached before, enter it below:", 
                font=('Arial', 15, 'bold'), 
                fg='white', 
                bg='black',
                relief=RAISED,
                bd=10)

entryText = Entry(gui,
                font=("Arial",15))

submitButton = Button(gui,
                text="Submit",
                command=on_submit_button,
                font=("Arial", 15))

openFile = Button(gui,
                text='Open A Text File',
                font=("Arial", 15),
                command=read_file_content)

firstLabel.pack()
entryText.pack()
submitButton.pack()
openFile.pack()
gui.mainloop()
