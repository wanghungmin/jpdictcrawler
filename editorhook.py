from aqt import mw
from aqt.qt import *
from .opencc import OpenCC
from .str import LF2BR,onlyOneLF
from .jpdictcrawler.path import *
from .jpdictcrawler import crawler
from .jpdictcrawler.crawler import JpDictCrawler
from .jpdictcrawler.downloader import Downloader
from .autofield import AutoField
# hook the editor
# when each editor is opened,the hook "setupEditorButtons" will be called
# we use this hook to bind the editor and the JpDictCrawler 
# because we need to use the editor's "loadNoteKeepingFocus" function to refresh the editor when we choose the different pronounce
# but the hook "editFocusLost" do not provide the editor self
class EditorHook():
    def __init__(editor):
        self.jp = JpDictCrawler()
        self.af = AutoField()
        self.editor = editor
    def hookOnFocusLost(self,flag, n, fidx):
        if not self.af.isTargetNoteType(n.model()['name']):
            return flag
        fields = mw.col.models.fieldNames(n.model())
        src = fields[fidx] 
        if not self.af.isFieldInSrc(src):
            return flag
        srcTxt = mw.col.media.strip(n[src])

        try:
            if not self.af.findDstFieldName(n):
                return flag
            if not self.af.isAllFieldEmpty():
                return flag
            if srcTxt == '':
                self.af.flushDstFields()
                return True
            jp.serchWord(srcTxt)
            
            #kana = af.getFieldValue(n,'KanaFields')
            if self.jp.isMultiPronounces():
                self.editor.widget = box = QComboBox("select pronounce")
                list = self.jp.getKanaList()
                box.addItems(list)
                box.activated.connect(self.regenerateFields)
                box.show()
                return flag
           
            sentence = self.jp.getSentence()
            meaning = self.jp.getMeaning()
            pronounce = self.jp.getPronounce()
            if meaning:
                self.af.addDstValue('MeaningFields',cc.convert(LF2BR(onlyOneLF(meaning))))
            if pronounce:
                self.af.addDstValue('KanaFields',pronounce[0])
                self.af.addDstValue('PronounceAudioField',AnkiMedia.audioLinkToField(pronounce[1],pronounce[2]))
            if sentence:
                self.af.addDstValue('SentenceFields',sentence[0])
                self.af.addDstValue('SentenceMeaningFields',cc.convert(sentence[1]))
                self.af.addDstValue('SentenceAudioField',AnkiMedia.audioLinkToField(sentence[2],pronounce[2]+"_sentence"))
            
            if not self.af.generateFields():
                return flag
                
        except crawler.CrawlerError as e:
            logging.warning(e)
        except Exception as e:
            logging.error('Error when serch word:'+jp.word)
            logging.error(e)
            logging.error(traceback.format_exc())
            self.jp.dumpHtmlResult()
            jp = None
            raise
        return True    

    def onStrike():
        pass
    
    def regenerateFields(self,index):
        self.jp.setIndexPronounces(index)
        logging.debug('regenerate fields')
        sentence = self.jp.getSentence()
        meaning = self.jp.getMeaning()
        pronounce = self.jp.getPronounce()
        if meaning:
            self.af.addDstValue('MeaningFields',cc.convert(LF2BR(onlyOneLF(meaning))))
        if pronounce:
            self.af.addDstValue('KanaFields',pronounce[0])
            self.af.addDstValue('PronounceAudioField',AnkiMedia.audioLinkToField(pronounce[1],pronounce[2]))
        if sentence and sw.sentence_generate:
            self.af.addDstValue('SentenceFields',sentence[0])
            self.af.addDstValue('SentenceMeaningFields',cc.convert(sentence[1]))
            self.af.addDstValue('SentenceAudioField',AnkiMedia.audioLinkToField(sentence[2],pronounce[2]+"_sentence"))
        if sentence == None:
            self.af.addDstValue('SentenceFields','')
            self.af.addDstValue('SentenceMeaningFields','')
            self.af.addDstValue('SentenceAudioField','')
            
        if not self.af.generateFields():
            return False
        self.editor.loadNoteKeepingFocus()
        logging.debug('regenerate fields success')
        return True