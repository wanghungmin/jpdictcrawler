# -*- coding: utf-8 -*-

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from anki.hooks import addHook
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
from .jpdictcrawler import crawler
from .jpdictcrawler.crawler import JpDictCrawler
from .jpdictcrawler.downloader import Downloader
from .ankimedia import AnkiMedia
from .autofield import AutoField
import logging
import json
import os.path
from . import opencc
from .opencc import OpenCC
from .str import LF2BR,onlyOneLF

logging.info('----------new add-on start-----------')



    
cc = OpenCC('s2twp')
'''
字串簡轉繁
常用轉換表
s2t.json Simplified Chinese to Traditional Chinese 簡體到繁體
t2s.json Traditional Chinese to Simplified Chinese 繁體到簡體
s2tw.json Simplified Chinese to Traditional Chinese (Taiwan Standard) 簡體到臺灣正體
tw2s.json Traditional Chinese (Taiwan Standard) to Simplified Chinese 臺灣正體到簡體
s2hk.json Simplified Chinese to Traditional Chinese (Hong Kong Standard) 簡體到香港繁體（香港小學學習字詞表標準）
hk2s.json Traditional Chinese (Hong Kong Standard) to Simplified Chinese 香港繁體（香港小學學習字詞表標準）到簡體
s2twp.json Simplified Chinese to Traditional Chinese (Taiwan Standard) with Taiwanese idiom 簡體到繁體（臺灣正體標準）並轉換爲臺灣常用詞彙
tw2sp.json Traditional Chinese (Taiwan Standard) to Simplified Chinese with Mainland Chinese idiom 繁體（臺灣正體標準）到簡體並轉換爲中國大陸常用詞彙
t2tw.json Traditional Chinese (OpenCC Standard) to Taiwan Standard 繁體（OpenCC 標準）到臺灣正體
t2hk.json Traditional Chinese (OpenCC Standard) to Hong Kong Standard 繁體（OpenCC 標準）到香港繁體（香港小學學習字詞表標準）
'''



class Switch():
    chinese_convert = True
    sentence_generate = True
af = AutoField()
jp = JpDictCrawler()
config = mw.addonManager.getConfig(__name__)
af.loadConfig(config)
sw = Switch()



class SetupWidget():
    def __init__(self):
        self.widget = QWidget()
        self.checkbox = QCheckBox("sentence generate",widget)
def testFunction():
    global sw
    # show a message box
    showInfo("Written by redmin")
    
    '''
    mw.myWidget = widget = QWidget()
    checkbox = QCheckBox("sentence generate",widget)
    def setSentenceGenerateFlag(checkbox):
        sw.sentence_generate = checkbox.checkState()
    checkbox.setCheckState(sw.sentence_generate)
    checkbox.setTristate(False)
    checkbox.stateChanged.connect(setSentenceGenerateFlag)
    widget.show()
    '''


'''    
config = mw.addonManager.getConfig(__name__)

srcFields = config['srcFields']
dstMeaningFields = config['dstMeaningFields']
dstPronounceFields = config['dstPronounceFields']
dstPronounceAudioField = config['dstPronounceAudioField']
dstSentenceFromFields = config['dstSentenceFromFields']
dstSentenceToFields = config['dstSentenceToFields']
dstSentenceAudioField = config['dstSentenceAudioField']

def onFocusLost(flag, n, fidx):
    jp = JpDictCrawler()
    src = None
    dstMeaning = None
    dstPronounce = None
    dstPronounceAudio = None
    dstSentenceFrom = None
    dstSentenceTo = None
    dstSentenceAudio = None
    # japanese model?
    if "japanese" not in n.model()['name'].lower():
        return flag

    # have src and dst fields?
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in srcFields:
            if name == f:
                src = f
                srcIdx = c
        for f in dstMeaningFields:
            if name == f:
                dstMeaning = f
        for f in dstPronounceFields:
            if name == f:
                dstPronounce = f
        for f in dstPronounceAudioField:
            if name == f:
                dstPronounceAudio = f
        for f in dstSentenceFromFields:
            if name == f:
                dstSentenceFrom = f
        for f in dstSentenceToFields:
            if name == f:
                dstSentenceTo = f
        for f in dstSentenceAudioField:
            if name == f:
                dstSentenceAudio = f
    if not src or not(dstMeaning or dstPronounce or dstPronounceAudio or dstSentenceFrom or dstSentenceTo or dstSentenceAudio):
        return flag
    # if the src field is empty,flush all the dst fields
    if not n[src]:
        if dstMeaning:
            n[dstMeaning] = ''
        if dstPronounce:
            n[dstPronounce] = ''
        if dstPronounceAudio:
            n[dstPronounceAudio] = ''
        if dstSentenceFrom:
            n[dstSentenceFrom] = ''
        if dstSentenceTo:
            n[dstSentenceTo] = ''
        if dstSentenceAudio:
            n[dstSentenceAudio] = ''
        return True
    # dst field already filled?
    if n[dstMeaning]:
        return flag
    if n[dstSentenceFrom]:
        return flag
    if n[dstSentenceTo]:
        return flag
    # event coming from src field?
    if fidx != srcIdx:
        return flag
    # grab source text
    srcTxt = mw.col.media.strip(n[src])
    if not srcTxt:
        return flag
    # update field
    logging.debug('src field is triggered,serch the word:'+srcTxt)
    try:
        jp.serchWord(srcTxt)
        sentence = jp.getSentence()
        meaning = jp.getMeaning()
        [kana,pronounce_link,romaji] = jp.getPronounce()
        if kana:
            if dstPronounce:
                n[dstPronounce] = kana
        if pronounce_link:
            if dstPronounceAudio:
                n[dstPronounceAudio] = AnkiMedia.audioLinkToField(pronounce_link,romaji)
        if meaning:
            if dstMeaning:
                n[dstMeaning] = meaning
        if sentence:
            if dstSentenceFrom:
                n[dstSentenceFrom] = sentence[0]
            if dstSentenceTo:
                n[dstSentenceTo] = sentence[1]
            if dstSentenceAudio:
                n[dstSentenceAudio] = AnkiMedia.audioLinkToField(sentence[2],romaji+"_sentence")
    except crawler.CrawlerError as e:
        logging.warning(e)
    except Exception as e:
        jp.dumpHtmlResult()
        logging.error(e)
        logging.error(traceback.format_exc())
        jp = None
        raise
    return True
'''

def onFocusLost(flag, n, fidx):
    global af
    global jp
    global sw
    if not af.isTargetNoteType(n.model()['name']):
        return flag
    fields = mw.col.models.fieldNames(n.model())
    src = fields[fidx] 
    if not af.isFieldInSrc(src):
        return flag
    srcTxt = mw.col.media.strip(n[src])

    try:
        if not af.findDstFieldName(n):
            return flag
        if not af.isAllFieldEmpty(n):
            return flag
        if srcTxt == '':
            af.flushDstFields(n)
            return True
        jp.serchWord(srcTxt)
        
        #kana = af.getFieldValue(n,'KanaFields')
        #if kana and jp.isMultiPronounces():
        #    jp.selectKana(kana)
        sentence = jp.getSentence()
        meaning = jp.getMeaning()
        pronounce = jp.getPronounce()
        if meaning:
            af.addDstValue('MeaningFields',cc.convert(LF2BR(onlyOneLF(meaning))))
        if pronounce:
            af.addDstValue('KanaFields',pronounce[0])
            af.addDstValue('PronounceAudioField',AnkiMedia.audioLinkToField(pronounce[1],pronounce[2]))
        if sentence and sw.sentence_generate:
            af.addDstValue('SentenceFields',sentence[0])
            af.addDstValue('SentenceMeaningFields',cc.convert(sentence[1]))
            af.addDstValue('SentenceAudioField',AnkiMedia.audioLinkToField(sentence[2],pronounce[2]+"_sentence"))
        
        if not af.generateFields(n):
            return flag
            
    except crawler.CrawlerError as e:
        logging.warning(e)
    except Exception as e:
        logging.error('Error when serch word:'+jp.word)
        logging.error(e)
        logging.error(traceback.format_exc())
        jp.dumpHtmlResult()
        jp = None
        raise
    return True
addHook('editFocusLost', onFocusLost)
# create a new menu item, "JpDictCrawler"
action = QAction("JpDictCrawler", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)