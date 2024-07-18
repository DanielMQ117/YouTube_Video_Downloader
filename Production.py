
import re
import sys
import threading
import ffmpeg as fm
from PIL import Image
from requests import *
from pathlib import Path
from datetime import date
from pytube import YouTube
import customtkinter as Ctk
from threading import Thread
from bs4 import BeautifulSoup
from tkinter import StringVar
from collections import Counter
from os import readlink, remove
from pytube.exceptions import *
from typing import Dict, Literal
from time import strftime, localtime

# prevent IDE from removing unused imports
_ = re, StringVar, fm, YouTube, Image, readlink, remove, date, Ctk, strftime, localtime, BeautifulSoup

Ctk.set_appearance_mode('dark')
Ctk.set_default_color_theme('green')


def video_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)

def audio_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)

def videoFormat_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)


def existsThread(name: str) -> bool:
    # Itera sobre todos los hilos activos
    for th in threading.enumerate():
        if th.name == name: return True
    return False


class Download_File():

    tempFiles = 'Temp'
    root = Path('/').absolute().joinpath(tempFiles)

    def __init__(self):
        self._openDirectory()

    def _openDirectory(self) -> bool:

        try:
            self.root.mkdir(parents=True, exist_ok=True)
            print(f'Directorio "{self.root}" creado exitosamente.')

            return True

        except Exception as e:
            print(f'No se pudo crear el directorio "{self.root}": {e}')

        return False

    def outputFile(self, title: str, outputPath: str = None, **kwargs) -> bool:

        sys.stdin.flush(); sys.stdout.flush()

        title = title.replace('/', '_')[:]
        if outputPath == None: outputPath = str(Path(__file__).parent)
        fileName = str(date.today()).replace('-', '_') + strftime("_at_%I-%M-%S-%p", localtime())

        abr = kwargs['abr'] * 1000
        audio = kwargs['audio']
        format = kwargs['format']

        audioPath = audio.download(output_path = str(self.root), filename = fileName, filename_prefix = 'a_')
        audio_stream = fm.input(filename = r'{}'.format(audioPath))
        finalFile = outputPath + '/' + title + format

        if format in kwargs['fileType']['video']:

            video = kwargs['video']
            videoPath = video.download(output_path = str(self.root), filename = fileName, filename_prefix = 'v_')
            video_stream = fm.input(filename = r'{}'.format(videoPath))
            (
                fm
                .output(audio_stream,
                        video_stream,
                        finalFile,
                        threads=9,
                        acodec='aac',
                        audio_bitrate=abr,
                        vcodec='h264',
                        bufsize='6.5M',
                        metadata=f'title={title}')
                .run(overwrite_output=False)
            )
            remove(videoPath); remove(audioPath)

            return True
        (
            fm
            .output(audio_stream,
                    finalFile,
                    threads=3,
                    acodec='libmp3lame',
                    audio_bitrate=abr,
                    bufsize=(abr*1.5),
                    metadata=f'title={title}')
            .run(overwrite_output=False)
        )
        remove(audioPath)

        return True

    def saveFile(self, title, outputPath, **kwargs):

        if existsThread('Thread-2'):
            self.threadSave = Thread(target=self.outputFile, name='Thread-2', args=(title, outputPath), kwargs=kwargs, daemon=True) 
            self.threadSave.start()
        else:
            return 0


class App(Ctk.CTk):

    pathSet = None
    height = 34
    suffix = 'kbps'
    fileType = {'audio': ['.mp3'], 'video': ['.mp4', '.avi', '.mkv', '.webm']}
    videoFormatItag = []
    videoFormatItag.extend(fileType['audio'])
    videoFormatItag.extend(fileType['video'])


    def __init__(self):

        super().__init__()

        self.resizable(False, 0)            # type: ignore
        self.title('Video Downloader')

        self.font = Ctk.CTkFont(family='Roboto',size=12, weight='bold', slant='roman')

        self.root0Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color='gray84', height=100)
        self.root0Frame.grid(row=0, column=0, sticky=Ctk.NSEW, padx=10, pady=(10, 5))

        self.root1Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color='gray84', height=100)
        self.root1Frame.grid(row=1, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 5))

        self.root2Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color='gray84', height=100)
        self.root2Frame.grid(row=2, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 10))

        self.URLLabel = Ctk.CTkLabel(self.root0Frame, width=51, height=self.height, text='URL', font=self.font, fg_color='#71C5E8', corner_radius=6)
        self.URLLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.entryURL = Ctk.CTkEntry(self.root0Frame, placeholder_text='Copy the URL here', text_color='#19222B', font=Ctk.CTkFont(size=12, weight='normal', slant='italic'), width=200, height=34, corner_radius=6, fg_color='#EBBDD1')
        self.entryURL.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky=Ctk.NSEW)
        self.entryURL.bind('<Return>', self.clickEvent)

        self.clearButton = Ctk.CTkButton(self.root0Frame, text='x', width=34, height=34, text_color='gray10', bg_color='transparent', fg_color='gray84', hover_color='gray78', command=self.clearUrl)
        self.clearButton.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky=Ctk.NSEW)

        self.titleLabel = Ctk.CTkLabel(self.root1Frame, width=51, height=self.height, text='Title:', font=self.font, fg_color='#71C5E8', corner_radius=6)
        self.titleLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky=Ctk.NSEW)

        self.title = StringVar()
        self.titleTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=self.height, corner_radius=6, fg_color='gray78', text_color='#000000')
        self.titleTextbox.grid(row=0, column=1, padx=(5, 5), pady=(10, 5), sticky='nsew')
        self.titleTextbox.configure(state='readonly')
        
        self.duration = StringVar()
        self.durationLabel = Ctk.CTkLabel(master=self.root1Frame, text='00:00' ,font=Ctk.CTkFont(size=12, weight='normal', slant='roman'), width=34, height=self.height, corner_radius=6, fg_color='gray78', text_color='#000000')
        self.durationLabel.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.autorLabel = Ctk.CTkLabel(self.root1Frame, width=51, height=self.height, text='Autor:', font=self.font, fg_color='#71C5E8', corner_radius=6)
        self.autorLabel.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky=Ctk.W)

        self.autor = StringVar()
        self.autorTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=self.height, corner_radius=6, fg_color='gray78', text_color='#000000')
        self.autorTextbox.grid(row=1, column=1, padx=(5, 5), pady=(5, 10), sticky='nsew')
        self.autorTextbox.configure(state='readonly')

        self.setPathButton = Ctk.CTkButton(master=self.root1Frame, width=60, height=34, text='Save in', font=self.font, fg_color='#71C5E8', command=self.setPath)
        self.setPathButton.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky='w')

        self.downloadIcon = Ctk.CTkImage(light_image=Image.open(fp="./Icons/Download_Icon.png"), size=(26,26))

        self.downloadVideo = Ctk.CTkButton(master=self.root1Frame, width=110, height=34, corner_radius=17, text_color='#000000', text='Download', font=self.font, image=self.downloadIcon, fg_color='#8a2be2', command=self.saveFile, compound=Ctk.RIGHT)
        self.downloadVideo.configure(state='disabled')
        self.downloadVideo.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky='e')

        self.parametersTabview = Ctk.CTkTabview(self.root1Frame, height=40, anchor='NW')
        self.parametersTabview.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), columnspan=3, sticky='nsew')
        self.parametersTabview.add('Set Quality')

        self.videoCombobox_var = Ctk.StringVar()
        self.videoItag = []
        self.videoCombobox = Ctk.CTkComboBox(self.parametersTabview.tab('Set Quality'), values=self.videoItag, width=90,command=video_Combobox_callback, variable=self.videoCombobox_var)
        self.videoCombobox.grid(row=0, column=0, padx=(10, 5), pady=(5, 10), sticky=Ctk.W)
        self.videoCombobox.configure(state='disabled')
        self.videoCombobox_var.set('Video')

        self.audioCombobox_var = Ctk.StringVar()
        self.showAudioItag = []
        self.audioCombobox = Ctk.CTkComboBox(self.parametersTabview.tab('Set Quality'), values=self.showAudioItag, width=90, command=audio_Combobox_callback, variable=self.audioCombobox_var)
        self.audioCombobox.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky=Ctk.N)
        self.audioCombobox.configure(state='disabled')
        self.audioCombobox_var.set('Audio')

        self.videoFormatCombobox_var = Ctk.StringVar()
        self.videoFormatCombobox = Ctk.CTkComboBox(self.parametersTabview.tab('Set Quality'), width=80, values=self.videoFormatItag, command=videoFormat_Combobox_callback, variable=self.videoFormatCombobox_var)
        self.videoFormatCombobox.grid(row=0, column=2, padx=(5, 10), pady=(5, 10), sticky=Ctk.E)
        self.videoFormatCombobox.configure(state='readonly')
        self.videoFormatCombobox_var.set('format')

        self.videoIcon = Ctk.CTkImage(light_image=Image.open(fp="./Icons/Video_Icon.png"), size=(100,100))

        self.videoImage = Ctk.CTkLabel(self.root2Frame, text='', compound='center', image=self.videoIcon)
        self.videoImage.pack(fill='x', anchor='center', side=Ctk.BOTTOM, padx=(10, 10), pady=(10, 10))

        self.loadingPreviewInfo = Ctk.CTkProgressBar(self.root2Frame, width=310, height=8, corner_radius=4, orientation='horizontal', mode='determinate', determinate_speed=20)
        self.loadingPreviewInfo.set(value=0)
        
        self.downloader = Download_File()

        #region METHODS

    def clearUrl(self):

        self.titleTextbox.configure(state='normal')
        self.autorTextbox.configure(state='normal')
        self.duration.set('00:00')

        self.entryURL.delete(0, Ctk.END)
        self.titleTextbox.delete(0, Ctk.END)
        self.autorTextbox.delete(0, Ctk.END)
        self.durationLabel.configure(textvariable=self.duration)

        self.titleTextbox.configure(state='readonly')
        self.autorTextbox.configure(state='readonly')

        self.videoCombobox_var.set('Video')
        self.audioCombobox_var.set('Audio')
        self.videoFormatCombobox_var.set('format')

        self.videoCombobox.configure(values=[])
        self.audioCombobox.configure(values=[])

        self.swichtWidgetState('disabled')


    def swichtWidgetState(self, state: str) -> None:

        self.downloadVideo.configure(state=state)
        self.videoCombobox.configure(state=state)
        self.audioCombobox.configure(state=state)

    def convertToMinutes(self, duration: int = 0) -> str:

        time = duration/60
        minutes = duration//60
        seconds = 60 * (time - minutes)
        min = '{:02d}:{:02.0f}'.format(minutes, seconds)

        return min
    
    def clickEvent(self, event):

        if existsThread('Thread-1'):
            self.threadDownload = Thread(target=self.readURL, name='Thread-1', daemon=True) 
            self.threadDownload.start()
        else:
            return 0

        self.loadingPreviewInfo.place(relx=0.5, rely=0.5, anchor='center')


    def readURL(self):

        readLink = self.entryURL.get()  #   https://www.youtube.com/watch?v=_jMz4QKEihM

        try:
            self.yt = YouTube(readLink)

        except VideoUnavailable:
            print(f' - Video {readLink} is unavaialable, skipping.')
        else:
            self.loadInf()

            print(self.yt.length)

        print(readLink)


    def loadInf(self):

        self.loadingPreviewInfo.step()
        self.showInf(self.yt)
        self.loadingPreviewInfo.step()
        self.filterAudioInf(self.yt)
        self.loadingPreviewInfo.step()
        self.filterVideoInf(self.yt)
        self.loadingPreviewInfo.step()
        self.getVideoThumbnail(self.yt)
        self.loadingPreviewInfo.step()
        self.loadingPreviewInfo.place_forget()
        self.swichtWidgetState('readonly')


    def showInf(self, yt: YouTube):

        min = self.convertToMinutes(yt.length)

        self.title.set(yt.title)
        self.autor.set(yt.author)
        self.duration.set(min)

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

        self.audioData = dict(zip(self.audioItag, audioAbr, strict=True))
        audioAbr.sort(key = lambda item: int(item.replace(self.suffix, '')), reverse=True)

        self.audioCombobox.configure(**{'values': audioAbr})
        self.audioCombobox_var.set('Audio')


    def filterVideoInf(self, yt: YouTube):

        re.purge()
        videoStr, videoItag, videoRes, videoFormat, resToDisplay = [], [], [], [], []
        self.videoData = {}

        # stream retorna StreamQuery
        self.streamsFilterVideo = yt.streams.filter(only_video=True)
        videoStr = str(self.streamsFilterVideo)

        videoItag = re.findall(pattern=r'itag="(\d+)"', string=videoStr)
        videoRes = re.findall(pattern=r'res="(\d+[A-z]{1,})"', string=videoStr)
        videoFormat = re.findall(pattern=r'mime_type="([A-z]+/\w+)"', string=videoStr)

        repeatedRes = Counter(videoRes)   # {'2160p':1, '1440p':1, '1080p':2}
        res = list(repeatedRes.keys())    # ['2160p', '1440p', '1080p']
        rep = list(repeatedRes.values())  # [1, 1, 2]

        for i in range(0, len(res)):
            for j in range(0, len(videoRes)):
                if (videoRes[j] == res[i]) and ((rep[i] == 1) or (videoFormat[j] == 'video/mp4')):
                    self.videoData[videoRes[j]] = videoItag[j]

        resToDisplay = list(self.videoData.keys())
        self.videoCombobox.configure(values = resToDisplay)
        self.videoCombobox_var.set('Video')


    def getVideoThumbnail(self, yt: YouTube):
        
        urlImage = yt.thumbnail_url
        response = get(urlImage)

        if response.status_code == 200:
            with open("C:/Users/Daniel/Desktop/thumbnail.jpg", 'wb') as file:
                file.write(response.content)

        print('Image: ' + urlImage)

        # open and load de images for displays it in GUI
        thumbnail = Image.open(fp="C:/Users/Daniel/Desktop/thumbnail.jpg")
        showThumbnail = Ctk.CTkImage(light_image=thumbnail, size=(thumbnail.width*(.3), thumbnail.height*(.3)))
        self.videoImage.configure(image=showThumbnail)


    def setPath(self, **kwargs):

        self.pathSet = Ctk.filedialog.askdirectory()
        print(self.pathSet)


    def saveFile(self):

        getItag = self.getItag()
        title = self.title.get()
        self.downloader.saveFile(title, self.pathSet, **getItag)


    def getItag(self) -> Dict[Literal['audio', 'abr', 'video', 'format', 'fileType'], str]:

        a = self.audioCombobox.get()
        v = self.videoCombobox.get()
        f = self.videoFormatCombobox.get()

        if f == 'format': f = '.mp3'

        if a == 'Audio':
            a = self.audioItag[-2]
            abr = int(self.audioData[a].removesuffix(self.suffix))
        else:
            abr = int(a.removesuffix(self.suffix))
            a = list(self.audioData.keys())[list(self.audioData.values()).index(a)]

        a = self.streamsFilterAudio.get_by_itag(int(a))

        if f in self.fileType['audio']: return {'audio': a, 'abr': abr, 'format': f, 'fileType': self.fileType}

        if v == 'Video':
            v = self.videoData['240p'] # Si no se selecciona una resolucion, toma la de 24op
        else:
            v = self.videoData[v]

        v = self.streamsFilterVideo.get_by_itag(int(v))

        return {'audio': a, 'abr': abr, 'video': v, 'format': f, 'fileType': self.fileType}


if __name__ == '__main__':
    app = App()
    app.mainloop()



#https://docs.python.org/es/3/library/re.html
#https://docs.python.org/es/3/library/functions.html#zip
#['blue', 'green', 'dark-blue', 'sweetkind']
