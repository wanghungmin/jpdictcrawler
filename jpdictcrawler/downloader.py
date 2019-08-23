import requests
import logging
import os

class DownloadError(Exception):
    pass

class Downloader():
    @staticmethod 
    def getDataFromUrl(url):
        r = requests.get(url,headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'})
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