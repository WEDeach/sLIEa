from sLIEa import SINoALICE
uuid = "YOUR UUID"
client = SINoALICE(uuid, """
LOGIN ENCRYPT DATA
""")

if client.mpInfo['presentNum'] > 0:
    print('共有%s件禮物...即將自動領取...'%client.mpInfo['presentNum'])
    pds = [pd['presentDataId'] for pd in client.getPresentData()]
    print('成功領取%s件禮物' % len(client.gainPresent(pds)))
else:
    print('[*]Nothing')
input('點擊任意鍵...')