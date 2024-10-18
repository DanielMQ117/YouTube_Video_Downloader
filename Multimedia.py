
import sys
import ffmpeg as fm
from os import remove
from pathlib import Path
from datetime import date
from threading import Thread
from Lib import existsThread
from time import strftime, localtime


class Download_File():

    tempFiles = 'Temp'
    root = Path('/').absolute().joinpath(tempFiles)
    fileType = {'audio': ['.mp3'], 'video': ['.mp4', '.avi', '.mkv']}

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

        audioPath = audio.download(output_path=str(self.root), filename=fileName, filename_prefix='a_')
        audio_stream = fm.input(filename=r'{}'.format(audioPath))
        finalFile = outputPath + '/' + title + format

        if format in self.fileType['video']:

            video = kwargs['video']
            videoPath = video.download(output_path=str(self.root), filename=fileName, filename_prefix='v_')
            video_stream = fm.input(filename=r'{}'.format(videoPath))
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

        exists = existsThread('Thread-2')

        if not exists:
            self.threadSave = Thread(target=self.outputFile, name='Thread-2', args=(title, outputPath), kwargs=kwargs, daemon=True) 
            self.threadSave.start()
        else:
            return 0
