from platform import release
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()

class MultiKeyedDict():
    
    def __init__(self,dict) -> None:
        self.keySet=set()
        self.mainDict = {}
        for key,val in dict.items():
            for j in key:
                self.mainDict[j] = val
            self.keySet.add(key)
    
    def __getitem__(self,key):
        return self.mainDict[key] if key in self.keySet else key

    def get(self,key,elsepart):
        return self.mainDict.get(key,elsepart)


def keyDecode(key):
    wordDict = {
        'air': 'a',
        'bat': 'b',
        'cap': 'c',
        'drum': 'd',
        'each': 'e',
        'fine': 'f',
        'gust': 'g',
        'harp': 'h',
        'sit': 'i',
        'jury': 'j',
        'crunch': 'k',
        'look': 'l',
        'made': 'm',
        'near': 'n',
        'odd': 'o',
        'pitch': 'p',
        'quench': 'q',
        'red': 'r',
        'sun': 's',
        'trap': 't',
        'urge': 'u',
        'vest': 'v',
        'whale': 'w',
        'plex': 'x',
        'yank': 'y',
        'zip': 'z',
        'control': Key.ctrl,
        'shift': Key.shift,
        'alt': Key.alt,
        'backspace': Key.backspace,
        'end': Key.end,
        'home': Key.home,
        'tab' : Key.tab
    }
    if key in wordDict:
        return wordDict[key]
    return key


def press(key):
    keyboard.press(keyDecode(key))


def release(key):
    keyboard.release(keyDecode(key))


def tap(key, times=1):
    for i in range(times):
        keyboard.press(key)
        keyboard.release(key)
    return ''

# --------------------------------------------------------------------------------------------------------------------------------------------


def KeyCombos(keys):
    # keys = keys[0]
    keys.pop(0)
    for key in keys:
        press(key)
    for key in keys[::-1]:
        release(key)
    return ''


def Select(keys):
    command = keys[1]
    if command == 'line':
        tap(Key.home)
        press(Key.shift)
        tap(Key.end)
        release(Key.shift)
    elif command == 'all':
        KeyCombos(['', 'control', 'a'])
    return ''


def Kabab(keys):
    keys.pop(0)
    return '-'.join(keys)


def Camel(keys):
    output = Capital(keys)
    return output[0].lower() + output[1:]


def Capital(keys):
    keys.pop(0)
    return ''.join([x.title() for x in keys])


def Plaintext(listwords):
    listwords.pop(0)
    return ' '.join(listwords)


def ProgrammingKeywords(keywords):
    keywordList = {
        'and': 'and',
        'as': 'as',
        'assert': 'assert',
        'break': 'break',
        'class': 'class',
        'continue': 'continue',
        'def': 'def',
        'del': 'del',
        'elif': 'elif',
        'else': 'else',
        'except': 'except',
        'false': 'False',
        'finally': 'finally',
        'for': 'for',
        'from': 'from',
        'global': 'global',
        'if': 'if',
        'import': 'import',
        'in': 'in',
        'is': 'is',
        'lambda': 'lambda',
        'none': 'None',
        'nonlocal': 'nonlocal',  # ! dual pass Word
        'not': 'not',
        'or': 'or',
        'pass': 'pass',
        'raise': 'raise',
        'return': 'return',
        'true': 'True',
        'try': 'try',
        'while': 'while',
        'with': 'with',
        'yield': 'yield',
        'colon': ':',
        'comma':',',

    }
    anslist = []
    for i in keywords:
        if i in keywordList.keys():
            anslist.append(keywordList[i])
    return " ".join(anslist)


def Delete(keywords):
    keywords.pop(0)
    times = NumberDecode(keywords[0])
    tap(Key.backspace,times)

def Arguments(keywords):
    pyautogui.typewrite('()')
    keyboard.press(Key.left)
    return ''


def Move(keywords):
    keywords.pop(0)
    MoveSelectors = MultiKeyedDict({
        ('up'): Key.up,
        ('down'): Key.down,
        ('left'): Key.left,
        ('right'): Key.right,
    })
    keylen = len(keywords)
    if keylen == 1:
        moveSel = keywords[0]
        tap(MoveSelectors.get(moveSel, None))
    if keylen == 2:
        moveSel = keywords[0]
        times = NumberDecode(keywords[1])
        tap(MoveSelectors.get(moveSel, None), times)
    return ''


def NumberDecode(number):
    numberVariant = MultiKeyedDict({
        ('0'): 0,
        ('1'): 1,
        ('2'): 2,
        ('3'): 3,
        ('4'): 4,
        ('5'): 5,
        ('6'): 6,
        ('7'): 7,
        ('8'): 8,
        ('9'): 9,
    })
    # TODO incomplete
    return numberVariant[number]

def Curly(keywords):
    return '{}'

def newLine(keywords):
    tap(Key.enter)
    return ''

def Quotes(keywords):
    pyautogui.typewrite('\'\'')
    keyboard.press(Key.left)
    return ''

def Space(keywords):
    return ' '
# --------------------------------------------------------------------------------------------------------------------------------------------


def GrammerChannel(listwords):
    possibleCommands = {
        'press': KeyCombos,
        'select': Select,
        'kabab': Kabab,
        'camel': Camel,
        'capital': Capital,
        'say': Plaintext,
        'delete': Delete,
        'args': Arguments,
        'go': Move,
        'curly': Curly,
        'enter' : newLine,
        'quotes' : Quotes,
        'space' : Space,
    }
    function = possibleCommands.get(
        SelectorVaraintHandler(listwords[0]), ProgrammingKeywords)
    return function(listwords)


def SelectorVaraintHandler(input:str):
    selectorVariant = MultiKeyedDict( {
        ('camel', 'kamel'): 'camel',
        ('args', 'arcs', 'ox', 'herbs', 'ags'): 'args',
    })
    return selectorVariant[input]