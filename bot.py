# bot.py
import os
import card

#from discord import guild
from discord import channel
from discord import utils
from discord import Client
from discord import message
from dotenv import load_dotenv
from random import shuffle

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
VOICE_CHANNEL = os.getenv('VOICE_CHANNEL')
client = Client()

# setting the guild as a global variable
curGuild = None

# used for sending a card to a user
async def send_card(member,card):
    message =   "------New Game!------" + \
                  "\nRole:    " + card['name'] + \
                  "\nColor:   " + card['color'] + \
                  "\nGoal:    " + card['goal']
    await member.create_dm()
    await member.dm_channel.send(message)


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