from platform import release
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


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
    return ' '.join(listwords)


def ProgrammingKeywords():
    keywordList = {
        'and' : 'and',
        'as':'as',
        'assert':'assert',
        'break':'break',
        'class' : 'class',
        'continue' : 'continue',
        'def' : 'def',
        'del' : 'del',
        'elif' : 'elif',
        'else' :'else',
        'except':'except',
        'false':'False',
        'finally':'finally',
        'for':'for',
        'from':'from',
        'global':'global',
        'if':'if',
        'import':'import',
        'in':'in',
        'is':'is',
        'lambda':'lambda',
        'none':'None',
        'nonlocal':'nonlocal', # ! dual pass Word
        'not':'not',
        'or':'or',
        'pass':'pass',
        'raise':'raise',
        'return':'return',
        'true':'True',
        'try':'try',
        'while':'while',
        'with':'with',
        'yield':'yield',
        'colon':':',
    }

def Delete(keywords):
    pass

def Arguments(keywords):
    return "()"
# --------------------------------------------------------------------------------------------------------------------------------------------


def GrammerChannel(listwords):
    print(listwords)
    possibleCommands = {
        'press': KeyCombos,
        'select': Select,
        'kabab': Kabab,
        'camel': Camel,
        'capital': Capital,
        'say': Plaintext,
        'delete': Delete,
        'args':Arguments,
    }
    function = possibleCommands.get(SelectorVaraintHandler(listwords[0]), ProgrammingKeywords)
    # function = possibleCommands.get(listwords[0],plaintext)
    return function(listwords)

# Select(['select','line'])
# print(Kabab(['kabab','hello','world']))
# print(Camel(['','hello','world','niggas']))

def SelectorVaraintHandler(input):
    variant = {
        ['camel','kamel'] : 'Camel',
    }
    return input # ! change later to non-default function after code defnittion
