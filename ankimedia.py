from aqt import mw
from .jpdictcrawler.downloader import Downloader
import os.path
class AnkiMedia():
    @staticmethod
    def audioLinkToField(url,file_name):
        MEDIA_PATH = mw.col.media.dir()
        path = os.path.join(MEDIA_PATH, file_name + ".mp3")
        Downloader.saveDataFromUrl(url,path)
        return '[sound:'+file_name+'.mp3]'