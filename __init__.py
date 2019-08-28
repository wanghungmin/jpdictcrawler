# -*- coding: utf-8 -*-

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo,chooseList,ButtonedDialog
# import all of the Qt GUI library
from aqt.qt import *
from aqt.fields import FieldDialog
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
from .str import *
from .jpdictcrawler.path import *
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



class SetupWidget(QWidget):
    def __init__(self,sw):
        QWidget.__init__(self)
        self.sw = sw
        layout = QVBoxLayout(self)
        sg_checkbox = QCheckBox("sentence generate")
        cc_checkbox = QCheckBox("chinese convert")
        btn = QPushButton("OK")
        layout.addWidget(sg_checkbox)
        layout.addWidget(cc_checkbox)
        layout.addWidget(btn)
def testFunction():
    global sw
    # show a message box
    #showInfo("Written by redmin")
    mw.myWidget = setup = SetupWidget(sw)
    setup.show()
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
        if not af.isAllFieldEmpty():
            return flag
        if srcTxt == '':
            af.flushDstFields()
            return True
        if not jp.serchWord(srcTxt):
            return flag
        
        #kana = af.getFieldValue(n,'KanaFields')
        if jp.isMultiPronounces():
            logging.debug("pop QComboBox to select pronounce")
            list = jp.getKanaList()
            index = chooseList("multi pronounce", list, startrow=0, parent=None)
            jp.setIndexPronounces(index)
       
        sentence = jp.getSentence()
        meaning = jp.getMeaning()
        pronounce = jp.getPronounce()
        if meaning:
            meaning = LF2BR(removeFirstLF(onlyOneLF(meaning)))
            af.addDstValue('MeaningFields',cc.convert(meaning))
        if pronounce:
            af.addDstValue('KanaFields',pronounce[0])
            af.addDstValue('PronounceAudioField',AnkiMedia.audioLinkToField(pronounce[1],pronounce[2]))
        if sentence and sw.sentence_generate:
            if pronounce[2] == None:
                file_name = srcTxt+"_sentence"
            else:
                file_name = pronounce[2]+"_sentence"
            af.addDstValue('SentenceFields',sentence[0])
            af.addDstValue('SentenceMeaningFields',cc.convert(sentence[1]))
            af.addDstValue('SentenceAudioField',AnkiMedia.audioLinkToField(sentence[2],file_name))
        
        if not af.generateFields():
            return flag
            
    except crawler.CrawlerError as e:
        logging.warning(e)
    except requests.ConnectionError as e:
        showInfo(e)
    except Exception as e:
        logging.error('Error when serch word:'+jp.word)
        logging.error(e)
        logging.error(traceback.format_exc())
        jp.dumpHtmlResult()
        jp = None
        raise
    return True


# deprecated:this method is failed because the editor does not recieve the update flag to update the view
def regenerateFields(index):
    global jp
    global af
    global editor_ptr
    jp.setIndexPronounces(index)
    logging.debug('regenerate fields')
    sentence = jp.getSentence()
    meaning = jp.getMeaning()
    pronounce = jp.getPronounce()
    if meaning:
        meaning = LF2BR(removeFirstLF(onlyOneLF(meaning)))
        af.addDstValue('MeaningFields',cc.convert(LF2BR(onlyOneLF(meaning))))
    if pronounce:
        af.addDstValue('KanaFields',pronounce[0])
        af.addDstValue('PronounceAudioField',AnkiMedia.audioLinkToField(pronounce[1],pronounce[2]))
    if sentence and sw.sentence_generate:
        af.addDstValue('SentenceFields',sentence[0])
        af.addDstValue('SentenceMeaningFields',cc.convert(sentence[1]))
        af.addDstValue('SentenceAudioField',AnkiMedia.audioLinkToField(sentence[2],pronounce[2]+"_sentence"))
    if sentence == None:
        af.addDstValue('SentenceFields','')
        af.addDstValue('SentenceMeaningFields','')
        af.addDstValue('SentenceAudioField','')
        
    if not af.generateFields():
        return False
    editor_ptr.loadNoteKeepingFocus()
    #editor_ptr.loadNote()
    logging.debug('regenerate fields success')
    return True
# todo:open the search result
def onStrike(editor):
    pass
icon_path = os.path.join(ICON_PATH,"icon.png")
def addMyButton(buttons, editor):
    editor._links['strike'] = onStrike
    return buttons + [editor._addButton(
        icon_path, # "/full/path/to/icon.png",
        "strike", # link name
        "tooltip")]
addHook("setupEditorButtons", addMyButton)    
#-------------------------------------------

addHook('editFocusLost', onFocusLost)
# create a new menu item, "JpDictCrawler"
action = QAction("JpDictCrawler", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)