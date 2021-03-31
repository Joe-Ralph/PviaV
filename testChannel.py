from time import sleep
from grammarChannel import GrammerChannel
import pyautogui


command = [
    "press control air",
    "def",
    "space",
    "camel hello world",
    "args",
    "press end",
    "colon",
    "enter",
    "press tab",
    "say print",
    "args",
    "quotes",
    "say hello world",
    "press end",
    "enter",
    "camel hello world",
    "args",
    "press end"
]

sleep(4.0)
for i in command:
    pyautogui.typewrite(GrammerChannel(i.lower().split()))