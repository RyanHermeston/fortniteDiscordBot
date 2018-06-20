import discord
import sys
import requests


#discord bot token here
TOKEN = 'XXXXXXXXXX'


#fortnite tracker api key here
key = {'TRN-Api-Key':"XXXXXXXXXXX"}


client = discord.Client()

commands = ['!help','!stats','!winlist','!kdlist','!statsxb','!statsps']
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(commands[0]):

        msg = '''

        This bot is still under construction.\n
        Usage: !stats, !help, !kdlist and !winlist\n
        !stats `gamertag`   --- gives pc stats\n
        !winlist `gamertag`,`gamertag`,`gamertag`  pc only \n
        !kdlist `gamertag`,`gamertag`,`gamertag`  pc only\n
        !statsxb `gamertag`  --- xbox stats\n
        !statsps `gamertag`  --- psn stats\n
        Message @ryan.h for info

        '''

        await client.send_message(message.channel,msg)
    if message.content.split()[0]==commands[1]:

        name = ''
        '''
        for i in range(len(message.content.split())):
            if i == 0:
                continue
            name+=message.content.split()[i]+" "
        '''
        #name should be extraced differently, above method is trash
        #the data given is a string so we could just slice from the command length to end of string
        name+=message.content[len(commands[1])+1:]
        #this way of handling names is cleaner to read and elmininates an uneccesary for loop

        URL = "https://api.fortnitetracker.com/v1/profile/pc/"+name
        try:
            r = requests.get(url = URL,headers=key)
            data = r.json()


            overallKd = data['lifeTimeStats'][11]['value']
            overallWins = data['lifeTimeStats'][8]['value']
            overallMatchesPlayed = data['lifeTimeStats'][7]['value']
            overallWinrate = round(int(overallWins)/int(overallMatchesPlayed)*100,2)
            overallWinrate=  str(overallWinrate)
        except:
            msg = 'Failed to gather any stats for '+name
            await client.send_message(message.channel,msg)
            return
            #overall data above, current below, quick and dirty but is close to accurate
        try:
            currKills = int(data['stats']['curr_p9']['kills']['value'])+int(data['stats']['curr_p10']['kills']['value'])+int(data['stats']['curr_p2']['kills']['value'])


            s1 = data['stats']['curr_p2']['matches']['value']
            s2 = data['stats']['curr_p9']['matches']['value']
            s3 = data['stats']['curr_p10']['matches']['value']
            currMatches = int(s1)+int(s2)+int(s3)

            currWins = str(int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])+int(data['stats']['curr_p10']['top1']['value']))

            currWinRate =int(round(((int(currWins)/int(currMatches)) * 100),0))

            currKd = round(currKills/(currMatches-int(currWins)),2)
            #vars are overallWinrate,matches,overallWins,overallKd
            #print(str(currWinRate)+'%\n'+str(currMatches)+'\n'+str(currWins)+'\n'+str(currKd))
        except:

            msg = 'rare/new player info incomplete\n'+name+'\n'

            msg+="kd: "+overallKd+'\n'+"wins: "+overallWins+'\n'+"matches: "+overallMatchesPlayed+'\n'+"winrate: "+overallWinrate+"%\n--------------\n"

            try:

                matches3=int(data['stats']['curr_p2']['matches']['value'])+int(data['stats']['curr_p9']['matches']['value'])

                k3=int(data['stats']['curr_p2']['kills']['value'])+int(data['stats']['curr_p9']['kills']['value'])

                w3=int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])

                wr3 =int(round(((int(w3)/int(matches3)) * 100),0))

                kd3= round(k3/(matches3-int(w3)),2)

                msg+="kd: "+str(kd3)+'\n'+"wins: "+str(w3)+'\n'+"matches: "+str(matches3)+'\n'+"winrate: "+str(wr3)+"%\n--------------\n"
            except:

                m2=data['stats']['curr_p9']['matches']['value']

                k2=data['stats']['curr_p9']['kills']['value']

                w2=data['stats']['curr_p9']['top1']['value']

                wr2 =int(round(((int(w2)/int(m2)) * 100),0))

                kd2 = round(int(k2)/(int(m2)-int(w2)),2)

                msg+="kd: "+str(kd2)+'\n'+"wins: "+str(w2)+'\n'+"matches: "+str(m2)+'\n'+"winrate: "+str(wr2)+"%\n--------------\n"

            await client.send_message(message.channel,msg)
            return

        try:




            msg = name+'\n'


            cols = ['','','','','']
            cols[0] = 'Overall:'.center(0) + 'Current:'.rjust(33)
            cols[1] = str(('kd: '+overallKd).center(0)+('kd: '+str(currKd)).center(57))

            cols[2]= str(('wins: '+overallWins).center(0)+('wins: '+str(currWins)).center(54))
            cols[3]= str(('matches: '+overallMatchesPlayed).center(0)+('matches: '+str(currMatches)).center(39))
            cols[4]= str(('winrate: ' +overallWinrate+'%').center(0)+('winrate: '+str(currWinRate)+'%').center(38))
            for i in range(len(cols)):
                msg+='\n'+cols[i]

            #CURRENT FORMAT
            '''
            wsg = ''
            coals = ['','','','','']
            coals[0] ='Overall:','Current:'
            coals[1]='kd: '+str(overallKd) , 'kd: '+str(currKd)
            coals[2]='wins: '+str(overallWins),'wins: '+str(currWins)
            coals[3]='matches:'+str(overallMatchesPlayed),'matches:'+str(currMatches)
            coals[4]='winrate: '+str(overallWinrate)+'%','winrate: '+str(currWinRate)+'%'
            col_width = max(len(word) for row in coals for word in row)+2 # padding

            for row in coals:
                wsg+= ("".join(word.ljust(col_width) for word in row))+'\n'

            msg+=wsg
            '''

            '''
            RETIRED
            overList = [overallKd,overallWins,overallMatchesPlayed,overallWinrate+'%',]
            currList = ['\t'+str(currKd),'\t'+str(currWins),str(currMatches),str(currWinRate)+'%',]

            descList = ['kd:  ','wins:','matches:','winrate:']
            msg+='Overall:\t\t\t' + 'Current:'+'\n'
            for e,i,j in zip(descList,overList,currList):
                msg +=('{} {} \t\t\t{}'.format(e,i,j))+'\n'
            '''
            currKd = float(currKd)

            if (currKd) <= 1.0:
                msg+= '\nstatus: no skin'
            elif (currKd) >= 1.0 and currKd<=2.0:
                msg+= '\nstatus: Rust Lord'
            elif (currKd) >= 2.0 and currKd <=3.0:
                msg+= '\nstatus: Dark Knight'
            elif (currKd) >= 3.0:
                msg+='\nstatus: Streamer'
            else:
                msg+= '\nstatus: no idea ask Ryan'


        except:
            msg = 'Failed during msg creation'
        await client.send_message(message.channel,msg)

    if message.content.split()[0]==commands[2]:
        name,msg,delim = '','',','
        namechunk = ''
        urls,wins=[],[]
        snames = []
        fnames = []
        splitnames,finalnames=  [],[]
        winDic ={}
        ustr = "https://api.fortnitetracker.com/v1/profile/pc/"
        skip = message.content[0:8]

        if delim not in message.content:
            msg = 'separate names with commas'
            await client.send_message(message.channel,msg)
            return
        else:
            names = message.content[len(message.content.split()[0])+1:].split(',')
            for i in names:
                snames.append(i.split())
            for i in snames:
                if len(i)>1:
                    for j in range(len(i)-1):
                        i[j]+=' '
            for i in snames:
                if len(i)>1:
                    namechunk = ''
                    for j in i:
                        namechunk+=j
                    fnames.append(namechunk)
                else:
                    namechunk = ''
                    for j in i:
                        namechunk+=j
                    fnames.append(namechunk)
            for i in fnames:

                urls.append(ustr+i)

        for i in range(len(urls)):

            try:
                r = requests.get(url = urls[i],headers=key)
                data = r.json()
                wins.append(data['lifeTimeStats'][8]['value'])
            except:
                wins.append('N/A')

        for i in range(len(wins)):
            winDic[fnames[i]]=wins[i]
        #sorts by second item of dict, which is value, first is key
        soDict = sorted(winDic.items(),key= lambda dic: (int(dic[1])),reverse = True)
        #sorted returns a list, reason for no .items() after newly sorted
        for k,v in soDict:
            msg+=k+': '+v+'\n'

        topWins = next(iter(soDict))
        msg+=str(topWins[0])+' has bragging rights'
        '''
        sDict = sorted(kdDic.items(),key= lambda x: (float(x[1])),reverse = True)
        for k,v in sDict:
            msg+=k+': '+v+'\n'


        topKd = next(iter(sDict))
        msg+=str(topKd[0])+' is better than you all'
        '''

        await client.send_message(message.channel,msg)


    if message.content.split()[0]==commands[3]:
        name,msg,delim = '','',','
        urls,kds=[],[]
        snames,fnames = [],[]
        namechunk = ''
        kdDic = {}
        ustr = "https://api.fortnitetracker.com/v1/profile/pc/"
        skip = message.content[0:8]

        if delim not in message.content:
            msg = 'separate names with commas'
            await client.send_message(message.channel,msg)
            return
        else:
            names = message.content[len(message.content.split()[0])+1:].split(',')
            for i in names:
                snames.append(i.split())
            for i in snames:
                if len(i)>1:
                    for j in range(len(i)-1):
                        i[j]+=' '
            for i in snames:
                if len(i)>1:
                    namechunk = ''
                    for j in i:
                        namechunk+=j
                    fnames.append(namechunk)
                else:
                    namechunk = ''
                    for j in i:
                        namechunk+=j
                    fnames.append(namechunk)

            for i in fnames:

                urls.append(ustr+i)

        for i in range(len(urls)):

            try:
                r = requests.get(url = urls[i],headers=key)
                data = r.json()
                kds.append(data['lifeTimeStats'][11]['value'])
            except:
                kds.append('N/A')

        #for i in range(len(kds)):
        #    msg+=str(names[i]+': '+kds[i]+'\n')

        for i in range(len(kds)):
            kdDic[fnames[i]]=kds[i]
        #sorts by second item of dict, which is value, first is key
        #for k,v in sorted(kdDic.items(),key= lambda x: (float(x[1])),reverse = True):
        #    msg+=k+': '+v+'\n'

        sDict = sorted(kdDic.items(),key= lambda x: (float(x[1])),reverse = True)
        for k,v in sDict:
            msg+=k+': '+v+'\n'


        topKd = next(iter(sDict))
        msg+=str(topKd[0])+' is better than you all'
        await client.send_message(message.channel,msg)

    if message.content[0]=='!' and message.content.split()[0] not in commands:
        msg = 'Command not recognized, type !help to display commands'
        await client.send_message(message.channel,msg)


    if message.content.split()[0]==commands[4]:

        name = ''
        '''
        for i in range(len(message.content.split())):
            if i == 0:
                continue
            name+=message.content.split()[i]+" "
        '''
        #name should be extraced differently, above method is trash
        #the data given is a string so we could just slice from the command length to end of string
        name+=message.content[len(commands[4])+1:]
        #this way of handling names is cleaner to read and elmininates an uneccesary for loop

        URL = "https://api.fortnitetracker.com/v1/profile/xbox/"+name
        try:
            r = requests.get(url = URL,headers=key)
            data = r.json()


            overallKd = data['lifeTimeStats'][11]['value']
            overallWins = data['lifeTimeStats'][8]['value']
            overallMatchesPlayed = data['lifeTimeStats'][7]['value']
            overallWinrate = int(overallWins)/int(overallMatchesPlayed)*100
            overallWinrate=  str(int(overallWinrate))
        except:
            msg = 'Failed to gather any stats for '+name
            await client.send_message(message.channel,msg)
            return
            #overall data above, current below, quick and dirty but is close to accurate
        try:
            currKills = int(data['stats']['curr_p9']['kills']['value'])+int(data['stats']['curr_p10']['kills']['value'])+int(data['stats']['curr_p2']['kills']['value'])


            s1 = data['stats']['curr_p2']['matches']['value']
            s2 = data['stats']['curr_p9']['matches']['value']
            s3 = data['stats']['curr_p10']['matches']['value']
            currMatches = int(s1)+int(s2)+int(s3)

            currWins = str(int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])+int(data['stats']['curr_p10']['top1']['value']))

            currWinRate =int((int(currWins)/int(currMatches)) * 100)

            currKd = round(currKills/(currMatches-int(currWins)),2)
            #vars are overallWinrate,matches,overallWins,overallKd
            #print(str(currWinRate)+'%\n'+str(currMatches)+'\n'+str(currWins)+'\n'+str(currKd))
        except:
            msg = 'incomplete stats\n '+name
            msg+=' \n'
            msg+="kd: "+overallKd+'\n'+"wins: "+overallWins+'\n'+"matches: "+overallMatchesPlayed+'\n'+"winrate: "+overallWinrate+"%\n"



            try:

                matches3=int(data['stats']['curr_p2']['matches']['value'])+int(data['stats']['curr_p9']['matches']['value'])

                k3=int(data['stats']['curr_p2']['kills']['value'])+int(data['stats']['curr_p9']['kills']['value'])

                w3=int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])

                wr3 =int(round(((int(w3)/int(matches3)) * 100),0))

                kd3= round(k3/(matches3-int(w3)),2)

                msg+="kd: "+str(kd3)+'\n'+"wins: "+str(w3)+'\n'+"matches: "+str(matches3)+'\n'+"winrate: "+str(wr3)+"%\n--------------\n"
            except:

                m2=data['stats']['curr_p9']['matches']['value']

                k2=data['stats']['curr_p9']['kills']['value']

                w2=data['stats']['curr_p9']['top1']['value']

                wr2 =int(round(((int(w2)/int(m2)) * 100),0))

                kd2 = round(int(k2)/(int(m2)-int(w2)),2)

                msg+="kd: "+str(kd2)+'\n'+"wins: "+str(w2)+'\n'+"matches: "+str(m2)+'\n'+"winrate: "+str(wr2)+"%\n--------------\n"
            await client.send_message(message.channel,msg)
            return

        try:




            msg = name+'\n'


            cols = ['','','','','']
            cols[0] = 'Overall:'.center(0) + 'Current:'.rjust(33)
            cols[1] = str(('kd: '+overallKd).center(0)+('kd: '+str(currKd)).center(57))

            cols[2]= str(('wins: '+overallWins).center(0)+('wins: '+str(currWins)).center(54))
            cols[3]= str(('matches: '+overallMatchesPlayed).center(0)+('matches: '+str(currMatches)).center(39))
            cols[4]= str(('winrate: ' +overallWinrate+'%').center(0)+('winrate: '+str(currWinRate)+'%').center(45))
            for i in range(len(cols)):
                msg+='\n'+cols[i]

            #CURRENT FORMAT
            '''
            wsg = ''
            coals = ['','','','','']
            coals[0] ='Overall:','Current:'
            coals[1]='kd: '+str(overallKd) , 'kd: '+str(currKd)
            coals[2]='wins: '+str(overallWins),'wins: '+str(currWins)
            coals[3]='matches:'+str(overallMatchesPlayed),'matches:'+str(currMatches)
            coals[4]='winrate: '+str(overallWinrate)+'%','winrate: '+str(currWinRate)+'%'
            col_width = max(len(word) for row in coals for word in row)+2 # padding

            for row in coals:
                wsg+= ("".join(word.ljust(col_width) for word in row))+'\n'

            msg+=wsg
            '''

            '''
            RETIRED
            overList = [overallKd,overallWins,overallMatchesPlayed,overallWinrate+'%',]
            currList = ['\t'+str(currKd),'\t'+str(currWins),str(currMatches),str(currWinRate)+'%',]

            descList = ['kd:  ','wins:','matches:','winrate:']
            msg+='Overall:\t\t\t' + 'Current:'+'\n'
            for e,i,j in zip(descList,overList,currList):
                msg +=('{} {} \t\t\t{}'.format(e,i,j))+'\n'
            '''
            currKd = float(currKd)

            if (currKd) <= 1.0:
                msg+= '\nstatus: no skin'
            elif (currKd) >= 1.0 and currKd<=2.0:
                msg+= '\nstatus: Rust Lord'
            elif (currKd) >= 2.0 and currKd <=3.0:
                msg+= '\nstatus: Dark Knight'
            elif (currKd) >= 3.0:
                msg+='\nstatus: Streamer'
            else:
                msg+= '\nstatus: no idea ask Ryan'


        except:
            msg = 'Failed during msg creation'
        await client.send_message(message.channel,msg)
    if message.content.split()[0]==commands[5]:
        name = ''
        '''
        for i in range(len(message.content.split())):
            if i == 0:
                continue
            name+=message.content.split()[i]+" "
        '''
        #name should be extraced differently, above method is trash
        #the data given is a string so we could just slice from the command length to end of string
        name+=message.content[len(commands[5])+1:]
        #this way of handling names is cleaner to read and elmininates an uneccesary for loop

        URL = "https://api.fortnitetracker.com/v1/profile/psn/"+name
        try:
            r = requests.get(url = URL,headers=key)
            data = r.json()


            overallKd = data['lifeTimeStats'][11]['value']
            overallWins = data['lifeTimeStats'][8]['value']
            overallMatchesPlayed = data['lifeTimeStats'][7]['value']
            overallWinrate = int(overallWins)/int(overallMatchesPlayed)*100
            overallWinrate=  str(int(overallWinrate))
        except:
            msg = 'Failed to gather any stats for '+name
            await client.send_message(message.channel,msg)
            return
            #overall data above, current below, quick and dirty but is close to accurate
        try:
            currKills = int(data['stats']['curr_p9']['kills']['value'])+int(data['stats']['curr_p10']['kills']['value'])+int(data['stats']['curr_p2']['kills']['value'])


            s1 = data['stats']['curr_p2']['matches']['value']
            s2 = data['stats']['curr_p9']['matches']['value']
            s3 = data['stats']['curr_p10']['matches']['value']
            currMatches = int(s1)+int(s2)+int(s3)

            currWins = str(int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])+int(data['stats']['curr_p10']['top1']['value']))

            currWinRate =int((int(currWins)/int(currMatches)) * 100)

            currKd = round(currKills/(currMatches-int(currWins)),2)
            #vars are overallWinrate,matches,overallWins,overallKd
            #print(str(currWinRate)+'%\n'+str(currMatches)+'\n'+str(currWins)+'\n'+str(currKd))
        except:
            msg = 'incomplete stats\n '+name
            msg+='\n'
            msg+="kd: "+overallKd+'\n'+"wins: "+overallWins+'\n'+"matches: "+overallMatchesPlayed+'\n'+"winrate: "+overallWinrate+"%"

            try:

                matches3=int(data['stats']['curr_p2']['matches']['value'])+int(data['stats']['curr_p9']['matches']['value'])

                k3=int(data['stats']['curr_p2']['kills']['value'])+int(data['stats']['curr_p9']['kills']['value'])

                w3=int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])

                wr3 =int(round(((int(w3)/int(matches3)) * 100),0))

                kd3= round(k3/(matches3-int(w3)),2)

                msg+="kd: "+str(kd3)+'\n'+"wins: "+str(w3)+'\n'+"matches: "+str(matches3)+'\n'+"winrate: "+str(wr3)+"%\n--------------\n"
            except:

                m2=data['stats']['curr_p9']['matches']['value']

                k2=data['stats']['curr_p9']['kills']['value']

                w2=data['stats']['curr_p9']['top1']['value']

                wr2 =int(round(((int(w2)/int(m2)) * 100),0))

                kd2 = round(int(k2)/(int(m2)-int(w2)),2)

                msg+="kd: "+str(kd2)+'\n'+"wins: "+str(w2)+'\n'+"matches: "+str(m2)+'\n'+"winrate: "+str(wr2)+"%\n--------------\n"

            await client.send_message(message.channel,msg)
            return

        try:




            msg = name+'\n'


            cols = ['','','','','']
            cols[0] = 'Overall:'.center(0) + 'Current:'.rjust(33)
            cols[1] = str(('kd: '+overallKd).center(0)+('kd: '+str(currKd)).center(57))

            cols[2]= str(('wins: '+overallWins).center(0)+('wins: '+str(currWins)).center(54))
            cols[3]= str(('matches: '+overallMatchesPlayed).center(0)+('matches: '+str(currMatches)).center(39))
            cols[4]= str(('winrate: ' +overallWinrate+'%').center(0)+('winrate: '+str(currWinRate)+'%').center(45))
            for i in range(len(cols)):
                msg+='\n'+cols[i]

            #CURRENT FORMAT
            '''
            wsg = ''
            coals = ['','','','','']
            coals[0] ='Overall:','Current:'
            coals[1]='kd: '+str(overallKd) , 'kd: '+str(currKd)
            coals[2]='wins: '+str(overallWins),'wins: '+str(currWins)
            coals[3]='matches:'+str(overallMatchesPlayed),'matches:'+str(currMatches)
            coals[4]='winrate: '+str(overallWinrate)+'%','winrate: '+str(currWinRate)+'%'
            col_width = max(len(word) for row in coals for word in row)+2 # padding

            for row in coals:
                wsg+= ("".join(word.ljust(col_width) for word in row))+'\n'

            msg+=wsg
            '''

            '''
            RETIRED
            overList = [overallKd,overallWins,overallMatchesPlayed,overallWinrate+'%',]
            currList = ['\t'+str(currKd),'\t'+str(currWins),str(currMatches),str(currWinRate)+'%',]

            descList = ['kd:  ','wins:','matches:','winrate:']
            msg+='Overall:\t\t\t' + 'Current:'+'\n'
            for e,i,j in zip(descList,overList,currList):
                msg +=('{} {} \t\t\t{}'.format(e,i,j))+'\n'
            '''
            currKd = float(currKd)

            if (currKd) <= 1.0:
                msg+= '\nstatus: no skin'
            elif (currKd) >= 1.0 and currKd<=2.0:
                msg+= '\nstatus: Rust Lord'
            elif (currKd) >= 2.0 and currKd <=3.0:
                msg+= '\nstatus: Dark Knight'
            elif (currKd) >= 3.0:
                msg+='\nstatus: Streamer'
            else:
                msg+= '\nstatus: no idea ask Ryan'


        except:
            msg = 'Failed during msg creation'
        await client.send_message(message.channel,msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name,'\n',client.user.id)
    print('_________')

client.run(TOKEN)
