# the latest version of this library has some problems, use v1.2.2
# pip install playsound==1.2.2
from playsound import playsound

def sound(soundAddress):
    try:
        playsound(soundAddress, block=False)
    except:
        pass
