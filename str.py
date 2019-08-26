

def LF2BR(str):
    return str.replace("\n", "<br>")
    
def onlyOneLF(str):
    while '\n\n' in str:
        str = str.replace("\n\n", "\n")
    return str
    
def removeFirstLF(str):
    return str[1:]