
import threading
from pathlib import Path
from requests import get
from threading import Thread
from typing import List, Dict, Literal


def getThumbnail( url: str, root: Path, name: str = 'thumbnail.jpg') -> Path:

    path = Path(root).joinpath(name)
    response = get(url)

    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)

    return path


def existsThread(name: str) -> bool:
    # Itera sobre todos los hilos activos
    for th in threading.enumerate():
        if th.name == name: return True
    return False


def convertToMinutes(duration: int = 0) -> str:

        hour = duration // 3600
        minutes = (duration % 3600) // 60
        seconds_res = duration % 60

        time = {'s': seconds_res, 'm': minutes, 'h': hour}

        return '{h:02d}:{m:02d}:{s:02d}'.format(**time) if hour > 0 else '{m:02d}:{s:02d}'.format(**time)


def getItags(aData, vData, aud: str = 'Audio', vid: str = 'Video') -> Dict[Literal['aud', 'vid'], int]:

    itags = {}

    def setAud() -> str:
        for itag, aBr in aData.items():
            if aud == aBr: return itag

    itags['aud'] = int(list(aData.keys())[-1] if 'Audio' == aud else setAud())
    itags['vid'] = int(list(vData.values())[-1] if 'Video' == vid else vData[vid])

    return itags


def getVideoStream(audio: Dict, video: Dict, itags: Dict, format: str, fileType: List[str]) -> Dict[Literal['audio', 'video', 'format'], str]:

    videoStream = {}

    videoStream['format'] = '.mp3' if format == '.format' else format
    videoStream['audio'] = audio.get_by_itag(itags['aud'])

    if format in fileType:
        videoStream['video'] = video.get_by_itag(itags['vid'])

    return videoStream
