import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from Poker_hand import *
from dotenv import load_dotenv
import os


bot = commands.Bot(command_prefix='>', intents=discord.Intents.all())
load_dotenv()

@bot.event
async def on_ready():
    """Sends a message which says that bot is online and ready to play to the terminal 
    """
    print(f'{bot.user} is ready and online!')


@bot.command(name='hello')
async def hello(ctx):
    """Choice: play or not by pressing the button
    """
    play = Button(label='Play!', style=ButtonStyle.green)   #This button launches the game
    quit = Button(label='Maybe later...', style=ButtonStyle.grey)   #This button make the user quit the game
    
    #functions cooroutins to set the buttons functionality
    async def play_callback(interaction):
        global session
        global myhand 

        session = GameSession()
        session.prepare_game_session()
        
        myhand = MyHand()
        myhand.label = str(ctx.author).split("#")[0]
        session.players.append(myhand)
        session.wins = dict(zip(session.players, [0 for _ in range(len(session.players))]))

        names = [player.label for player in session.players]
        names_to_str = '\n'.join(names)
        await interaction.response.send_message('Nice! Now 4 players are online:\n{0}\nNow you have to make the initial pari. It is 25 coins'.format(names_to_str))

    async def quit_callback(interaction):
        await interaction.response.send_message(f'Ok, come back later!')

    play.callback = play_callback
    quit.callback = quit_callback

    #Adding these buttons to the massage
    myview = View(timeout=180)
    myview.add_item(play)
    myview.add_item(quit)

    #Sending the message
    await ctx.send(f'Hey, {ctx.author}! I am your *Pocker Bot*.\n On ths server you can play a clasic 5-cards pocker game!', view=myview)

@bot.command(name='initial_pari')
async def init_pari(ctx):
    """When the user enters this command, he or she makes all including him/her make initial pari 
    """
    session.make_init_pari()
    balances = [(player.label, player.total_balance) for player in session.players]
    await ctx.send(f'Ok, now the bank is {session.bank}')

@bot.command(name='balances')
async def get_balances(ctx):
    """Print the curent balances of each player
    """
    result = ''
    for player in session.players:
        line = f'{player.label} -- {player.total_balance}\n'
        result += line

    await ctx.send(result)

@bot.command(name='start')
async def main_game_control(ctx):
    """Launches the session
    """
    session.give_cards()
    session.find_combs()
    await ctx.send(f'{session.make_paris()}')
    msg = await bot.wait_for('message')
    session.bank += int(msg.content)
    myhand.total_balance -= int(msg.content)
    await ctx.send(session.show_combs())
    await ctx.send(session.determine_winners())
    await ctx.send(session.determine_losers_and_final_winner())

#________________________________________________________________

@bot.command(name='support')
async def support(ctx):
    """Sends the help message
    """
    support = Button(label='Support', style=ButtonStyle.red)
    tech_doc = Button(label='Documentation', style=ButtonStyle.green)

    async def support_response(interaction):
        with open(r'D:\miniprojet-Bot\new_bot\help.txt') as file:
            help_doc= file.read()
        await interaction.response.send_message(f'{help_doc}')

    async def techdoc_response(interaction):
        await interaction.response.send_message(file=discord.File(r'new_bot\Documentation.docx'))

    support.callback = support_response
    tech_doc.callback = techdoc_response

    myview = View(timeout=180)
    myview.add_item(support)
    myview.add_item(tech_doc)

    await ctx.send('Click here to send a support', view=myview)


bot.run(os.getenv('BOT_TOKEN'))     #A unique bot's token 
