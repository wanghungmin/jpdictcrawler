import json
from aqt import mw
import logging

class AutoField():
    def __init__(self):
        self.noteTypes = [] # is a list 
        self.srcFields = [] # is a list 
        self.dstFields = {} # is a dict
        self.typeNameDict = {} # is a dictionary , to mark the field types and the corresponding field names in this note
        self.typeValueDict = {} # is a dictionary , to mark the field values that we want to fill in corresponding fields type 
        self.note = None
    def bindNote(n):
        self.note = n
        return
    def isTargetNoteType(self,noteName):
        noteName = noteName.lower()
        for allowedString in self.noteTypes:
            if allowedString in noteName:
                return True
        return False
        pass
    def setSrcFeilds(self,srcFields):
        self.srcFields = srcFields
        return
    def setDstFields(self,dstFields):
        self.dstFields = dstFields
        return
    def getFieldValue(self,n,field_type):
        name = self.typeNameDict[field_type]
        if name == None:
            return None
        return n[name]
    def getNameFromType(self,field_type):
        return self.typeNameDict[field_type]
    def loadConfig(self,config):
        self.srcFields = config['srcFields']
        self.dstFields = config['dstFields']
        self.noteTypes = config['noteTypes']
    def isFieldInSrc(self,field_name):
        return field_name in self.srcFields
    def flushDstFields(self):
        for type,name in self.typeNameDict.items():
            if name is None:
                continue
            self.note[name] = ''
        return 
    def addDstValue(self,field_type,value):
        self.typeValueDict.update({field_type:value})
        return
    def setField(self,n,field_name,value):
        try:
            n[field_name] = value
        except:
            raise
    def isAllFieldEmpty(self):
        flag = True
        for type,name in self.typeNameDict.items():
            if name is None:
                continue
            if self.note[name]:
                 flag = False
        return flag
    # if no dst field is found ,return False,else return true
    # this function should be call before other operation
    def findDstFieldName(self,n):
        self.note = n
        fields = mw.col.models.fieldNames(n.model())
        self.typeNameDict = {}
        flag = False
        for field_type in self.dstFields:
            self.typeNameDict.update({field_type:None}) 
            for field_name in fields:     
                if field_name in self.dstFields[field_type]:
                    self.typeNameDict.update({field_type:field_name}) 
                    flag = True
                    break             
        return flag
    # call it after all
    def generateFields(self):       
        for type , name in self.typeNameDict.items():
            if name == None:
                continue
            if type in self.typeValueDict:
                self.setField(self.note,name,self.typeValueDict[type])
        self.typeValueDict = {}
        return True   
