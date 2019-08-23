import opencc
from opencc import OpenCC



class Converter():
    config='s2twp'
    cc = None
    def convert(self,str):
        return self.cc.convert(str)
    
    def __init__(self):
        self.cc = OpenCC(self.config)
        