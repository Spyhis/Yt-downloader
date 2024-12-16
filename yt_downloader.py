import yt_dlp 
import os
from tkinter import *
from pyperclip import paste
from time import sleep
import threading
from tkinter import ttk
import sqlite3
from tkinter import filedialog
from tkinter import messagebox
con = sqlite3.connect("ytsave.db")
cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS ytsaving (directory TEXT, kontrol INT, language TEXT)")
con.commit()

window = Tk()
window.geometry("1030x720")
window.resizable(False,False)
window.config(border=0)
window.config(bg="white")


dosya = ["{}:\\".format(i) for i in "ABCDEFGHJIJKLMNOPRSTUVYZXQ" if os.path.exists("{}:\\".format(i)) and os.path.isdir("{}:\\".format(i))]

def save():
    cursor.execute("Select * From ytsaving where kontrol = ?", (1,))
    liste = cursor.fetchall()
    if len(liste)!= 0:
        lambda:None
    if len(liste)== 0:
        try:
            cursor.execute("Insert into ytsaving Values(?,?,?)", (os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), 1, "English"))
            con.commit()

        except:
            cursor.execute("Insert into ytsaving Values(?,?,?)", (os.path.join(dosya[0]),1, "English"))
            con.commit()
            
save()

cursor.execute("Select directory From ytsaving")
listee = cursor.fetchall()
i = "".join(listee[0])


mp4 = PhotoImage(file="mp4.png")
mp3 = PhotoImage(file="mp3.png")
webm = PhotoImage(file="webm.png")
setting = PhotoImage(file="settings.png")

label = Label(window, text="Please Paste Youtube Link", fg="black", font="Thunderbolt", bg="white")
label.place(x= 50, y=20)

link = ttk.Entry(window, width=44, font=(25),  background="#e3e1e1", )
link.place(x=55, y= 55)



title = Label(window, text="", fg="black", bg="white")
title1 = Label(window, text="", fg="black", bg="white")
title2 = Label(window, text="", fg="black", bg="white")
title.place(x= 600, y=60)
title1.place(x= 600, y=80)
title2.place(x= 600, y=100)

opt = Label(window, fg="black", font=("Thunderbolt", 15), bg="white" )
opt.place(x=50, y=330) 

frame = Frame(window, width=430, height=720, bg="#e3e1e1",)
frame.place(x= 1030)
frame1 = Frame(window, width=430, height=720, bg="#e3e1e1",)
frame1.place(x= 1570)

a = Label(frame, text="", bg="#e3e1e1", height=720, width=570 ).pack()
a = Label(frame1, text="", bg="white", height=720, width=430 ).pack()
b = Label(window, text="Select the directory where you want the video to be installed: ", bg="#e3e1e1")
b.place(x= 1040, y=30)

direc = Entry(window, width=80, border=0, state=NORMAL)
direc.place(x=1040, y=60)
direc.insert(END, i)
direc.config(state=DISABLED)

var = IntVar()
titlescontrol = 0
def languageT():
    cursor.execute("Update ytsaving set language = ? where language = ?",("Turkish", "English"))
    con.commit()
    label.config(text="Lütfen Youtube Bağlantısını Yapıştırın")
    b.config(text="Videonun yüklenmesini istediğiniz dizini seçin: ")
    language.config(text="Türkçe")
    languagee.config(text="İngilizce")
    file.config(text="Seç")
    delpas.config(text="Sil")
    pas.config(text="Yapıştır")
    labellangu.config(text="Diller: ")
    if titlescontrol == 1:
        title.config(text=f"Başlık: {titleL}")
        title1.config(text=f"Süre: {title1L}")
        title2.config(text=f"Çözünürlük: {title2L}")
        opt.config(text="Yükleme Seçenekleri:")
    if titlescontrol == 0:
        lambda:None
def languageEn():
    cursor.execute("Update ytsaving set language = ? where language = ?",("English", "Turkish"))
    con.commit()
    label.config(text="Please Paste Youtube Link")
    b.config(text="Select the directory where you want the video to be installed: ")
    language.config(text="Turkish")
    languagee.config(text="English")
    file.config(text="Select")
    delpas.config(text="Delete")
    pas.config(text="Paste")
    labellangu.config(text="Languages: ")
    if titlescontrol == 1:
        title.config(text=f"Title: {titleL}")
        title1.config(text=f"Duration: {title1L}")
        title2.config(text=f"Resolution: {title2L}")
        opt.config(text="Download Settings:")
    if titlescontrol == 0:
        lambda:None

language = Radiobutton(window, text="Turkish",bg="#e3e1e1",activebackground="#e3e1e1",fg="black",variable=var, value=1, command=languageT)
language.place(anchor=W, x=1050, y=150)
languagee = Radiobutton(window, text="English", bg="#e3e1e1",activebackground="#e3e1e1",fg="black", variable=var, value=0, command=languageEn)
languagee.place(anchor=W, x=1050, y=180)
labellangu = Label(window, text="Languages: ", bg="#e3e1e1")
labellangu.place(x= 1040, y=120)

downlabel = Label(window,bg="white",)
downlabel.place(x=1600,y=100)


def my_hook(d):
    downlabel.config(text="Video Is Preparing To Download")
    if d['status'] == 'finished':
        downlabel.config(text="Download Completed, Now Converting")
    elif d['status'] == 'downloading':
        downlabel.config(text=f"Downloading: {d['filename']} - {d['_percent_str']} complete")

ydl = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': direc.get()+'/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'noplaylist':True
}


def downloadmp4():

    links = link.get()
    ydl = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': direc.get()+'/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'noplaylist':True
    }

    try:
        with yt_dlp.YoutubeDL(ydl) as ydll:
            ydll.download([links])
    except:
        messagebox.showerror("Hata", "Hatalı indirme")
        link.delete(0, END)


def downloadmp3():
    links = link.get()
    ydl = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': direc.get()+'/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'noplaylist':True
    }

    try:  

        with yt_dlp.YoutubeDL(ydl) as ydll:
            ydll.download([links])
    except:
        messagebox.showerror("Hata", "Hatalı indirme")
        link.delete(0, END)
        
def downloadwebm():

    links = link.get()
    ydl = {
        'format': 'bestvideo+bestaudio/bestvideo/best',
        'outtmpl': direc.get()+'/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'noplaylist':True
    }
    try: 

        with yt_dlp.YoutubeDL(ydl) as ydll:
            ydll.download([links])
    except:
        messagebox.showerror("Hata", "Hatalı indirme")
        link.delete(0, END)

def filee():
    global filename
    files = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    cursor.execute("Select directory From ytsaving")
    l = cursor.fetchall()
    olddirec = "".join(l[0])
    filename = filedialog.askdirectory()
    direc.config(state=NORMAL)
    direc.delete(0, END)
    if filename == "":
        direc.config(state= NORMAL)
        try:
            cursor.execute("Update ytsaving set directory = ? where directory = ?",(files, olddirec))
            con.commit()
            direc.insert(END,os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        except:
            dosya = ["{}:\\".format(i) for i in "ABCDEFGHJIJKLMNOPRSTUVYZXQ" if os.path.exists("{}:\\".format(i)) and os.path.isdir("{}:\\".format(i))]
            direc.insert(END, os.path.join(dosya[0]))
            cursor.execute("Update ytsaving set directory = ? where directory = ?",(os.path.join(dosya[0]), olddirec))
            con.commit()
        direc.config(state= DISABLED)
    else:
        direc.insert(END,filename)
        cursor.execute("Update ytsaving set directory = ? where directory = ?",(filename, olddirec))
        con.commit()
        direc.config(state=DISABLED)

file = Button(window, text="Select", command=filee)
file.place(x=1540, y=60)

button = True
def option():
    global button
    if button == True:
        window.geometry("1570x720")
        button = False
    else:
        window.geometry("1030x720")
        button = True
mp4button = Button(window, border=0, bg="white", activebackground="white", state=DISABLED, command=downloadmp4)
mp4button.place(x= 100, y=400)

mp3button = Button(window, border=0, bg="white", activebackground="white", state=DISABLED, command=downloadmp3)
mp3button.place(x= 240, y=400)

webmbutton = Button(window, image=webm, border=0, bg="white", activebackground="white", state=DISABLED, command=downloadwebm)
webmbutton.place(x= 380, y=400)

settingss = Button(window, image=setting, border=0, bg= "white", activebackground="white", command=option)
settingss.place(x=7, y=10)


def past():
    result = paste()
    link.insert(0, result)
def dele():
    link.delete(0, END)
def delandpast():
    dele()
    past()
delpas = Button(window, text="Delete", command=dele, font=("Thunderbolt", 10), bg="white")
delpas.place(x=480, y=60)
pas = Button(window, text="Paste", command=past,font=("Thunderbolt", 10), bg="white")
pas.place(x=480, y= 30)
titleL = ""
title1L = ""
title2L = ""
cursor.execute("Select language From ytsaving")
lannn = cursor.fetchall()
def main():
    global title1L
    global title2L
    global titleL
    global titlescontrol
    lang = "".join(lannn[0])
    links = link.get()
    number = len(links)
    if number>0:
        try:
            delpas.config(state=DISABLED)
            pas.config(state=DISABLED)
            with yt_dlp.YoutubeDL(ydl) as ydll:
                info = ydll.extract_info(links, download=False)
                if info["duration"]/3600 <1:
                    min = info["duration"]//60
                    sec = info["duration"]%60
                    if lang == "English":
                        title1.config(text=f"Duration: {min:02d}:{sec:02d}")
                    elif lang == "Turkish":
                        title1.config(text=f"Süre: {min:02d}:{sec:02d}")
                    title1L = f"{min:02d}:{sec:02d}"
                if info["duration"]/3600 >=1:
                    hour = info["duration"]//3600
                    a = info["duration"]- hour*3600
                    min = a//60
                    sec = a%60
                    if lang == "English":
                        title1.config(text=f"Duration: {hour:02d}:{min:02d}:{sec:02d}")
                    elif lang == "Turkish":
                        title1.config(text=f"Süre: {hour:02d}:{min:02d}:{sec:02d}")
                    title1L = f"{hour:02d}:{min:02d}:{sec:02d}"
                if lang == "English":
                    title.config(text=f"Title: {info["title"]}")
                    title2.config(text=f"Resolution: {info["height"]}P")
                    opt.config(text="Download Options:")
                elif lang == "Turkish":
                    title.config(text=f"Başlık: {info["title"]}")
                    title2.config(text=f"Çözünürlük: {info["height"]}P")
                    opt.config(text="Yükleme Seçenekleri:")
                titlescontrol = 1
                titleL = f"{info["title"]}"
                title2L = f"{info["height"]}P"
                mp4button.config(image=mp4, state=ACTIVE)
                mp3button.config(image=mp3, state=ACTIVE)
                webmbutton.config(image= webm, state=ACTIVE)
                delpas.config(state=NORMAL)
                pas.config(state=NORMAL)
        except:
            messagebox.showerror("Hata", "Hatalı Link")
            link.delete(0, END)
            delpas.config(state=NORMAL)
            pas.config(state=NORMAL)
    else:
        lambda:None

numbe = 0
def hece():
    global numbe
    while True:
        links = link.get()
        numbe = len(links)
        sleep(3)
a = threading.Thread(target=hece, daemon=True)
a.start()

numb = 0 
def heces():
    global titlescontrol
    global numb
    while True:
        links = link.get()
        numb = len(links)
        sleep(0.5)
        if numb == 0:
            titlescontrol = 0
he = threading.Thread(target=heces, daemon=True)
he.start()

def control():
    while True:
        if numb == 0:
            title.config(text="")
            title1.config(text="")
            title2.config(text="")
            webmbutton.config(image="",state=DISABLED)
            mp4button.config(image="", state=DISABLED)
            mp3button.config(image="", state=DISABLED)
            opt.config(text="")
        while numbe == 0:
            delpas.config(state=NORMAL)
            pas.config(state=NORMAL)
            main()
            sleep(1)
t = threading.Thread(target=control, daemon=True)
t.start()

def langu():
    cursor.execute("Select language From ytsaving")
    lan = cursor.fetchall()
    lang = "".join(lan[0])
    if lang == "English":
        languagee.config(value=0)
        language.config(value=1)
        languageEn()
    elif lang == "Turkish":
        languagee.config(value=1)
        language.config(value=0)
        languageT()
langu()
window.mainloop()
