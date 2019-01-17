# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint

import json, shutil, time, os, base64, tempfile
    
class Models(object):
        
    def __init__(self):
        pass

    def log(self, text):
        try:
            print("[%s] %s" % (str(datetime.now()), text))
        except:
            print("[%s] LOG ERROR" % (str(datetime.now())))

    def saveFile(self, path, raw):
        with open(path, 'wb') as f:
            shutil.copyfileobj(raw, f)

    def deleteFile(self, path):
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False

    def ToFileTimeUtc(self, current=False):
        tick = (datetime.utcnow() - datetime(1, 1, 1)).total_seconds() * 10000000
        if current:
            return tick
        if tick < 504911232000000000:
            raise
        return int(tick - 504911232000000000)

    def getStamina(self, userData):
        if userData['stamina'] >= userData['staminaMax']:
            return userData['stamina']
        tick = (datetime.utcnow() - datetime(1, 1, 1)).total_seconds() * 10000000
        
        totalSeconds = (datetime.now() - datetime.fromtimestamp(userData['staminaUpdatedTime'])).total_seconds()
        num = int(totalSeconds / 180);
        return userData['stamina'] + num