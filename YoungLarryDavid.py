import asyncio
import random
import time
import discord
import os
import string
import lyrics
from discord.ext.commands import Bot
from discord.ext import commands
from collections import defaultdict

BOT_PREFIX = ("+")

client = Bot(command_prefix=BOT_PREFIX)
#client.remove_command('help') will fix this later
markov = defaultdict(lambda: defaultdict(int))

def remove_punction(text):
    """
    Removes the punctuation from a given string
    """
    return text.translate(str.maketrans("", "", string.punctuation))

def get_trigrams(data):
    """
    Generates the trigrams of an array of elements. For example, if `data = [a, b, c, d]` then the
    output will be `[[a,b,c], [b,c,d]]`.
    """
    for i in range(len(data) - 2):
        yield data[i:i + 3]

def get_ngrams(degree, data):
    """
    Generates the n-grams of an array of elements. For example, if `data = [a, b, c, d]` and
    `degree = 2` then the output will be `[[a,b], [b,c], [c,d]]`. This is just a generic
    version of the `get_trigrams` function, here for reference.
    """
    for i in range(len(data) - degree + 1):
        yield data[i:i + degree]

def weighted_choice(states):
    """
    Given a dictionary of keys and weights, choose a random key based on its weight.
    """
    n = random.uniform(0, sum(states.values()))
    for key, val in states.items():
        if n < val:
            return key
        n -= val

    # Something went wrong, don't make a choice.
    return None

def init_markov():
    # just join the array into a single string
    data = ' '.join([
        *lyrics.kanye_lyrics,
        *lyrics.gucci_lyrics,
        *lyrics.random_lyrics,
        *lyrics.nas_lyrics,
        *lyrics.E40_lyrics,
        *lyrics.snoop_dogg_lyrics,
        *lyrics.three_six_lyrics,
        *lyrics.project_pat_lyrics,
        *lyrics.wu_tang_lyrics,
        *lyrics.biggie_lyrics,
        *lyrics.doc_oct_lyrics,
        *lyrics.eminem_lyrics,
        *lyrics.freddie_gibbs_lyrics,
        *lyrics.big_L_lyrics,
        *lyrics.outkast_lyrics
    ])

    print('data: ' + data)
    data = remove_punction(data).replace('\n', ' ')
    parsed_data = data.split(' ')

    # Now split the input data into trigrams for parsing.
    for (w1, w2, w3) in get_trigrams(parsed_data):
        # Use lowercase to normalize the data.
        w1 = w1.lower()
        w2 = w2.lower()
        w3 = w3.lower()

        # Update the tally for this combination.
        markov[(w1, w2)][w3] += 1
    print('ok its initialized')

def spit_game():
     # Use random to pick a random initial state (or set it yourself).
    start_state = random.choice(list(markov.keys()))
    # You can preview it by writing ```print("Initial State: %s" % repr(start_state))```

    # Now start 'walking' along the Markov Chain to generate stuff. Unfortunately, the hard part
    # is knowing when to stop. Here I say I want sentences no longer than 15 words, and if there's
    # a dead-end, stop immediately. Naturally, there's much better ways to do this.
    s1, s2 = start_state
    max_length = 15
    result = [s1, s2]
    for _ in range(max_length):
        next_state = weighted_choice(markov[(s1, s2)])
        if next_state is None:
            break
        result.append(next_state)
        s1 = s2
        s2 = next_state

    # the result is an array so just make it a string
    return ' '.join(result) + '.'

@client.event
async def on_ready():
    print("It's Gucci Time!")
    init_markov()
    await client.change_presence(game=discord.Game(name='+help for command list!'))

# Sends a message to a new member that joins the discord server.
@client.event
async def on_member_join(member):
    await client.send_message(member, "Sup!? It's ya boy Young LD, and my sole purpose in this world is to provide you and your crew with some dank, absurd, hard hittin' rap lyrics.\n" 
    "For a list of all available commands, use the +help command.\n"
    "ps - Wu-Tang is 4 da children and don't forget to Protect Ya Kneck.")
"""  
@client.event
async def on_message(message):
    # Don't need the bot to reply to itself.
    if message.author == client.user:
        return

    # Randomly picks a lyric from the list of kanye_lyrics
    if message.content.upper().startswith('+KANYE'):
        await client.send_message(message.channel, random.choice(lyrics.kanye_lyrics))

    # Randomly picks a lyric from the list of gucci_lyrics
    if message.content.upper().startswith('+GUCCI'):
        await client.send_message(message.channel, random.choice(lyrics.gucci_lyrics))

    # Randomly picks a lyrics from the list of random_lyrics
    if message.content.upper().startswith('+RANDOM'):
        await client.send_message(message.channel, random.choice(lyrics.random_lyrics))

    # Randomly picks lyrics from the list of nas_lyrics
    # primarily lyrics from illmatic aka the best hip hop album of all time
    if message.content.upper().startswith('+NAS'):
        await client.send_message(message.channel, random.choice(lyrics.nas_lyrics))

    # Randomly picks lyrics from the list of E40_lyrics
    if message.content.upper().startswith('+E40'):
        await client.send_message(message.channel, random.choice(lyrics.E40_lyrics))

    # Randomly picks lyrics from the list of snoop_dogg_lyrics
    if message.content.upper().startswith('+SNOOP'):
        await client.send_message(message.channel, random.choice(lyrics.snoop_dogg_lyrics))

    # Randomly picks lyrics from the list of three_six_lyrics
    if message.content.upper().startswith('+TRIPLE6'):
        await client.send_message(message.channel, random.choice(lyrics.three_six_lyrics))

    # Randomly picks lyrics from the list of project_pat_lyrics
    if message.content.upper().startswith('+PAT'):
        await client.send_message(message.channel, random.choice(lyrics.project_pat_lyrics))

    # Randomly picks lyrics from the list of wu_tang_lyrics
    if message.content.upper().startswith('+WUTANG'):
        await client.send_message(message.channel, random.choice(lyrics.wu_tang_lyrics))

    # Randomly picks lyrics from the list of biggie_lyrics
    if message.content.upper().startswith('+BIGGIE'):
        await client.send_message(message.channel, random.choice(lyrics.biggie_lyrics))

    # Rancomly picks lyrics from the list of doc_oct_lyrics
    if message.content.upper().startswith('+DROCTAGON'):
        await client.send_message(message.channel, random.choice(lyrics.doc_oct_lyrics))

    # Randomly picks lyrics from the list of eminem_lyrics
    if message.content.upper().startswith('+EMINEM'):
        await client.send_message(message.channel, random.choice(lyrics.eminem_lyrics))

    # Randomly picks lyrics from the list of gangsta gibbs lyrics
    if message.content.upper().startswith('+GIBBS'):
        await client.send_message(message.channel, random.choice(lyrics.freddie_gibbs_lyrics))

    # Randomly picks lyrics from the list of Big L lyrics
    if message.content.upper().startswith('+BIGL'):
        await client.send_message(message.channel, random.choice(lyrics.big_L_lyrics))

    # Randomly picks lyrics from the list of Outkast lyrics
    if message.content.upper().startswith('+OUTKAST'):
        await client.send_message(message.channel, random.choice(lyrics.outkast_lyrics))

    # Displays the bots personal opinion on who are the top 10 best hip-hop artist of all time
    if message.content.upper().startswith('+TOP10'):
        await client.send_message(message.channel, "This is my top ten list of the best hip-hop artist of all time.\n"
                                  "1. Nas\n"
                                  "2. Ghostface Killah\n"
                                  "3. Andre 3000\n"
                                  "4. The Notorious B.I.G.\n"
                                  "5. Big L\n"
                                  "6. Raekwon da Chef\n"
                                  "7. Tupac\n"
                                  "8. Kendrick Lamar\n"
                                  "9. Eminem\n"
                                  "10. Jay-Z")

    # Displays the bots personal opinion on who are the top 10 best hip-hop producers of all time
    if message.content.upper().startswith('+PRODUCERS'):
        await client.send_message(message.channel, "This is my top ten list of best hip-hop producers of all time.\n"
                                  "1. J Dilla\n"
                                  "2. Madlib\n"
                                  "3. RZA\n"
                                  "4. Dr. Dre\n"
                                  "5. Organized Noize\n"
                                  "6. No I.D.\n"
                                  "7. Pete Rock\n"
                                  "8. Sounwave\n"
                                  "9. Q-Tip\n"
                                  "10. Kanye West")
    
    # Uses markov chain to generate random lyrics
    if message.content.upper().startswith('+SPIT'):
        await client.send_message(message.channel, spit_game())
    
    # Displays commands for the user
    if message.content.upper().startswith('+HELP'):
        commands={}
        commands['+help']='Young LD Displays the list of command that can be used.'
        commands['+kanye']='Displays random lyrics from the greatest artist of our generation.'
        commands['+gucci']='Displays lyrics by Guwop AKA El Gato the Human Glacier.'
        commands['+nas']='Displays random lyrics from the greatest album of all time, Illmatic.'
        commands['+e40']='Displays random lyrics by E40 AKA Charlie Hustle.'
        commands['+snoop']='Displays random lyrics by the Dogg Father.'
        commands['+triple6']='Displays random lyrics by Three 6 Mafia.'
        commands['+pat']='Displays random lyrics by Project Pat.'
        commands['+wutang']='Wu-Tang is for the the children.'
        commands['+biggie']='Displays random lyrics by the black Frank White.'
        commands['+droctagon']='Displays random lyrics by Dr.Octagon AKA the Dr.Octagonecologyst.'
        commands['+eminem']='Displays random lyrics by Eminem.'
        commands['+gibbs']='Displays random lyrics by Gangsta Gibbs.'
        commands['+bigl']='Displays random lyrics by Big L.'
        commands['+outkast']='Displays random lyrics by Outkast.'
        commands['+top10']='Young LD displays his top 10 list of the best Hip-Hop artist of all time.'
        commands['+producers']='Young LD displays his top 10 list of the best Hip-Hop producers of all time.'
        commands['+random']='Displays random lyrics from a bunch of different artist.'
        commands['+spit']='Uses a Markov chain to combine lyrics and comes up with some funky shit.'

        msg=discord.Embed(title='Young Larry David', description='Written by SnoopFrogg', color=0x0000ff)
        for command, description in commands.items():
            msg.add_field(name=command, value=description, inline=False)
        #msg.add_field(name='Join our Discord/For Questions/Chilling', value='', inline=False)
        await client.send_message(message.channel, embed=msg)
"""
@client.command(pass_context=True)
async def kanye(ctx):

    await client.say(lyrics.kanye_lyrics)

async def list_server():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

client.loop.create_task(list_server())
client.run(os.getenv('TOKEN'))
