from sLIEa import SINoALICE
uuid = "YOUR UUID"
client = SINoALICE("""
LOGIN ENCRYPT DATA
""", uuid)

ggt = client.getGuildGachaTop()
if not ggt['isJoinGuild']:
    input('NOT JOINED GUILD...')
    exit()
ggt = ggt['gachaInfo']
print('你目前擁有 %s 個轉蛋幣, 轉動一次耗費 %s 個轉蛋幣'%(ggt['itemNum'], ggt['price']))
#---------------------------------------------------------------------------------------
act = input('[cmd]\n==========\n轉動一次 -- a\n自動轉動 -- b\n==========\b執行指令:')
if act == 'a':
    if ggt['itemNum'] >= ggt['price']:
        print('[*]成功獲得: ',client.execGuildGacha(ggt['guildGachaMstId']))
    else:
        print('[*]轉蛋幣不足><')
elif act == 'b':
    c = 0
    while ggt['itemNum'] >= ggt['price']:
        print('[*]成功獲得: ',client.execGuildGacha(ggt['guildGachaMstId']))
        ggt['itemNum'] -= ggt['price']
        c += 1
    print('轉動完成! 共轉動 %s 次' % c)
else:
    pass


input('...')