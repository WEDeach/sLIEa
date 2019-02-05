# -*- coding: utf-8 -*-
from .config import Config
import json, requests, urllib, hashlib
import msgpack

class Server(Config):
    _session = requests.session()
    Headers = {}

    def __init__(self):
        self.Headers = {}
        Config.__init__(self)

    def urlEncode(self, url, path, params=[]):
        return url + path + '?' + urllib.parse.urlencode(params)

    def getJson(self, url, allowHeader=False, Headers={}):
        if allowHeader is False:
            return json.loads(self._session.get(url).text)
        else:
            print(Headers)
            res = self._session.get(url, headers=Headers)
            print(res.status_code)
            return json.loads(res.text)

    def setHeadersWithDict(self, headersDict):
        self.Headers.update(headersDict)

    def setHeaders(self, argument, value):
        self.Headers[argument] = value

    def addHeaders(self, source):
        headerList={}
        headerList.update(self.Headers)
        headerList.update(source)
        return headerList

    def addPayload(self, source):
        payloadList={}
        payloadList.update(self.payloads)
        if payloadList['payload'] is None:
            payloadList['payload'] = {}
        payloadList['payload'].update(source)
        return payloadList

    def optionsContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.options(url, headers=headers, data=data)

    def postContent(self, url, data=None, files=None, headers=None):
        if headers is None:
            headers=self.Headers
        return  self._session.post(url, headers=headers, data=data, files=files)

    def getContent(self, url, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.get(url, headers=headers, stream=True)

    def deleteContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.delete(url, headers=headers, data=data)

    def putContent(self, url, data=None, headers=None):
        if headers is None:
            headers=self.Headers
        return self._session.put(url, headers=headers, data=data)

    def CalRequestId(self, curReqId=None):
        if curReqId != None:
            self.payloads['requestid'] = hashlib.md5((curReqId + "DW0-KLO-C7").encode('utf8')).hexdigest()

    def unpackData(self, msgpackData, act=True):
        msg = msgpack.unpackb(msgpackData, use_list=False, raw=False)
        if msg['status'] == 200:
            if act:
                self.CalRequestId(msg['requestid'])
            if 'errors' in msg:
                if msg['errors'][0]['code'] == 1009:
                    return False
                elif msg['errors'][0]['code'] == 2002:
                    self.isLogin = False
                elif msg['errors'][0]['code'] == 20002:
                    self.isLogin = False
                print(msg['errors'][0]['code'],':',msg['errors'][0]['reason'])
                return {}
            else:
                if 'payload' not in msg:
                    print('not found payload:', msg)
            return msg
        else:
            print(msg)
            return False
            
    def SetupSocket(self, reflectorType, reflectorServerId, roomId):
        print("#SetupSocket start. roomId:" + roomId)
        reflectorUrl = ''
        #connection_url = '/march'
        #/json/quest_battle/
        
    def EmitServer(self, roomId, redirectUrl, payload):
        #if self.socket != None:
		# jsonData = {}
        # jsonData["request_timestamp"] = time.time()
		# jsonData["uuid"] = self.uuid
		# jsonData["room_id"] = roomId
		# jsonData["payload"] = payload
		# jsonData2 = {}
        # jsonData["Accept"] = "application/json"
		# jsonData["Uuid"] = self.uuid
		# if (str(payload) != '')
		# {
			# jsonData2["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8";
		# }
		# jsonData["custom_headers"] = jsonData2;
		# jsonData["redirect_url"] = redirectUrl;
		# EmitByType(EmitType.server, jsonData);
        pass