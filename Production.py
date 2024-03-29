
import re
import ffmpeg as fm
from PIL import Image
from requests import *
from datetime import date
from pytube import YouTube
import customtkinter as Ctk
from threading import Thread
from bs4 import BeautifulSoup
from tkinter import StringVar
from os import readlink, remove
from pytube.exceptions import *
from time import strftime, localtime

# prevent IDE from removing unused imports
_ = re, StringVar, fm, YouTube, Image, readlink, remove, date, Ctk, strftime, localtime, BeautifulSoup

Ctk.set_appearance_mode('dark')
Ctk.set_default_color_theme('green')


def video_Combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

def audio_Combobox_callback(choice):
    print("combobox dropdown clicked:", choice)

def videoFormat_Combobox_callback(choice):
    print("combobox dropdown clicked:", choice)


class App(Ctk.CTk):

    def __init__(self):

        super().__init__()

        self.resizable(False, 0)            # type: ignore
        self.title("Video Downloader")

        self.root0Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color="gray84", height=100)
        self.root0Frame.grid(row=0, column=0, sticky=Ctk.NSEW, padx=10, pady=(10, 5))

        self.root1Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color="gray84", height=100)
        self.root1Frame.grid(row=1, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 5))

        self.root2Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color="gray84", height=100)
        self.root2Frame.grid(row=2, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 10))

        self.URLLabel = Ctk.CTkLabel(self.root0Frame, width=23, height=20, text="URL", fg_color="#71C5E8", corner_radius=6)
        self.URLLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.entryURL = Ctk.CTkEntry(self.root0Frame, placeholder_text="Copy the URL here", text_color="#19222B", font=Ctk.CTkFont(size=12, weight="normal", slant="italic"), width=200, height=34, corner_radius=6, fg_color="#EBBDD1")
        self.entryURL.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky=Ctk.NSEW)
        self.entryURL.bind("<Return>", self.readURL)

        self.clearButton = Ctk.CTkButton(self.root0Frame, text="x", width=24, text_color="gray10", bg_color="transparent", fg_color="gray84", hover_color="gray78", command=self.clearUrl)
        self.clearButton.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky=Ctk.NSEW)

        self.titleLabel = Ctk.CTkLabel(self.root1Frame, width=23, height=20, text="Title:", fg_color="#71C5E8", corner_radius=6)
        self.titleLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.autorLabel = Ctk.CTkLabel(self.root1Frame, width=23, height=20, text="Autor:", fg_color="#71C5E8", corner_radius=6)
        self.autorLabel.grid(row=1, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.parametersTabview = Ctk.CTkTabview(self.root1Frame, height=40, anchor="NW")
        self.parametersTabview.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), columnspan=3, sticky="nsew")
        self.parametersTabview.add("Set Quality")

        self.videoCombobox_var = Ctk.StringVar()
        self.videoItag = []
        self.videoCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), values=self.videoItag, width=80,command=video_Combobox_callback, variable=self.videoCombobox_var)
        self.videoCombobox.grid(row=0, column=0, padx=(5, 5), pady=(5, 10), sticky=Ctk.W)
        self.videoCombobox_var.set("Video")

        self.audioCombobox_var = Ctk.StringVar()
        self.showAudioItag = []
        self.audioCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), values=self.showAudioItag, width=80, command=audio_Combobox_callback, variable=self.audioCombobox_var)
        self.audioCombobox.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky=Ctk.N)
        self.audioCombobox_var.set("Audio")

        self.videoFormatCombobox_var = Ctk.StringVar()
        self.videoFormatItag = [".mp3", ".mp4", ".avi", ".mkv"]
        self.videoFormatCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), width=80, values=self.videoFormatItag, command=videoFormat_Combobox_callback, variable=self.videoFormatCombobox_var)
        self.videoFormatCombobox.grid(row=0, column=2, padx=(5, 5), pady=(5, 10), sticky=Ctk.E)
        self.videoFormatCombobox_var.set("format")
        
        self.titleTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.titleTextbox.grid(row=0, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")
        self.titleTextbox.configure(state="readonly")

        self.autorTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.autorTextbox.grid(row=1, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")
        self.autorTextbox.configure(state="readonly")
        
        self.durationLabel = Ctk.CTkLabel(master=self.root1Frame, text="" ,font=Ctk.CTkFont(size=12, weight="normal", slant="roman"), width=23, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.durationLabel.grid(row=0, column=2, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.videoIcon = Ctk.CTkImage(light_image=Image.open(fp='./Icons/Video_Icon.png'), size=(100,100))
        self.downloadIcon = Ctk.CTkImage(light_image=Image.open(fp='./Icons/Download_Icon.png'), size=(30,30))

        self.videoImage = Ctk.CTkLabel(self.root2Frame, text='', compound="center", image=self.videoIcon, fg_color='#ff0')
        self.videoImage.grid(row=0, column=0, padx=(5, 10), pady=(5, 5), sticky="e")

        self.setPathButton = Ctk.CTkButton(master=self.root2Frame, width=30, height=36, text="Set Folder", fg_color='#ff0', command=self.setPath)
        self.setPathButton.grid(row=0, column=1, padx=(5, 10), pady=(5, 5), sticky="w")

        self.downloadVideo = Ctk.CTkButton(master=self.root2Frame, width=30, height=36, text="", image=self.downloadIcon, fg_color='#ff0')
        self.downloadVideo.grid(row=0, column=2, padx=(5, 10), pady=(5, 5), sticky="w")

    def clearUrl(self):

        self.titleTextbox.configure(state="normal")
        self.autorTextbox.configure(state="normal")

        duration = StringVar()
        duration.set("  ")

        self.entryURL.delete(0, Ctk.END)
        self.titleTextbox.delete(0, Ctk.END)
        self.autorTextbox.delete(0, Ctk.END)
        self.durationLabel.configure(textvariable=duration)

        self.titleTextbox.configure(state="readonly")
        self.autorTextbox.configure(state="readonly")

        self.videoCombobox_var.set("Video")
        self.audioCombobox_var.set("Audio")
        self.videoFormatCombobox_var.set("format")

        self.videoCombobox.configure(values=[])
        self.audioCombobox.configure(values=[])
        self.videoFormatCombobox.configure(values=[])

        self.entryURL._placeholder_text_active = True

    def readURL(self, event):

        readLink = self.entryURL.get()

        try:
            self.yt = YouTube(readLink)

        except VideoUnavailable:

            print(f' - Video {readLink} is unavaialable, skipping.')

        else:

            self.showInf(self.yt)
            self.filterAudioInf(self.yt)
            self.filterVideoInf(self.yt)
            self.getVideoThumbnail(self.yt)

            print(self.yt.length)

        print(readLink)

    def showInf(self, yt):

        self.title = StringVar()
        self.autor = StringVar()
        self.duration = StringVar()

        self.title.set(yt.title)
        self.autor.set(yt.author)
        self.duration.set(yt.length)

        self.titleTextbox.configure(textvariable=self.title)
        self.autorTextbox.configure(textvariable=self.autor)
        self.durationLabel.configure(textvariable=self.duration)


    def filterAudioInf(self, yt):

        re.purge()
        audioStr, audioItag, audioAbr, audioData = [], [], [], []

        # stream retorna StreamQuery
        audioStr = str(yt.streams.filter(only_audio=True))

        audioItag = re.findall(pattern=r'itag="(\d+)"', string=audioStr)
        audioAbr = re.findall(pattern=r'abr="(\d+[A-z]{1,})"', string=audioStr)

        audioData = dict(zip(audioItag, audioAbr, strict=True))

        self.audioCombobox.configure(**{"values": audioAbr})
        self.audioCombobox_var.set("Audio")

        #audioList = audioStr

        print("\n******************************************************")
        print(audioItag)
        print(audioAbr)
        print(audioData)


    def filterVideoInf(self, yt):

        re.purge()
        videoStr, videoItag, videoRes, videoData = [], [], [], []

        # stream retorna StreamQuery
        videoStr = str(yt.streams.filter(only_video=True))

        videoItag = re.findall(pattern=r'itag="(\d+)"', string=videoStr)
        videoRes = re.findall(pattern=r'res="(\d+[A-z]{1,})"', string=videoStr)

        videoData = dict(zip(videoItag, videoRes, strict=True))

        self.videoCombobox.configure(**{"values": videoRes})
        self.videoCombobox_var.set("Video")

        print(videoItag)
        print(videoRes)
        print(videoData)
        print("******************************************************\n")


    def getVideoThumbnail(self, yt):
        
        urlImage = yt.thumbnail_url

        response = get(urlImage)

        if response.status_code == 200:
            with open('C:/Users/Daniel/Desktop/thumbnail.jpg', 'wb') as file:
                file.write(response.content)

        print("Image: " + urlImage)

        # open and load de images for displays it in GUI
        thumbnail = Image.open(fp='C:/Users/Daniel/Desktop/thumbnail.jpg')
        showThumbnail = Ctk.CTkImage(light_image=thumbnail, size=(thumbnail.width*(.3), thumbnail.height*(.3)))
        self.videoImage.configure(image=showThumbnail)


    def setPath(self, **kwargs):

        self.pathSet = None
        self.pathSet = Ctk.filedialog.askdirectory()
        print(self.pathSet)


if __name__ == '__main__':
    app = App()
    app.mainloop()



#https://docs.python.org/es/3/library/re.html
#https://docs.python.org/es/3/library/functions.html#zip
#["blue", "green", "dark-blue", "sweetkind"]

#audioListSlice = re.split(pattern='>, <', string=audioStr)
#audioList = re.findall(pattern=r'([A-z]{4})="(\d+)"', string=audioStr)
#audioList = re.findall(pattern=r'(itag="(\d+)")', string=audioStr)
#audioList = re.findall(pattern='itag=[0-9]*', string=audioStr)
#audioList = re.findall(pattern=r'(itag="[0-9]*")', string=audioStr)
