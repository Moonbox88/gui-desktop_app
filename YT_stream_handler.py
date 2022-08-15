import pytube.exceptions
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
#from ffmpy import FFmpeg
import io


class YTVideoDLOptions:
    def __init__(self, url):
        try:
            self.url = url
            self.yt = YouTube(self.url)

        except VideoUnavailable:
            print(f'Video "{self.url}" is unavailable, skipping.')
            exit()
        except pytube.exceptions.RegexMatchError:
            print(f'Input "{self.url}" is not valid, skipping.')
            exit()
