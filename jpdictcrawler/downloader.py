import requests
import logging
import os
from .define import *
class DownloadError(Exception):
    pass

class Downloader():
    @staticmethod 
    def getDataFromUrl(url):
        r = requests.get(url,headers = headers)
        if r:
            logging.debug('audio has been download')
            return r.content
        else:
            logging.error('audio has not been download')
            raise DownloadError('download error,url:'+url)
            return None
    @staticmethod 
    def saveDataFromUrl(url,path):
        try:            
            open(path, 'wb').write(Downloader.getDataFromUrl(url))
            return True
        except:
            logging.error('save audio fail')
            raise
            return False