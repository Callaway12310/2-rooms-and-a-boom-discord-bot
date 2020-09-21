# bot.py
import os

import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


async def send_card(member,card):
    message =   "\n\n------New Game!------" + \
                  "\nRole:    " + card['name'] + \
                  "\nColor:   " + card['color'] + \
                  "\nGoal:    " + card['goal']
    await member.create_dm()
    await member.dm_channel.send(message)


# Ran once at startup
@client.event
async def on_ready():

    #get names from file
    nameFile = open('names.txt')
    names = nameFile.readlines()
    nameFile.close()

    #verify all names are actually names in the server and create a list of their members
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    memberList = []

    for member in guild.members:
        for name in names:
            name = name.strip('\n')
            if str(name) in str(member.name):
                print(name + " is in the server")
                memberList.append(member)

    print()
    # Send out cards based on the number of people in the member list

    #generate card list
    president   = {'name':'President','color':'Blue','goal':'Avoid the bomber'}
    bomber      = {'name':'Bomber','color':'red','goal':'Be with the president'}
    genericBlue = {'name':'Blue team','color':'Blue','goal':'Keep the president away from the bomber'}
    genericRed  = {'name':'Red team','color':'Red','goal':'Get the bomber to be with the president'}
    gambler     = {'name':'Gambler','color':'Grey','goal':'Guess if red blue or neither team won'}

    cardList = [president,bomber]

    # check for gambler if odd number
    if(len(memberList)%2 > 0):
        cardList.append(gambler)
    
    # add all other players, alternating odd and even
    for i in range(len(cardList),len(memberList)):
        if(i%2 > 0):
            cardList.append(genericBlue)
        else:
            cardList.append(genericRed)
    
    # shuffle the cards and member list for room sorting
    random.shuffle(cardList)
    random.shuffle(memberList)


    # send out cards to each member
    print("Sending out the cards")
    print("There are " + str(len(cardList)) + " cards")
    print("There are " + str(len(memberList)) + " members")
    print()
    i = 0
    for member in memberList:
        print(member.name + " gets the " + cardList[i]['name'] + ' card and starts in room ' + str(i%2 + 1))
 
        # send the card
        await send_card(member,cardList[i])
        # message =   " Role: " + cardList[i]['name'] + \
        #     "\nColor: " + cardList[i]['color'] + \
        #     "\nGoal: " + cardList[i]['goal'] + \
        #     "\nStarting Room: "    + str(i%2 + 1)
        # await member.create_dm()
        # await member.dm_channel.send(message)

        #incriment i for next card
        i+=1




#----- Main -------------
client.run(TOKEN)