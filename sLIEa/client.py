# -*- coding: utf-8 -*-
from .server import Server
from .lie import API
from .models import Models

class SINoALICE(API, Models):
    isLogin = False
    
    def __init__(self, encryptedData, uuid=None, loginVer=None):
        self.server = Server()
        API.__init__(self)
        self.server.setHeadersWithDict({
            'User-Agent': 'UnityRequest com.komoe.sinoalicegoogle 10.0.7 (LGE LGM-V300K Android OS 5.1.1 / API-22 (N2G47H/500190101))',
            'X-Unity-Version': '5.4.4f1'
        })
        if encryptedData is not None:
            if uuid is None:
                print('[!]You need to get Uuid, you can capture it from the URL in other requests.')
                #Even if I use the wrong uuid, the server still accepts my request
            else:
                if loginVer != None:
                    self.userLogin(encryptedData, uuid, loginVer)
                else:
                    self.userLogin(encryptedData, uuid)
                self.__initAll()

    def __initAll(self):
        Models.__init__(self)
        
        self.uuid = None
        self.SessionId = None
        
        self.userData = self.getUserData()
        self.itemDataList = []
        self.cardDataList = []
        self.characterDataList = []
        self.deckDataList = []
        self.jobDataList = []
        self.costumeDataList = []
        self.InGameChat = {
            'roomId': None,
            'room_id': None
        }
        self.mpInfo = self.getMyPageInfo()
        self.newMessageList = self.mpInfo['newMessageList']
        self.connection = {}