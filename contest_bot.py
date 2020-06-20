import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.utils import get
from pathlib import Path
import random
import asyncio
import time
from db_conn import UsersDb as db
# dopisanie funkcji z asyncio do sprawdzania userow

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ID = int(os.getenv('GUILD_ID'))


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    global guild
    guild = bot.get_guild(ID)

    print(
        f'{bot.user.name} {guild} has connected to discord!'
    )


@bot.command(pass_context=True, name='show')
async def join(ctx):
    user = str(ctx.author)
    await ctx.send(user)


@bot.command(pass_context=True, name='add')
async def add_member(ctx):
    for member in guild.members:
        if not member.bot:
            db(member.id, member.name).new_user()


@bot.group()
async def contest(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid contest command passed...')


global contest_start
contest_start = False


@contest.command(pass_context=True, name='start')
async def start(ctx, name: str, *options):
    global contest_start
    if contest_start:
        await ctx.send("Contest is currently running!")
    else:
        global embed
        embed = discord.Embed(title=name, color=0xff0000, inline=False)
        for option in options:
            embed.add_field(name=option, value=0, inline=False)

        global user_vote
        user_vote = []
        await ctx.send(content=f'Contest {name} has been started!', embed=embed)
        contest_start = True


@contest.command(pass_context=True, name='add')
async def add(ctx, option: str):
    embed.add_field(name=option, value=0, inline=False)
    await ctx.send('New option has been added to contest!')


@contest.command(pass_context=True, name='vote')
async def vote(ctx, name: str):
    try:
        dicted = embed.to_dict()
    except NameError:
        await ctx.send('Contest is over!')
    else:
        if ctx.author in user_vote:
            await ctx.send('You already voted!')
        else:
            user_vote.append(ctx.author)
            index = 0
            if not 'fields' in dicted.keys():
                await ctx.send('This contest doesn\'t have any option!')
            else:

                for n in dicted['fields']:
                    if n['name'] == name:
                        value = int(n['value'])
                        value += 1
                        embed.set_field_at(
                            index=index, name=name, value=value)
                    index += 1

                await ctx.send(embed=embed)


@contest.command(pass_context=True, name='stop')
async def stop(ctx):
    global contest_start
    if contest_start:
        await ctx.send(content='Contest has been ended', embed=embed)
        del globals()['embed']
        del globals()['user_vote']
        contest_start = False
    else:
        await ctx.send('Contest is already over!')


async def on_join(member):
    if not member.bot:
        user = db(member.id, member.name)
        if user.check_user():
            user.new_user()
            print('New user has been added!')
        else:
            print('User already exist!')
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name} familiy!'
    )


bot.add_listener(on_join, 'on_member_join')
bot.run(TOKEN)
