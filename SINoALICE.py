import asyncio
import msgpack
import os, json, requests, urllib, time, string, random

API_URL = 'https://line1-sdk-login.komoejoy.com'
headers = {
    'User-Agent': 'UnityRequest com.komoe.sinoalicegoogle 10.0.5 (LGE LGM-V300K Android OS 5.1.1 / API-22 (N2G47H/500190101))',
    'X-Unity-Version': '5.4.4f1'
}
payloads = {
  "payload": None,
  "requestid": None,
  "uuid": None,
  "userId": None,
  "sessionId": None,
  "actionToken": None,
  "access_token": None,
  "ctag": None,
  "actionTime": 131917203325430000
}
cookies = {}

def addHeaders(source):
    headerList={}
    headerList.update(headers)
    headerList.update(source)
    return headerList

def updatePayload(data):
    payloadList={}
    payloadList.update(payloads)
    payloadList['payload'].update(data)
    return payloadList

def id_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getNowTime():
    return int(time.time()*1000)

def urlEncode(url, path, params=[]):
    return url + path + '?' + urllib.parse.urlencode(params)

def testGetTimestamp():
    url = 'http://line1-gameinfoc.komoejoy.com/?operators=5&merchant_id=1&isRoot=0&server_id=920001&sdk_log_type=1&app_id=1115&support_abis=x86%2Carmeabi-v7a%2Carmeabi&net=4&sdk_ver=1.0.6&code=0&actionname=login&res=0&dp=720*1280&pf_ver=5.1.1&login_type=0&channel_id=1&uid=7448007&udid=HH1Kc0J7SH0fLhspVWdVZ1VlUmEFMlRsVSlVbF9qCDkMPg85DD4JaF9mVw%3D%3D&platform_type=3&ver=10.0.5&model=LGM-V300K&'
    r = requests.get(url, headers=headers, stream=True)
    print(r.headers['date'], '\n', r.text)
    res_time = r.headers['date']
    #time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    main_time = int(time.mktime(time.strptime(res_time,"%a, %d %b %Y %H:%M:%S GMT"))*1000)
    print(main_time)
    return main_time
    
def userInfo():
    params = {
        #sorry><
    }
    url = urlEncode(API_URL, '/api/client/user.info', params)
    r = requests.get(url, headers=headers, stream=True)
    print(r.status_code, '\n', r.text)

def getConfig():
    params = {
        #sorry><
    }
    url = urlEncode(API_URL, '/api/client/config', params)
    r = requests.get(url, headers=headers, stream=True)
    print(r.status_code, '\n', r.text)
#--------------------------------------
def getGuildData():
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/guild/guild_data'
#--------------------------------------
def findFriend():
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/input_pass_number'
    data = {
      "payload": {
        "friendPass": None
      }
    }
def addFriend():
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/relationship/register_new_friend_request'
    data = {
      "payload": {
        "targetUserId": None,
        "relationship": None,
        "relationShip": None
      }
    }
#--------------------------------------
def getNewMessage():
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/get_new_message'
    hr = addHeaders({
        'Content-Type': 'application/x-msgpack'
    })
    payloads['requestid'] = 'ce7c41ef9af7e052abe9361b5ad1a8d6'
    data = msgpack.packb(payloads)
    r = requests.post(url, headers=hr, data=data)
    if r.status_code == 200:
        res_data = r.content
        res = unpackData(res_data)
        print(res)
        #if res['payload']['newMessageList']:
        #    return res['payload']['newMessageList']
    else:
        res_data = r.content
        res = unpackData(res_data)
        print(res)
    return []

def getMessageList(roomId, lastMessageId=0):
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/chat/get_message_list'
    hr = addHeaders({
        'Content-Type': 'application/x-msgpack'
    })
    np = updatePayload({
        "roomId": roomId,
        "lastMessageId": lastMessageId
    })
    data = msgpack.packb(np)
    r = requests.post(url, headers=hr, data=data)
    if r.status_code == 200:
        res_data = r.content
        res = unpackData(res_data)
        if res['payload']['messages']:
            return res['payload']['messages']
    return []
#--------------------------------------
def userLogin(data):
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/alice_login'
    hr = addHeaders({
        'Content-Type': 'application/x-msgpack'
    })
    r = requests.post(url, headers=hr, data=data)
    if r.status_code == 200:
        res_data = r.content
        msg = msgpack.unpackb(res_data, use_list=False, raw=False)
        payloads['uuid'] = msg['payload']['uuid']
        payloads['userId'] = msg['payload']['userId']
        payloads['sessionId'] = msg['payload']['sessionId']
        cookies = r.cookies.copy()
        print('登入成功')
        return True
    return False
    
def getUserData():
    url = 'https://l13-prod-all-gs-user-ualice-tw.komoejoy.com/api/user/get_user_data'
    hr = addHeaders({
        'Content-Type': 'application/x-msgpack'
    })
    print(cookies)
    data = msgpack.packb(payloads)
    r = requests.post(url, headers=hr, data=data, cookies=cookies)
    if r.status_code == 200:
        res_data = r.content
        msg = msgpack.unpackb(res_data, use_list=False, raw=False)
        print(msg)
        return True
    return False
    
def unpackData(data):
    msg = msgpack.unpackb(data, use_list=False, raw=False)
    if msg['status'] == 200:
        if 'error' in msg:
            if msg['error']['code'] == 20002:
                #'Other device login'
                pass
            print(msg['error']['reason'])
            return False
        return msg
    else:
        print(msg)
        return False

client = userLogin("""
Input your encrypted verification data
""")
#print(getNewMessage())
#while client:
#    msgs = getNewMessage()
#    if msgs:
#        for msg in msgs:
#            msg_data = getMessageList(msg['roomId'], msg['lastMessageId'])
#            print(msg_data)
#    else:
#        print('null')