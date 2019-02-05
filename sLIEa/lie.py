# -*- coding: utf-8 -*-
from random import randint
import json, ntpath, time, os
import asyncio
import traceback
import msgpack
import hashlib

def loggedIn(func):
    def checkLogin(*args, **kwargs):
        if args[0].isLogin:
            return func(*args, **kwargs)
        else:
            print('Login failed')
    return checkLogin

class User(object):

    def __init__(self):
        pass

    def userLogin(self,encryptedData, uuid):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/alice_login'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        r = self.server.postContent(url, headers=hr, data=encryptedData)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            self.SessionId = msg['payload']['sessionId']
            self.uuid = uuid
            self.server.payloads['uuid'] = uuid
            self.server.payloads['userId'] = msg['payload']['userId']
            self.server.payloads['sessionId'] = msg['payload']['sessionId']
            self.server.payloads['actionTime'] = self.ToFileTimeUtc()
            self.isLogin = True
            print('登入成功')
            return True
        print('Login failed!')
        return False

    @loggedIn
    def getUserData(self, userId=None):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/user/get_user_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        if userId is not None:
            np = self.server.addPayload({
                "userId": int(userId)
            })
            data = msgpack.packb(np)
        else:
            data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            if self.server.payloads['uuid'] in str(msg['payload']['userData']):
                print(msg['payload']['userData'].keys())
            return msg['payload']['userData']
        return False
        
    @loggedIn
    def getConfig(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/config/get_config'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']
        return False

    @loggedIn
    def getMyPageInfo(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/my_page/get_my_page_info_for_alice_11'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']
        return False

    @loggedIn
    def generatePassNumber(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/generate_pass_number'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']['passNumbe']
        return False

    @loggedIn
    def inputPassNumber(self, pn):
        if len(str(pn)) < 5:
            print('e: ')
            return
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/input_pass_number'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "friendPass": int(pn)
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']
        return False

    @loggedIn
    def addFriend(self, targetUserId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/register_new_friend_request'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "targetUserId": targetUserId,
            "relationship": None,
            "relationShip": None
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            if "payload" not in msg:
                print(msg)
                return {}
            return msg['payload']
        return False

    @loggedIn
    def removeFriend(self, targetUserId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/delete_friend_request'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "targetUserId": targetUserId,
            "relationship": None,
            "relationShip": None
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']
        return False

    @loggedIn
    def geCharacterDataList(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/character/get_character_data_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            self.deckDataList = msg['payload']['deckDataList']
            return msg['payload']
        return False
        
    @loggedIn
    def getDeckDataList(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/deck/get_deck_data_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            self.deckDataList = msg['payload']['deckDataList']
            return msg['payload']['deckDataList']
        return False

    @loggedIn
    def getDeckDetail(self, deckDataId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/deck/get_deck_detail_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "deckDataId": deckDataId
          })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']['deckDetailDataList']
        return False

    @loggedIn
    def getRecommendDeck(self, characterDataId, isSub=False, weaponCardDataIds=[], protectorCardDataIds=[], nightMareCardDataIds=[], subWeaponCardDataIds=[], subProtectorCardDataIds=[], subNightMareCardDataIds=[], attribute=0, autoMode=False):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/deck/get_recommend_deck_for_alice'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "attribute": attribute,
            "characterDataId": characterDataId,
            "isSubDeck": isSub,
            "weaponCardDataIds": weaponCardDataIds,
            "protectorCardDataIds": protectorCardDataIds,
            "nightMareCardDataIds": nightMareCardDataIds,
            "subWeaponCardDataIds": subWeaponCardDataIds,
            "subProtectorCardDataIds": subProtectorCardDataIds,
            "subNightMareCardDataIds": subNightMareCardDataIds
          })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            res = msg['payload']
            if autoMode:
                res = self.getRecommendDeck(characterDataId, True, res['weaponCardDataIds'],res['protectorCardDataIds'],res['nightMareCardDataIds'])
            return res
        return False

    @loggedIn
    def updateDeckData(self, deckDataId, characterDataId, weaponCardDataIds=[], protectorCardDataIds=[], nightMareCardDataIds=[], subWeaponCardDataIds=[], subProtectorCardDataIds=[], subNightMareCardDataIds=[], attribute=0, deckName="裝備配置"):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/deck/update_deck_card_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "deckDataId": deckDataId,
            "characterDataId": characterDataId,
            "deckName": deckName,
            "weaponCardDataIds": weaponCardDataIds,
            "protectorCardDataIds": protectorCardDataIds,
            "nightMareCardDataIds": nightMareCardDataIds,
            "subWeaponCardDataIds": subWeaponCardDataIds,
            "subProtectorCardDataIds": subProtectorCardDataIds,
            "subNightMareCardDataIds": subNightMareCardDataIds
          })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            return msg['payload']
        return False

    @loggedIn
    def setProfileComment(self, comment):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/profile/set_comment'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "comment": comment
          })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            msg = self.server.unpackData(r.content)
            if msg['payload']['success']:
                self.userData = msg['payload']['userData']
            return msg['payload']
        return False

class Mission(object):

    def __init__(self):
        pass

    @loggedIn
    def getMissionDataRecordList(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/mission/get_mission_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']['missionDataRecordList']
        return []

    @loggedIn
    def getMissionReward(self, completedMissionList):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/mission/get_mission_reward'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "distributeMstId": [completedMissionList]
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                self.userData = res['payload']['userData']
                return res['payload']
        return []

    @loggedIn
    def checkAchievement(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/achievement/check_achievement'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "targetUserId": 0, #can see other player?
            "sceneName": "MissionTop"
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']['accomplishList']
        return []
    def getMissionMstIdRecordData(self, missionMstId):
        for mmr in self.missionMstRecord:
            if mmr['missionMstId'] == missionMstId:
                return mmr
        return False

    def getCompletedMissionsReward(self, isCompleted=[]):
        notReward = []
        for mdr in self.missionDataRecord:
            mmrd = self.getMissionMstIdRecordData(mdr['missionMstId'])
            if mmrd and mmrd['conditionsCount'] != 0:
                if mdr['count'] >= mmrd['conditionsCount']:
                    if mdr['status'] != 1:
                        isCompleted.append(mdr['missionMstId'])
                        self.getMissionReward(mdr['missionMstId'])
                    else:
                        notReward.append(mdr['missionMstId'])
        self.missionDataRecord = self.getMissionDataRecordList()
        if notReward:
            isCompleted = self.getCompletedMissionsReward(isCompleted)
        return isCompleted

class Chat(object):
    def __init__(self):
        pass

    @loggedIn
    def getNewMessage(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/get_new_message'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']['newMessageList']:
                return res['payload']['newMessageList']
        return []

    @loggedIn
    def getMessageList(self, roomId, lastMessageId=0):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/get_message_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "roomId": roomId,
            "lastMessageId": lastMessageId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']['messages']:
                return res['payload']['messages']
        return []

    @loggedIn
    def getFixedMessageList(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/get_fixed_message_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            return res['payload']
        return []
        
    @loggedIn
    def joinChatRoom(self, roomId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/join_room'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "roomId": roomId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            return res['payload']
        return []

    @loggedIn
    def sendTextMessage(self, roomId, data, messageType=0):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/send_text_message'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "roomId": roomId,
            "data": data,
            "messageType": messageType,
            'status': 2
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=json.dumps(self.server.payloads))
        if r.status_code == 200:
            print(r.text)
        else:
            print(r.text)
        return []

    @loggedIn
    def getLastMessageId(self, roomId):
        mid = 0
        for msg in self.newMessageList:
            if msg['roomId'] == roomId:
                mid = msg['lastMessageId']
        return mid

class Present(object):
    def __init__(self):
        pass

    @loggedIn
    def getPresentData(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/present/get_present_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                #and res['payload']['gainPresentData'] :))
                return res['payload']['presentData']
        return []

    @loggedIn
    def gainPresent(self, presentDataIds):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/present/gain_present'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "presentDataId": presentDataIds
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                self.userData = res['payload']['userData']
                self.itemDataList = res['payload']['itemDataList']
                self.cardDataList = res['payload']['cardDataList']
                self.characterDataList = res['payload']['characterDataList']
                self.jobDataList = res['payload']['jobDataList']
                self.costumeDataList = res['payload']['costumeDataList']
                return res['payload']['gainList']
        return []

class Clean(object):
    def __init__(self):
        pass

    @loggedIn
    def checkCleaning(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/cleaning/check'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []
        
    @loggedIn
    def cleaningRetire(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/cleaning/retire'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def startCleaning(self, cleaningType=1):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/cleaning/start'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "cleaningType": cleaningType
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def endCleaning(self, remainTime, currentWave, getAp, getExp, getEnemyDown, isEnd=False):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/cleaning/end'
        if not isEnd:
            url += '_wave'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "remainTime": remainTime,
            "currentWave": currentWave,
            "getAp": getAp,
            "getExp": getExp,
            "getEnemyDown": getEnemyDown
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if not res:
                self.cleaningRetire()
                raise Exception("EndCleaning Failed!")
            elif 'payload' in res:
                self.userData = res["payload"]["userData"]
                return res['payload']
        return []

class Quest(object):
    def __init__(self):
        pass

    @loggedIn
    def getAliceAreaMap(self, questMapMstId=1):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_alice_area_map'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questMapMstId": questMapMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def getAliceStageList(self, questAreaMstId=1):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_alice_stage_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questAreaMstId": questAreaMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']['stageList']
        return []
        
    @loggedIn
    def getAliceEventAreaList(self, questAreaMstId=1):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_alice_event_area_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questAreaMstId": questAreaMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                '''{
                    "questAreaMstId": 160,
                    "questScheduleMstId": 40,
                    "areaStatus": 9,
                    "questCampaign": false,
                    "totalCount": 0,
                    "clearCount": 0,
                    "remainTime": 1402132
                }
                to getAliceStageList(160) # 160 = questAreaMstId
                '''
                return res['payload']['eventAreaList']
        return []

    @loggedIn
    def getStageAllData(self, questStageMstId=1, questAreaMstId=1):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_stage_all_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questStageMstId": questStageMstId,
            "questAreaMstId": questAreaMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def getUnitQuestList(self, joinStatus):
        '''
        Disable,
        Anyone, 1
        GuildMemberAndFriend, 
        GuildMember, 3
        Friend, 4
        SpecificFriend
        '''
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_unit_quest_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "joinStatus": joinStatus
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                '''
                "battleNum": 23,
                "questDataId": 34386005,
                "questMapMstId": 1,
                "questAreaMstId": 15,
                "questStageMstId": 141,
                "questLevel": 1,
                "questUseStamina": 6,
                "userId": 1007199625,
                "characterMstId": 2,
                "name": "玥兒",
                "level": 6,
                "jobRoleType": 5,
                "joinNum": 1,
                "remainTime": 583,
                "stageBossEnemyId": 6,
                "stageBossResourceName": "",
                "stageBossIconResourceName": "",
                "stageBossAssetBundleName": "enemy/1",
                "stageBossAttribute": 3
                '''
                return res['payload']['unitQuestStageList']
        return []
    
    @loggedIn
    def checkQuestUnit(self, battleNum, questDataId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/check_quest_unit'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "battleNum": 23,
            "questDataId": 34386005
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if not res:
                return False
            else:
                return True
        return False
    
    
    @loggedIn
    def initBattleStage(self, questStageMstId, deckDataId, joinStatus=1, joinType=0):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/initialize_stage'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questStageMstId": questStageMstId,
            "joinStatus": joinStatus,
            "deckDataId": deckDataId,
            "joinType": joinType
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                self.userData = res['payload']['userData']
                return res['payload']['questRoomData']
        return []

    @loggedIn
    def getBattleInfo(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/get_info'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' not in res:
                return False
            if res['payload']:
                if res['payload']['general']['time'] > res['payload']['general']['endTime']:
                    print('TIME OVER!')
                    self.retireBattle()
                    return False
                return res['payload']
        return []

    @loggedIn
    def getBattleCurrentDeckData(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/get_current_deck_data'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def getBattleGetArtList(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/get_art_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    def getQuestMapName(self, questMapMstId):
        for qmmr in self.aliceQuestMapMstRecord:
            if qmmr['questMapMstId'] == questMapMstId:
                return qmmr['name']

    def getQuestAreaName(self, questAreaMstId):
        for qmmr in self.aliceQuestAreaMstRecord:
            if qmmr['questAreaMstId'] == questAreaMstId:
                return qmmr['name']
    
    def getQuestStageName(self, questStageMstId):
        for qmmr in self.questStageMstRecord:
            if qmmr['questStageMstId'] == questStageMstId:
                return qmmr['name']
                

    @loggedIn
    def getBattleWaveStart(self, currentQuestWaveMstId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/wave_start'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "currentQuestWaveMstId": currentQuestWaveMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []
        
    @loggedIn
    def joinBattleStage(self, battleNum, questDataId, deckDataId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/join_stage'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "battleNum": battleNum,
            "questDataId": questDataId,
            "deckDataId": deckDataId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                return res['payload']
            else:
                return False
        return []
        
    @loggedIn
    def retireBattle(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/user_retire'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

    @loggedIn
    def changeAiMode(self, isAi=0, mode='quest_battle'):
        #mode : quest_battle or gvg
        if mode in ['quest_battle', 'gvg']:
            url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/%s/change_ai_mode' % mode
        else:
            return False
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "isAi": isAi
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                #res['payload']['success'] == True else res['payload']['message']
                return res['payload']
        return []

    @loggedIn
    def battleWaveClear(self, currentQuestWaveMstId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/wave_clear'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "currentQuestWaveMstId": currentQuestWaveMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                #res['payload']['success'] == True else res['payload']['message']
                return res['payload']
        return []

    @loggedIn
    def FinalizeStageForUser(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest_battle/finalize_stage_for_user'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                #res['payload']['success'] == True else res['payload']['message']
                return res['payload']
        return []

    @loggedIn
    def getQuestResult(self, questDataId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/quest/get_result'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "questDataId": questDataId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                #res['payload']['success'] == True else res['payload']['message']
                self.userData = res['payload']['userData']
                return res['payload']
        return []

    """ GvG """

    @loggedIn
    def getGvgInfo(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gvg/get_info'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            return res['payload']
        return []
        
    @loggedIn
    def getGvgViewParams(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gvg_out_battle/get_gvg_view_params'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            return res['payload']
        return []

class Gacha(object):
    def __init__(self):
        pass

    @loggedIn
    def getGachaTop(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gacha/get_gacha_top'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']['gachaList']
        return []

    @loggedIn
    def getGuildGachaTop(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gacha/get_guild_gacha_top'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                return res['payload']
        return []

    @loggedIn
    def getGuildGachaRewardList(self, guildGachaMstId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gacha/get_guild_gacha_reward_list'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "guildGachaMstId": guildGachaMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                return res['payload']
        return []

    @loggedIn
    def execGuildGacha(self, guildGachaMstId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gacha/guild_gacha_exec'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "guildGachaMstId": guildGachaMstId
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                return res['payload']
        return []

    @loggedIn
    def execGacha(self, gachaMstId, gachaType):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/gacha/gacha_exec'
        hr = self.server.addHeaders({
            'Content-Type': 'application/x-msgpack'
        })
        np = self.server.addPayload({
            "gachaMstId": gachaMstId,
            "gachaType": gachaType
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if res['payload']:
                return res['payload']
        return []

class Guild(object):
    def __init__(self):
        pass
    
    @loggedIn
    def recommendGuildSearch(self, mstId):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/guild/recommend_guild_search'
        hr = {
            'Content-Type': 'application/x-msgpack'
        }
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                '''
                "guildDataId": 9908,
                "guildName": "未隸屬公會",
                "guildIdentifierId": "nw44u6",
                "guildDescription": "**現在只招收綜合值75000以上的新成員，不符合資格的新成員會被即時解除**",
                "guildMasterUserId": 1000989295,
                "maxMember": 15,
                "joinMember": 14,
                "guildExp": 5055127,
                "guildLevel": 38,
                "guildRank": 4,
                "guildPoint": 5055127,
                "gvgWin": 26,
                "gvgLose": 11,
                "gvgDraw": 0,
                "gvgTimeType": 128,
                "beforeGvgTimeType": 0,
                "isAutoAccept": true,
                "autoExpulsionType": 0,
                "isGvgPushCall": false,
                "gvgPushCallComment": "是時候出場了！！",
                "currentGuildTitleMstId": 0,
                "subscriptionPowerType": 8,
                "subscriptionGvgJoinType": 2,
                "subscriptionActionType": 15,
                "subscriptionStyleType": 3,
                "subscriptionComment": null
                '''
                return res['payload']['guildDataList']
        return []
        
    @loggedIn
    def createGuild(self, guildName, guildDescription):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/guild/create_guild'
        hr = {
            'Content-Type': 'application/x-msgpack'
        }
        np = self.server.addPayload({
            "guildName": guildName,
            "guildDescription": guildDescription
        })
        data = msgpack.packb(np)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res and res['payload'].get('guildDataId') != None:
                return res['payload']['guildDataId']
        return False
        
    @loggedIn
    def guildData(self):
        url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/guild/create_guild'
        hr = {
            'Content-Type': 'application/x-msgpack'
        }
        data = msgpack.packb(self.server.payloads)
        r = self.server.postContent(url, headers=hr, data=data)
        if r.status_code == 200:
            res = self.server.unpackData(r.content)
            if 'payload' in res:
                return res['payload']
        return False

class API(User, Chat, Mission, Present, Clean, Quest, Gacha, Guild):
    def __init__(self):
        User.__init__(self)
        Chat.__init__(self)
        Present.__init__(self)
        Mission.__init__(self)
        Clean.__init__(self)
        Quest.__init__(self)
        Gacha.__init__(self)
        #Mst.__init__(self)
        Guild.__init__(self)