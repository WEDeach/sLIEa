# -*- coding: utf-8 -*-
from .server import Server
from .lie import API
from .models import Models

class SINoALICE(API, Models):
    isLogin = False
    
    def __init__(self, uuid, encryptedData=None):
        self.server = Server()
        API.__init__(self)
        self.server.setHeadersWithDict({
            'User-Agent': 'UnityRequest com.komoe.sinoalicegoogle 10.0.5 (LGE LGM-V300K Android OS 5.1.1 / API-22 (N2G47H/500190101))',
            'X-Unity-Version': '5.4.4f1'
        })
        if encryptedData is not None:
            self.userLogin(uuid, encryptedData)
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