import discord
import sys
import requests


#discord bot token here
TOKEN = 'XXXXXXXXXX'


#fortnite tracker api key here
key = {'TRN-Api-Key':"XXXXXXXXXXX"}


client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!help'):

        msg = '''Currently this bot is only for overall fortnite stats. To use type: !stats `gamertag` message @Ryan.H for info, he is my overlord.
        '''

        await client.send_message(message.channel,msg)
    if message.content.split()[0]=='!stats':

        name = ''
        for i in range(len(message.content.split())):
            if i == 0:
                continue
            name+=message.content.split()[i]+" "

        URL = "https://api.fortnitetracker.com/v1/profile/pc/"+name
        try:
            r = requests.get(url = URL,headers=key)
            data = r.json()
            overallKd = data['lifeTimeStats'][11]['value']
            overallWins = data['lifeTimeStats'][8]['value']
            overallMatchesPlayed = data['lifeTimeStats'][7]['value']
            overallWinrate = int(overallWins)/int(overallMatchesPlayed)*100
            overallWinrate=  str(int(overallWinrate))
            #overall data above, current below, quick and dirty but is close to accurate

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


            msg = name.center(37)
            fir,sec,thrd,frth,fith = '','','','',''
            cols = [fir,sec,thrd,frth,fith]
            cols[0] = 'Overall:'.center(0) + 'Current:'.rjust(33)
            cols[1] = ('kd: '+overallKd).center(0)+('kd: '+str(currKd)).rjust(35)
            cols[2]= ('wins: '+overallWins).center(0)+('wins: '+str(currWins)).rjust(32)
            cols[3]= ('matches: '+overallMatchesPlayed).center(0)+('matches: '+str(currMatches)).rjust(26)
            cols[4]= ('winrate: ' +overallWinrate+'%').center(0)+('winrate: '+str(currWinRate)+'%').rjust(29)
            for i in range(len(cols)):
                msg+='\n'+cols[i]


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
            msg = 'Failed to retrieve'
        await client.send_message(message.channel,msg)




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name,'\n',client.user.id)
    print('_________')

client.run(TOKEN)
