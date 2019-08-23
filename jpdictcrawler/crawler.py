import requests
from bs4 import BeautifulSoup
import codecs
from urllib.parse import quote


import string
if __name__ == '__main__':
    from path import *
    from define import *
else:
    from .path import *
    from .define import *
import logging
import os








#---------cookies添加-----------------
f=open(COOKIES_PATH,'r')#打开所保存的cookies内容文件
cookies={}#初始化cookies字典变量
for line in f.read().split(';'):   #按照字符：进行划分读取
    #其设置为1就会把字符串拆分成2份
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容
    
#-----------------------------------

def string_shaping(str):
    return str.replace("\n", "").strip()



#------------------------------------------------------------------
# find the first sentence in the tag's scope
# return a list of [def_sentence_from,def_sentence_to,audio_link]
def find_sentence_pair(tag):
    def_sentence_from = tag.find(attrs={'class':'def-sentence-from'})
    if(def_sentence_from==None):
        return None;
    def_sentence_to = tag.find(attrs={'class':'def-sentence-to'})
    audio_link = def_sentence_from.find(attrs={'class':'word-audio'}).get('data-src')
    return [string_shaping(def_sentence_from.text),string_shaping(def_sentence_to.text),audio_link]

class CrawlerError(Exception):
    pass

class JpDictCrawler():
    soup = None
    numPronounces = 1
    indexPronounces = 0
    isWordFound = False
    word = ''
    def serchWord(self,word):
        self.word = word
        url = dict_url+word
        url = quote(url, safe = string.printable)
        logging.debug("url:"+str(url))
        try:
            resp = requests.get(url, headers = headers,cookies = cookies)
        except requests.ConnectionError as e:
            logging.error(e)
            return None
        logging.debug('web connect status code:'+str(resp.status_code))
        logging.debug("encoding:"+str(resp.encoding))
        soup = BeautifulSoup(resp.text,'html.parser')
        if not soup:
            logging.warning('soup is not exist')
            return None
        word_found = soup.find(attrs={'class':'word-details-pane'})
        #this exist some problem if some cross word is found,the web will not return a page which containing word-notfound
        #word_notfound = soup.find('div',attrs={'class':'word-notfound'}) 
        if not word_found:
            self.isWordFound = False
            logging.info(word+':word not found')
            return soup
        else:
            self.isWordFound = True
        multi_pronounces = soup.find_all('header',attrs={'class':'word-details-header'})
        if(multi_pronounces):
            pronounces = soup.find_all(attrs={'class':'word-details-pane'})
            self.numPronounces = len(pronounces)
            logging.info(word+':the word has　'+ str(self.numPronounces) + '　pronounces')
        else:
            numPronounces = 1
        self.soup = soup    
        return soup
    
    # check if the current soup is valid
    def checkValid(self):
        if(self.isSoupExist()):           
            if(self.isWordFound):
                return True
            else:
                logging.warning('this word is not found, check if you have handled it before!!')
                return False
        else:
            return False 
    
    def isSoupExist(self):
        if(self.soup):
            return True
        else:
            raise CrawlerError('soup is not exist, check if you have serched before!!')
            return False
    
    def isMultiPronounces(self):
        self.checkValid()
        if self.numPronounces ==1:
            return False
        else:
            return True
    
    # select pronounces using kana
    # if success set indexPronounces and return true
    # else return false
    def selectKana(self,kana):
        if not self.checkValid():
            return False
        pronounces = self.soup.find('header',attrs={'class':'word-details-header'}).find_all('div',attrs={'class':'pronounces'})
        for i in range(self.numPronounces):
            if kana == string_shaping(pronounces[i].find('span').text).replace("[", "").replace("]", ""):
                self.indexPronounces = i
                return True
        return False
    
    # return the meanings of the word
    def getMeaning(self):
        if not self.checkValid():
            return None
        meanings_str = ''
        simples = self.soup.find_all('div',attrs={'class':'simple'})
        if(simples):
            '''
            pos = simples[self.indexPronounces].find_all('h2')#part of speech
            meanings = simples[self.indexPronounces].find_all('ul')
            for i in range(len(meanings)):
                meanings_str = meanings_str + string_shaping(pos[i].text) + string_shaping(meanings[i].text)+'\n'
            '''
            meanings_str = simples[self.indexPronounces].text
        return meanings_str
    
    # get example sentence of the word
    # return a list of the sentence in the form of [Sentence,SentenceMening,SentenceAudioLink]
    def getSentence(self):
        if not self.checkValid():
            return None
        detail_groups = self.soup.find_all(attrs={'class':'detail-groups'})
        if(detail_groups):
            return find_sentence_pair(detail_groups[self.indexPronounces])
    
    # get pronounce of the word 
    # return a list of the pronounce in the form of [Kana,PronounceAudioLink,Romaji]
    def getPronounce(self):
        if not self.checkValid():
            return None
        if self.numPronounces==1:
            pronounce = self.soup.find('div',attrs={'class':'pronounces'})
            return [string_shaping(pronounce.find('span').text).replace("[", "").replace("]", ""),\
                    string_shaping(pronounce.find(attrs={'class':'word-audio'}).get('data-src')),\
                    string_shaping(pronounce.find_all('span')[1].text).replace("[", "").replace("]", "")]
        else:
            pronounces = self.soup.find_all('div',attrs={'class':'word-details-pane'})
            return [string_shaping(pronounces[self.indexPronounces].find('div',attrs={'class':'pronounces'}).find('span').text).replace("[", "").replace("]", ""),\
                    string_shaping(pronounces[self.indexPronounces].find(attrs={'class':'word-audio'}).get('data-src')),\
                    string_shaping(pronounces[self.indexPronounces].find('div',attrs={'class':'pronounces'}).find_all('span')[1].text).replace("[", "").replace("]", "")]
    def dumpHtmlResult(self):
        try:
            f = codecs.open(HTML_RESULT_PATH,"w+","utf-8")
            self.checkValid()
            #-------print total html result--------
            text = self.soup.prettify()
            f.write(text)
            f.close()
            return True
        except:
            return False
        
    def __init__(self):
        return

if __name__ == '__main__':
    
    logging.debug('\n--------------debug the crawler module---------------')
    jp = JpDictCrawler();
    
    word = '危ない'
    
    jp.serchWord(word)
    


    try:
        if jp.dumpHtmlResult():
            logging.debug('dump html successfully')
        else:
            logging.debug('dump html fail')
        show_msg = '\n------------------------------result--------------------------------\n'
        #------------open file------------------------------------
        
        show_msg = show_msg + 'Expression:\n' + word +'\n'

        #jp.selectKana('みょうにち')
        
        show_msg = show_msg +'這詞有'+str(jp.numPronounces)+'個讀音'
        if(jp.isMultiPronounces()):
            show_msg = show_msg+ '現在是第'+str(jp.indexPronounces+1)+'個讀音'
        [kana,link,spelling]=jp.getPronounce()    
        show_msg = show_msg +'\nkana:\n'+kana+'\npronounce:\n'+link+'\n詞義\n'+jp.getMeaning()
        
        sentence = jp.getSentence()
        if (sentence):
            show_msg = show_msg +'\n例句\n'+sentence[0]+'\n'+sentence[1]+'\n'+sentence[2]
        show_msg = show_msg + '\n--------------------------------end---------------------------------'
        logging.debug(show_msg)
        r = requests.get(link)
        if not r:
            logging.error('pronounces audio has not been download')
        else:
            logging.debug('pronounces audio has been download')
        PRONOUNCE_PATH = os.path.join(DEBUG_PATH, 'pronounce_audio.mp3')
        open(PRONOUNCE_PATH, 'wb').write(r.content)
        
        r = requests.get(sentence[2],headers = headers)
        if not r:
            logging.error('sentence audio has not been download')
        else:
            logging.debug('sentence audio has been download')
        SENTENCE_PATH = os.path.join(DEBUG_PATH, 'sentence_audio.mp3')
        open(SENTENCE_PATH, 'wb').write(r.content)
        
    except CrawlerError as e:
        logging.error(e)