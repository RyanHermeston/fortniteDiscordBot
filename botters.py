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
            kd = data['lifeTimeStats'][11]['value']
            wins = data['lifeTimeStats'][8]['value']
            matchesPlayed = data['lifeTimeStats'][7]['value']
            winrate = int(wins)/int(matchesPlayed)
            winrate=  str(int(winrate))
            #overall data above, current below, quick and dirty but is close to accurate

            s4kills = int(data['stats']['curr_p9']['kills']['value'])+int(data['stats']['curr_p10']['kills']['value'])+int(data['stats']['curr_p2']['kills']['value'])


            s1 = data['stats']['curr_p2']['matches']['value']
            s2 = data['stats']['curr_p9']['matches']['value']
            s3 = data['stats']['curr_p10']['matches']['value']
            s4matches = int(s1)+int(s2)+int(s3)

            s4wins = str(int(data['stats']['curr_p2']['top1']['value'])+int(data['stats']['curr_p9']['top1']['value'])+int(data['stats']['curr_p10']['top1']['value']))

            s4winRate =int((int(s4wins)/int(s4matches)) * 100)

            s4kd = round(s4kills/(s4matches-int(s4wins)),2)
            #vars are winrate,matches,wins,kd
            #print(str(s4winRate)+'%\n'+str(s4matches)+'\n'+str(s4wins)+'\n'+str(s4kd))



            msg = name+"\nOverall:\t\t\t\t Current:\nkd: "+kd+"\t\t\t\t kd: "+str(s4kd)+"\nwins: "+wins+"\t\t\t\t wins:"+str(s4wins)+"\nmatches: "+matchesPlayed+'\t\tmatches: '+ str(s4matches)+'\nwinrate: '+winrate+'%\t\t winrate: ' +str(s4winRate)+'%'

            if (kd) < '1':
                msg+= '\nstatus: no skin'
            elif (kd) > '1' and kd<'2':
                msg+= '\nstatus: regular shmuck'
            elif (kd) > '2' and kd <'3':
                msg+= '\nstatus: dark knight'
            elif (kd) > '3':
                msg+='\nstatus: streamer'
            else:
                msg+= '\nstatus: no idea'


        except:
            msg = 'Failed, make sure name is spelled right'
        await client.send_message(message.channel,msg)




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name,'\n',client.user.id)
    print('_________')

client.run(TOKEN)
