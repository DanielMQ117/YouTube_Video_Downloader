
import re
from Lib import *
from PIL import Image
from Theme import colors
from pytube import YouTube
import customtkinter as Ctk
from threading import Thread
from tkinter import StringVar
from collections import Counter
from pytube.exceptions import *
from typing import Dict, Literal
from Multimedia import Download_File

# prevent IDE from removing unused imports
_ = re, StringVar, YouTube, Image, Ctk

Ctk.set_appearance_mode('light')
Ctk.set_default_color_theme('green')


def video_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)

def audio_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)

def videoFormat_Combobox_callback(choice):
    print('combobox dropdown clicked:', choice)


class App(Ctk.CTk):

    pathSet = None
    height = 34
    suffix = 'kbps'
    fileType = {'audio': ['.mp3'], 'video': ['.mp4', '.avi', '.mkv']}
    videoFormatItag = []
    videoFormatItag.extend(fileType['audio'])
    videoFormatItag.extend(fileType['video'])


    def __init__(self):

        super().__init__()

        self.resizable(False, 0)            # type: ignore
        self.title('Video Downloader')

        self.fontR = Ctk.CTkFont(family='Roboto',size=13, weight='bold', slant='roman')
        self.fontV = Ctk.CTkFont(family='Verdana',size=12, weight='normal', slant='roman')
        self.fontI = Ctk.CTkFont(family='Verdana', size=11, weight='normal', slant='italic')

        self.root0Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color=colors[0], height=100)
        self.root0Frame.grid(row=0, column=0, sticky=Ctk.NSEW, padx=10, pady=(10, 5))

        self.root1Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color=colors[0], height=100)
        self.root1Frame.grid(row=1, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 5))

        self.root2Frame = Ctk.CTkFrame(self, corner_radius=6, fg_color=colors[0], height=100)
        self.root2Frame.grid(row=2, column=0, sticky=Ctk.NSEW, padx=10, pady=(5, 10))

        self.URLLabel = Ctk.CTkLabel(self.root0Frame, width=51, height=self.height, text='URL: :', text_color=colors[2], font=self.fontR, fg_color=colors[5], corner_radius=6)
        self.URLLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 10), sticky=Ctk.W)

        self.entryURL = Ctk.CTkEntry(self.root0Frame, placeholder_text='Copy the URL here', text_color=colors[4], font=self.fontI, width=200, height=34, corner_radius=6, fg_color=colors[1], border_color=colors[5])
        self.entryURL.grid(row=0, column=1, padx=(5, 5), pady=(10, 10), sticky=Ctk.NSEW)
        self.entryURL.bind('<Return>', self.clickEvent)

        self.clearButton = Ctk.CTkButton(self.root0Frame, text='x', font=self.fontR, width=34, height=34, text_color=colors[3], fg_color=colors[0], hover_color=colors[5], command=self.clearUrl)
        self.clearButton.grid(row=0, column=2, padx=(5, 10), pady=(10, 10), sticky=Ctk.NSEW)

        self.titleLabel = Ctk.CTkLabel(self.root1Frame, width=51, height=self.height, text='Title:', text_color=colors[2], font=self.fontR, fg_color=colors[7], corner_radius=6)
        self.titleLabel.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky=Ctk.NSEW)

        self.title = StringVar()
        self.titleTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=self.height, corner_radius=6, fg_color=colors[1], text_color=colors[3], border_color=colors[7])
        self.titleTextbox.grid(row=0, column=1, padx=(5, 5), pady=(10, 5), sticky='nsew')
        self.titleTextbox.configure(state='readonly', font=self.fontV)
        
        self.duration = StringVar()
        self.durationLabel = Ctk.CTkLabel(master=self.root1Frame, text='00:00', font=self.fontV, width=34, height=self.height, corner_radius=6, fg_color=colors[1], text_color=colors[3])
        self.durationLabel.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky='nsew')

        self.autorLabel = Ctk.CTkLabel(self.root1Frame, width=51, height=self.height, text='Autor:', text_color=colors[2], font=self.fontR, fg_color=colors[7], corner_radius=6)
        self.autorLabel.grid(row=1, column=0, padx=(10, 5), pady=(5, 10), sticky=Ctk.W)

        self.autor = StringVar()
        self.autorTextbox = Ctk.CTkEntry(master=self.root1Frame, width=200, height=self.height, corner_radius=6, fg_color=colors[1], text_color=colors[3], border_color=colors[7])
        self.autorTextbox.grid(row=1, column=1, padx=(5, 5), pady=(5, 10), sticky='nsew')
        self.autorTextbox.configure(state='readonly', font=self.fontV)

        self.setPathButton = Ctk.CTkButton(master=self.root1Frame, width=60, height=34, text='Save in', text_color=colors[2], font=self.fontR, fg_color=colors[9], hover_color=colors[10],command=self.setPath)
        self.setPathButton.grid(row=2, column=1, padx=(5, 10), pady=(5, 5), sticky='w')

        self.downloadIcon = Ctk.CTkImage(light_image=Image.open(fp="./Icons/Download_Icon.png"), size=(26,26))

        self.downloadVideo = Ctk.CTkButton(master=self.root1Frame, width=110, height=34, corner_radius=17, text='Download', font=self.fontR, image=self.downloadIcon, fg_color=colors[8], command=self.saveFile, compound=Ctk.RIGHT)
        self.downloadVideo.configure(state='disabled')
        self.downloadVideo.grid(row=2, column=1, padx=(5, 5), pady=(5, 5), sticky='e')

        self.parametersTabview = Ctk.CTkTabview(self.root1Frame, height=90, anchor='NW', fg_color=colors[1], segmented_button_fg_color=colors[9], segmented_button_selected_color=colors[9], segmented_button_selected_hover_color=colors[9])
        self.parametersTabview._segmented_button.configure(font=self.fontR)
        self.parametersTabview.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), columnspan=3, sticky='nsew')
        self._tabName = 'SETTINGS'
        self.parametersTabview.add(self._tabName)
        self.parametersTabview._segmented_button._buttons_dict[self._tabName].configure(cursor='arrow')

        self.videoCombobox_var = Ctk.StringVar()
        self.videoItag = []
        self.videoCombobox = Ctk.CTkComboBox(self.parametersTabview.tab(self._tabName), values=self.videoItag, width=80, command=video_Combobox_callback, variable=self.videoCombobox_var, fg_color=colors[1], font=self.fontV)
        self.videoCombobox.grid(row=0, column=0, padx=(10, 5), pady=(5, 10), sticky=Ctk.W)
        self.videoCombobox.configure(state='disabled')
        self.videoCombobox._dropdown_menu.configure(fg_color=colors[6], font=self.fontV)
        self.videoCombobox_var.set('Video')

        self.audioCombobox_var = Ctk.StringVar()
        self.showAudioItag = []
        self.audioCombobox = Ctk.CTkComboBox(self.parametersTabview.tab(self._tabName), values=self.showAudioItag, width=95, command=audio_Combobox_callback, variable=self.audioCombobox_var, fg_color=colors[1], font=self.fontV)
        self.audioCombobox.grid(row=0, column=1, padx=(5, 5), pady=(5, 10), sticky=Ctk.N)
        self.audioCombobox.configure(state='disabled')
        self.audioCombobox._dropdown_menu.configure(fg_color=colors[6], font=self.fontV)
        self.audioCombobox_var.set('Audio')

        self.videoFormatCombobox_var = Ctk.StringVar()
        self.videoFormatCombobox = Ctk.CTkComboBox(self.parametersTabview.tab(self._tabName), width=90, values=self.videoFormatItag, command=videoFormat_Combobox_callback, variable=self.videoFormatCombobox_var, fg_color=colors[0], font=self.fontV)
        self.videoFormatCombobox.grid(row=0, column=2, padx=(5, 10), pady=(5, 10), sticky=Ctk.E)
        self.videoFormatCombobox.configure(state='readonly', button_color=colors[5], border_color=colors[5])
        self.videoFormatCombobox._dropdown_menu.configure(fg_color=colors[6], font=self.fontV)
        self.videoFormatCombobox_var.set('.format')

        self.videoIcon = Ctk.CTkImage(light_image=Image.open(fp="./Icons/Video_Icon.png"), size=(100,100))

        self.videoImage = Ctk.CTkLabel(self.root2Frame, text='', compound='center', image=self.videoIcon)
        self.videoImage.pack(fill='x', anchor='center', side=Ctk.BOTTOM, padx=(10, 10), pady=(10, 10))

        self.loadingPreviewInfo = Ctk.CTkProgressBar(self.root2Frame, width=310, height=8, corner_radius=4, orientation='horizontal', mode='determinate', determinate_speed=20, progress_color=colors[9])
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
        self.videoFormatCombobox_var.set('.format')

        self.videoCombobox.configure(values=[])
        self.audioCombobox.configure(values=[])

        self.swichtWidgetState('disabled')


    def swichtWidgetState(self, state: Literal['readonly', 'disable']) -> None:

        if state == 'readonly':
            fg_c1=colors[7]; fg_c2=colors[0]; cursor='hand2'; bbc=colors[5]
        else: fg_c1=colors[8]; fg_c2=colors[1]; cursor='arrow'; bbc=colors[11]

        self.downloadVideo.configure(state=state, fg_color=fg_c1, cursor=cursor)
        self.videoCombobox.configure(state=state, fg_color=fg_c2, button_color=bbc, border_color=bbc)
        self.audioCombobox.configure(state=state, fg_color=fg_c2, button_color=bbc, border_color=bbc)


    def clickEvent(self, event):

        exists = existsThread('Thread-1')

        if not exists:
            self.threadDownload = Thread(target=self.readURL, name='Thread-1', daemon=True) 
            self.threadDownload.start()
        else:
            return 0

        self.loadingPreviewInfo.place(relx=0.5, rely=0.5, anchor='center')


    def readURL(self):

        readLink = self.entryURL.get()

        try:
            self.yt = YouTube(readLink)
        except VideoUnavailable:
            print(f' - Video {readLink} is unavaialable, skipping.')
        else:
            self.loadInf()


    def loadInf(self):

        self.loadingPreviewInfo.step()
        self.showInf(self.yt)
        self.loadingPreviewInfo.step()
        self.filterAudioInf(self.yt)
        self.loadingPreviewInfo.step()
        self.filterVideoInf(self.yt)
        self.loadingPreviewInfo.step()
        self.setVideoThumbnail(self.yt, self.downloader.root)
        self.loadingPreviewInfo.step()
        self.loadingPreviewInfo.place_forget()
        self.swichtWidgetState('readonly')


    def showInf(self, yt: YouTube):

        min = convertToMinutes(duration=yt.length)

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

        for i, v in enumerate(res):
            for j, v_ in enumerate(videoRes):
                if (v_ == v) and ((rep[i] == 1) or (videoFormat[j] == 'video/mp4')):
                    self.videoData[v_] = videoItag[j]

        resToDisplay = list(self.videoData.keys())
        self.videoCombobox.configure(values = resToDisplay)
        self.videoCombobox_var.set('Video')


    def setVideoThumbnail(self, yt: YouTube, root: Path):

        name = getThumbnail(url=yt.thumbnail_url, root=root)

        # open and load de images for displays it in GUI
        thumbnail = Image.open(fp=name)
        showThumbnail = Ctk.CTkImage(light_image=thumbnail, size=(thumbnail.width*(.3), thumbnail.height*(.3)))
        self.videoImage.configure(image=showThumbnail)


    def setPath(self, **kwargs):
        self.pathSet = Ctk.filedialog.askdirectory()


    def saveFile(self):

        media = self.getMultimedia()
        title = self.title.get()
        self.downloader.saveFile(title, self.pathSet, **media)


    def getMultimedia(self):

        streams = {}
        a = self.audioCombobox.get()
        v = self.videoCombobox.get()
        f = self.videoFormatCombobox.get()

        itags = getItags(self.audioData, self.videoData, aud=a, vid=v)
        streams = getVideoStream(self.streamsFilterAudio, self.streamsFilterVideo, itags, f, self.fileType['video'])
        streams['abr'] = int(a.removesuffix(self.suffix))
        
        return streams


if __name__ == '__main__':
    app = App()
    app.mainloop()
