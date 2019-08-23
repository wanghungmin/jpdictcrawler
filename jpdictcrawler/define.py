import logging
from .path import *
__all__ = [
    'dict_url',
    'headers'
    ]

dict_url = 'https://dict.hjenglish.com/jp/jc/'#爬滬江小D
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

#設定日誌安全等級為 DEBUG
#設定日誌檔名編碼
#設定日誌輸出格式
logging.basicConfig(level=logging.DEBUG,\
                    handlers=[logging.FileHandler(LOGFILE_PATH, 'a', 'utf-8')],\
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',\
                    datefmt='%m-%d %H:%M',)