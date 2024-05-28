
import re
import threading
import ffmpeg as fm
from PIL import Image
from requests import *
from datetime import date
from pytube import YouTube
import customtkinter as Ctk
from threading import Thread
from bs4 import BeautifulSoup
from tkinter import StringVar
from collections import Counter
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
        self.entryURL.bind("<Return>", self.clickEvent)

        self.clearButton = Ctk.CTkButton(self.root0Frame, text="x", width=24, text_color="gray10", bg_color="transparent", fg_color="gray84", hover_color="gray78", command=self.clearUrl)
        self.clearButton.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky=Ctk.NSEW)

        self.titleLabel = Ctk.CTkLabel(self.root1Frame, width=23, height=20, text="Title:", fg_color="#71C5E8", corner_radius=6)
        self.titleLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.titleTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.titleTextbox.grid(row=0, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")
        self.titleTextbox.configure(state="readonly")
        
        self.durationLabel = Ctk.CTkLabel(master=self.root1Frame, text="" ,font=Ctk.CTkFont(size=12, weight="normal", slant="roman"), width=23, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.durationLabel.grid(row=0, column=2, padx=(5, 10), pady=(5, 5), sticky="nsew")

        self.autorLabel = Ctk.CTkLabel(self.root1Frame, width=23, height=20, text="Autor:", fg_color="#71C5E8", corner_radius=6)
        self.autorLabel.grid(row=1, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.autorTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=20, corner_radius=6, fg_color="gray78", text_color="#000000")
        self.autorTextbox.grid(row=1, column=1, padx=(5, 10), pady=(5, 5), sticky="nsew")
        self.autorTextbox.configure(state="readonly")

        self.setPathButton = Ctk.CTkButton(master=self.root1Frame, width=30, height=36, text="Set Folder", fg_color='#ff0', command=self.setPath)
        self.setPathButton.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky="w")

        self.downloadIcon = Ctk.CTkImage(light_image=Image.open(fp='./Icons/Download_Icon.png'), size=(30,30))

        self.downloadVideo = Ctk.CTkButton(master=self.root1Frame, width=30, height=36, text="", image=self.downloadIcon, fg_color='#ff0', command=self.saveFile)
        self.downloadVideo.configure(state="disabled")
        self.downloadVideo.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky="e")

        self.parametersTabview = Ctk.CTkTabview(self.root1Frame, height=40, anchor="NW")
        self.parametersTabview.grid(row=3, column=0, padx=(10, 10), pady=(10, 5), columnspan=3, sticky="nsew")
        self.parametersTabview.add("Set Quality")

        self.videoCombobox_var = Ctk.StringVar()
        self.videoItag = []
        self.videoCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), values=self.videoItag, width=80,command=video_Combobox_callback, variable=self.videoCombobox_var)
        self.videoCombobox.grid(row=0, column=0, padx=(5, 5), pady=(5, 10), sticky=Ctk.W)
        self.videoCombobox.configure(state="disabled")
        self.videoCombobox_var.set("Video")

        self.audioCombobox_var = Ctk.StringVar()
        self.showAudioItag = []
        self.audioCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), values=self.showAudioItag, width=80, command=audio_Combobox_callback, variable=self.audioCombobox_var)
        self.audioCombobox.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky=Ctk.N)
        self.audioCombobox.configure(state="disabled")
        self.audioCombobox_var.set("Audio")

        self.videoFormatCombobox_var = Ctk.StringVar()
        self.videoFormatItag = [".mp3", ".mp4", ".avi", ".mkv"]
        self.videoFormatCombobox = Ctk.CTkComboBox(self.parametersTabview.tab("Set Quality"), width=80, values=self.videoFormatItag, command=videoFormat_Combobox_callback, variable=self.videoFormatCombobox_var)
        self.videoFormatCombobox.grid(row=0, column=2, padx=(5, 5), pady=(5, 10), sticky=Ctk.E)
        self.videoFormatCombobox.configure(state="readonly")
        self.videoFormatCombobox_var.set("format")

        self.loadingPreviewInfo = Ctk.CTkProgressBar(self.root2Frame, width=300, height=8, corner_radius=4, orientation="horizontal", mode="determinate", determinate_speed=20)
        #self.loadingPreviewInfo.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky=Ctk.EW)
        self.loadingPreviewInfo.set(value=0)

        self.videoIcon = Ctk.CTkImage(light_image=Image.open(fp='./Icons/Video_Icon.png'), size=(100,100))

        self.videoImage = Ctk.CTkLabel(self.root2Frame, text='', compound="center", image=self.videoIcon, fg_color='#ff0')
        self.videoImage.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="ew")
        
        #region METHODS

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

        self.swichtWidgetState("disabled")


    def swichtWidgetState(self, state: str) -> None:

        self.downloadVideo.configure(state=state)
        self.videoCombobox.configure(state=state)
        self.audioCombobox.configure(state=state)


    def clickEvent(self, event):

        self.threadDownload = Thread(target=self.readURL, name="Thread-1", daemon=True) if threading.current_thread().name != "Thread-1" else None

        self.threadDownload.start()

        self.loadingPreviewInfo.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky=Ctk.EW)


    def readURL(self):

        readLink = self.entryURL.get()  #   https://www.youtube.com/watch?v=_jMz4QKEihM

        try:
            self.yt = YouTube(readLink)

        except VideoUnavailable:

            print(f' - Video {readLink} is unavaialable, skipping.')

        else:
            
            self.loadingPreviewInfo.step()
            self.showInf(self.yt)
            self.loadingPreviewInfo.step()
            self.filterAudioInf(self.yt)
            self.loadingPreviewInfo.step()
            self.filterVideoInf(self.yt)
            self.loadingPreviewInfo.step()
            self.getVideoThumbnail(self.yt)
            self.loadingPreviewInfo.step()
            self.loadingPreviewInfo.grid_forget()
            self.swichtWidgetState("readonly")

            print(self.yt.length)

        print(readLink)

    def showInf(self, yt: YouTube):

        self.title = StringVar()
        self.autor = StringVar()
        self.duration = StringVar()

        self.title.set(yt.title)
        self.autor.set(yt.author)
        self.duration.set(yt.length)

        self.titleTextbox.configure(textvariable=self.title)
        self.autorTextbox.configure(textvariable=self.autor)
        self.durationLabel.configure(textvariable=self.duration)


    def filterAudioInf(self, yt: YouTube):

        re.purge()
        audioStr, self.audioItag, audioAbr, self.audioData = [], [], [], []

        # stream retorna StreamQuery
        self.streamsFilterAudio = yt.streams.filter(only_audio=True)
        audioStr = str(self.streamsFilterAudio)

        self.audioItag = re.findall(pattern=r'itag="(\d+)"', string=audioStr)
        audioAbr = re.findall(pattern=r'abr="(\d+[A-z]{1,})"', string=audioStr)

        audioAbR = [abr.replace("kbps", "") for abr in audioAbr]
        audioAbR.sort(key=lambda item: int(item), reverse=True)
        audioAbR = [(abr+"kbps") for abr in audioAbR]

        self.audioData = dict(zip(self.audioItag, audioAbr, strict=True))

        self.audioCombobox.configure(**{"values": audioAbR})
        self.audioCombobox_var.set("Audio")

        #audioList = audioStr

        print("\n******************************************************")
        print(self.audioItag)
        print(audioAbr)
        print(self.audioData)


    def filterVideoInf(self, yt: YouTube):

        re.purge()
        videoStr, videoItag, videoRes, videoFormat, resToDisplay = [], [], [], [], []
        resAvailable, self.videoOptions = {}, {}

        # stream retorna StreamQuery
        self.streamsFilterVideo = yt.streams.filter(only_video=True)
        videoStr = str(self.streamsFilterVideo)

        videoItag = re.findall(pattern=r'itag="(\d+)"', string=videoStr)
        videoRes = re.findall(pattern=r'res="(\d+[A-z]{1,})"', string=videoStr)
        videoFormat = re.findall(pattern=r'mime_type="([A-z]+/\w+)"', string=videoStr)

        videoResCounter = Counter(videoRes)

        videoRF = list(zip(videoRes, videoFormat, strict=True))
        repeatedVideoInfo = dict(zip(videoItag, videoRF, strict=True))
        resAvailable = dict(zip(videoResCounter.keys(), videoResCounter.values()))   # {'2160p':1, '1440p':1, '1080p':2}

        for res, quantity in resAvailable.items():
            for itag, resAndFormat in repeatedVideoInfo.items():
                if (res == resAndFormat[0]) and ((quantity == 1) or ((quantity > 1) and (resAndFormat[1] == "video/mp4"))):
                    resToDisplay.append(res)
                    self.videoOptions[res] = itag

        self.videoCombobox.configure(**{"values": resToDisplay})
        self.videoCombobox_var.set("Video")

        print(videoStr)
        print(videoFormat)
        print(videoItag)
        print(videoRes)
        print(self.videoOptions)
        print("******************************************************\n")


    def getVideoThumbnail(self, yt: YouTube):
        
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
        '''print(threading.current_thread().name)
        print(threading.active_count())
        print(threading.enumerate())'''


    def saveFile(self):

        self.getItag()


    def getItag(self):

        a, v, f = "", "", ""

        a = self.audioCombobox.get()
        v = self.videoCombobox.get()
        f = self.videoFormatCombobox.get()

        if a == "Audio":
            a = self.audioItag[-2]
        else:
            a = list(self.audioData.keys())[list(self.audioData.values()).index(a)]

        if v == "Video":
            v = self.videoOptions["240p"] # Si no se selecciona una resolucion, toma la de 24op
        else:
            v = self.videoOptions[v]


        print(a, v)
        self.streamsFilterAudio.get_by_itag(a)
        self.streamsFilterVideo.get_by_itag(v)


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
