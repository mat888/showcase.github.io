import socket
import random
import time
import asyncio

import discord
from discord.ext import commands

TOKEN = 'TOKEN'
GUILD = 'guild'
GUILD = 'guild'

#Olympia Guild channel ids
general_chat_id = 368577449929211925 #general text chat id
salty_bet_chat_id = 712168999126827028 # salty bet text chat id

#Matteo's Study
off_topic_chat_id = 701083383840637036 

server = 'irc.chat.twitch.tv'
port = 'port'
nickname = 'salty_bet_bot'
token = 'token'
channel = '#saltybet'

channel_g = off_topic_chat_id

emotes = { #type emote in format " '<:sethboi:578495534226997248>' " in chat.
} #removed for privacy

first_loop_global = True  #keeps function from executing match results logic if
                          #first message recieved is of results (no fight info yet)

#fight = fight_tracker('') #initialize first fight object -- defined below class definition
salty_bet_chat_id = 712168999126827028 # salty bet text chat id

class fight_tracker:

    def __init__(self):

        self.fighter_1 = None
        self.fighter_2 = None
        self.fighter_1_emote_key = None
        self.fighter_2_emote_key = None
        self.fighter_1_emote_str = None
        self.fighter_2_emote_str = None
        self.announcement = None
        self.tally = {}
        self.message_id = None

    def set_variables(self, message):

        self.fighter_1 = message[0]
        self.fighter_2 = message[1]

        #randomly set each reaction emote (via dict keys of 'emotes')
        vote_icon_keys = list(emotes.keys())
        self.fighter_1_emote_key = random.choice(vote_icon_keys)
        vote_icon_keys.remove(self.fighter_1_emote_key)
        self.fighter_2_emote_key = random.choice(vote_icon_keys)

        def emote_key_to_str(key):
            string = '<:' + key + ':' + str(emotes[key]) + '>'
            print('string', string)
            return string

        self.fighter_1_emote_str = emote_key_to_str(self.fighter_1_emote_key)
        self.fighter_2_emote_str = emote_key_to_str(self.fighter_2_emote_key)

        self.announcement = 'Bets are open for' + self.fighter_1 + ' ' \
         + self.fighter_1_emote_str + ' vs ' + self.fighter_2 + ' ' \
         + self.fighter_2_emote_str

# test = ':waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :Bets are OPEN for Superior spider-man vs Soulgen! (A Tier) (matchmaking) www.saltybet.com'
def get_fighters(message):
    start = message.find('Bets are OPEN for') #17 long
    message = message[start + 18:]
    words = message.split(' ') #word list with fighter information

    fighter_1 = ''
    i = 0                       #loop through words in fighter announcement

    while (words[i] != 'vs'):   #until 'vs' occours; delimits first fighter name
        fighter_1 += ' ' + words[i]
        i += 1

    fighter_2 = ''
    i += 1                       #skip past word 'vs' in announcement
    while (words[i][-1] != '!'): #last word in second fighter ends in '!'
        fighter_2 += ' ' + words[i]
        i += 1
    fighter_2 += words[i][:-1]

    return (fighter_1, fighter_2)

def get_winner(message):
    end = message.find('wins!')
    return message[:end]

def filter_fighter_announce(message): #only returns fight announcements from chat stream
    word_list = message.split(' ')    #will return both fighter intros and results

    if (message[0:75] == ':waifu4u!waifu4u@waifu4u.tmi.twitch.tv PRIVMSG #saltybet :Bets are OPEN for'):

        return message[58:]

    elif(len(word_list) > 4):
        if(('wins!' in word_list) and word_list[0] == ':waifu4u!waifu4u@waifu4u.tmi.twitch.tv'):

            return message[58:]

    return ''

async def chat_parser():
    resp = sock.recv(4096).decode('utf-8')
    # print('chat response: ' , resp)
    filtered_response = filter_fighter_announce(resp)

    if resp.startswith('PING'):
        # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
        print("Ponging iirc server")
        sock.send("PONG\n".encode('utf-8'))
        return ''

    elif (len(filtered_response) > 0):
        if (filtered_response.count('ets are OPEN for') > 0):
            filtered_response = get_fighters(filtered_response)
            return (filtered_response, 'pre-fight')

        elif (filtered_response.count('wins! Payouts to') > 0):
            filtered_response = get_winner(filtered_response)
            return (filtered_response, 'post-fight')
    return ''

# first_loop_global = True --see top of file for this uncommented
fight = fight_tracker()  ##initialize first fight object

async def message_loop():
    await client.wait_until_ready()

    global first_loop_global
    global channel_g
    channel = client.get_channel(channel_g)

    while True:

        chat_reception = await chat_parser()
        # print('chat_reception', chat_reception)
        # print('sleeping in message_loop()')
        await asyncio.sleep(.3)
        if (chat_reception == ''):
            continue
    
        if (chat_reception[1] == 'pre-fight'):
    
            print('setting variables')
            first_loop_global = False

            print(chat_reception)
            fight.set_variables(chat_reception[0])

            print('self.fighter_1', fight.fighter_1)
            print('self.fighter_2', fight.fighter_2)
            print('self.fight.announcement', fight.announcement)

            msg = await channel.send(fight.announcement)

            # print(dir(msg))

            fight.message_id = msg.id #used later to check
            #that reactions are to the correct message in Discord

            await msg.add_reaction(fight.fighter_1_emote_str)
            await msg.add_reaction(fight.fighter_2_emote_str)
            # print('\n ----- \n msg: \n' , msg, '\n ----- \n')
            print('past await in send fight.announcement')
    
        elif(not first_loop_global):
            print('first_loop_global: ', first_loop_global)
            print('winner announce')
            winner = get_winner(chat_reception[0])
            winner_text_output = ''
    
            if (winner == fight.fighter_1[0]):
                # fighter_1_emote_key -- use this to check tally for winners
                winner_text_output = fight.fighter_1[1] * 3 + fight.fighter_1[0] + " wins! " + fight.fighter_1[1] * 3
            else:
                winner_text_output = fight.fighter_2[1] * 3 + fight.fighter_2[0] + " wins! " + fight.fighter_2[1] * 3

            print('winner_text_output:', winner_text_output)
            await channel.send(winner_text_output)
            print('past await in send winner_text_output')
            # return winner_text_output

        print('passing')
        pass

def sock_connect():
    while(True):
        try:
            global sock
            sock = socket.socket()
            sock.connect((server, port)) #global variables
            sock.send(f"PASS {token}\r\n".encode('utf-8'))
            sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
            sock.send(f"JOIN {channel}\r\n".encode('utf-8'))
            return 0
        except:
            time.sleep(5)
            sock_connect()

# TOKEN = 'NzA2Njc0MTYyNDQ1NTgyNDE2.XrBbNg.uQRqBE_5Q0g6EVxQxiyiEgfDPGA'
# GUILD = 'Olympia International Cooperative Gaming Initiative'

client = discord.Client()

# salty_bet_chat_id = 712168999126827028 # salty bet text chat id
# again, defined for real at top of file.

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = client.get_channel(channel_g)
    
    # await channel.send('pretty neat')

    while (bool(client.is_closed)):
        counter += 1
        # print(counter)
        # await channel.send(counter)
        # p = await message_loop()
        await asyncio.sleep(5) # task runs every x seconds

@client.event
async def on_ready():
    print('Finding channel...')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    # u = [user.name for user in client.users]
    # print(u)
    print(guild.channels)
    print('Logged in as', client.user)

    print(client.emojis)

counter_g = 0


@client.event
async def on_message(message):
    global counter_g
    counter_g += 1
    print(counter_g)
    print(message)


@client.event
async def on_raw_reaction_add(payload):

    print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')

    if (fight.message_id == payload.message_id):
        print(payload)
        print('react to fight announce')
        print('user_id: ', payload.user_id)
        print('user: ', client.get_user(payload.user_id))
        reaction_id = payload.emoji.id
        print('reaction_id', reaction_id)

        user_id = client.get_user(payload.user_id)

        if ( reaction_id == emotes[fight.fighter_1_emote_key] or \
             reaction_id == emotes[fight.fighter_2_emote_key] ):

            if (user_id not in fight.tally):

                fight.tally[user_id] = reaction_id
                print(' -------------- \n', fight.tally, '\n -----------------')
    # print(payload.user_id)
'''
    print(payload.emoji.id)

    vote = payload.emoji.id
    voter = client.get_user(payload.user_id)
    print(voter)
    print(vote)
'''

sock_connect()
# client.loop.create_task(my_background_task())
client.loop.create_task(message_loop())
client.run(TOKEN)

'''

@client.event
async def on_ready():
    global channel
    print('Finding channel...')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    channel = guild.get_channel(salty_bet_chat_id)
    print('Connected to Channel.')

# @client.event
async def go():
    global channel
    await client.wait_until_ready()

    try:
        print('Beginning main loop.')
        while True:
            message_out = await message_loop()
            if (message_out != None and message_out != None):

                print('Sending to Discord: ', message_out)
                # await client.send_message(channel, message_out)
                await channel.send(message_out)
                print('message sent...')
            
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        sock.close()
        exit()

@client.event
async def on_message(message):
    print(message)

sock_connect()

client.loop.create_task(go())
client.run(TOKEN)

# start()

# def go():
#     client.run(TOKEN)

# go()
'''
