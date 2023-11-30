# sLIEa
[![LICENSE](https://img.shields.io/badge/license-BSD%203%20Clause-blue.svg "LICENSE")](https://github.com/fadhiilrachman/line-py/blob/master/LICENSE) [![Supported python versions: 3.x](https://img.shields.io/badge/python-3.x-green.svg "Supported python versions: 3.x")](https://www.python.org/downloads/) [![Chat on Discord](https://discordapp.com/api/guilds/466066749440393216/widget.png "Chat on Discord")](https://discord.gg/9dfectq)

*SINoALICE(TW ver.) Login API*
`Use this api maybe will ban account, please consider.`

----

## 2023 What'up
本庫一開始為公開的, 並在巴哈上有日誌參考:
- [我居然做了死亡愛麗絲(SINoALICE)的BOT...](https://home.gamer.com.tw/creationDetail.php?sn=4261795)
- [第二隻BOT的等級很母湯... - SINoALICE 死亡愛麗絲](https://home.gamer.com.tw/creationDetail.php?sn=4266277)
- [對於戰鬥&聊天系統的進步... - 死亡愛麗絲 SINoALICE](https://home.gamer.com.tw/creationDetail.php?sn=4272984)

簡單來說本庫是為了繁中伺服器(TW ver.)而做, 而其目的是為了學習:
- 了解遊戲架構與服務請求
- 遊戲機制與資料解析
- 遊戲副本連線運作機制(Socketio)

請求都以MsgPack做壓縮, 這是我第一次接觸msgpack, 在這五年來陸續接觸了5-6款遊戲也都是以magpack做壓縮, 這也包括了我目前正在製作的[D4DJ API](https://www.patreon.com/posts/d4dj-database-74413927?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link)

總體來說本庫對我收益頗大, 如今台服已經停止營運, 我又再次公開此庫給其他人研究
本庫端點均為**TW Only**, 在2024我還打算公開目前我還正在使用的[sLIEa_GW](https://github.com/WEDeach/sLIEa_GW)

台服與日服最大差異在於**沒有請求加密**, 只有簡單的MD5去做請求處理

## Requirement

The linepy module only requires Python 3. You can download from [here](https://www.python.org/downloads/). 

## How to use
1. Install and start mitmproxy
2. Start Android emulator by using command: ```emulator -avd "YOUR_AVD_NAME" -http-proxy 127.0.0.1:8080```(You can also use your phone and set up a wifi proxy)
3. Open browser and navigate to http://mitm.it/ to trust the certificate on your emulator.
4. Login to SINoALICE(TW ver.) and until you see the main lobby
5. Go to http://127.0.0.1/8081 and filter the sniffered traffic by ```alice_login```
6. You can find `LOGIN ENCRYPT DATA` on the "Requests" tab (make the view mode to RAW and copy it, the content should start with "\x89")
8. Replace it with the example string in 'example/getUserData.py' and make sure it is wrapped by `"""`.
9. Run!
