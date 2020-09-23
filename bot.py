# bot.py
import os
import card
from configparser import ConfigParser

#from discord import guild
from discord import channel
from discord import utils
from discord import Client
from discord import message
from dotenv import load_dotenv
from random import shuffle

# load in settings and parameters
#configurable parameters that can be changed later
config = ConfigParser()
config.read('settings.ini')
GUILD = config['Server']['server_name']
VOICE_CHANNEL = config['Server']['voice_channel_name']
TOKEN = config['Bot']['token']
client = Client()

# setting the guild as a global variable
curGuild = None


# Ran once at startup
@client.event
async def on_ready():

    #verify all names are actually names in the server and create a list of their members
    # and make the guild variable global for use in later function
    global curGuild
    curGuild = utils.find(lambda g: g.name == GUILD, client.guilds)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{curGuild.name}(id: {curGuild.id})\n'
    )

# used for sending a card to a user
async def send_card(member,card,roomNumber):
    message =   "------New Game!------" + \
                  "\nRole:    " + card['name'] + \
                  "\nColor:   " + card['color'] + \
                  "\nGoal:    " + card['goal'] + \
                  "\nStarting room: " + str(roomNumber)
    await member.create_dm()
    await member.dm_channel.send(message)

# Send out messages for a new game
async def new_game():

    # find the correct channel object
    voiceChannel = None
    for channel in curGuild.channels:
        if(VOICE_CHANNEL in str(channel.name)):
            voiceChannel = channel
            print(str(channel.name) + " selected\n")
            break
    
    memberList = voiceChannel.members


    # Call in cards
    president = card.president
    bomber = card.bomber
    gambler = card.gambler
    genericRed = card.genericRed
    genericBlue = card.genericBlue
    
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
    shuffle(cardList)
    shuffle(memberList)


    # send out cards to each member
    print("\nSending out the cards")
    print("There are " + str(len(cardList)) + " cards")
    print("There are " + str(len(memberList)) + " members")
    print()
    i = 0
    for member in memberList:
        roomNumber = str(i%2 + 1)

        # commented out unless testing
        # print(member.name + " gets the " + cardList[i]['name'] + ' card and starts in room ' + roomNumber)
 
        # send the card
        await send_card(member,cardList[i],roomNumber)

        #incriment i for next card
        i+=1

# Take in a message for a new game and start a new one
@client.event
async def on_message(message):
    # evaluate if a player wants to play start a new game
    if 'new game' in message.content:
        await new_game()
    # do nothing if they don't send "new game"
    else:
        pass

#----- Main -------------
client.run(TOKEN)