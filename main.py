import os
import random
import nextcord
from dotenv.main import load_dotenv
from nextcord.ext import commands
from multiprocessing.connection import Listener
from nextcord.ext.commands import view

def main():
    load_dotenv()
    token = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="!")
    BotModRole = 'Codi Boi'

    matches = {} # change to a class that contains a full member list, teams 1 and 2, sorted boolean, and the match id
    queues = {}
    queueMax = 8
    currentId = 0

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord!")

    @client.event
    async def on_message(message):
        # mess = message.content
        # if message.author == client.user:
        #     return
        # if mess.startswith('$hello'):
        #     await message.channel.send('Hello!')
        # elif mess.startswith('?bigmantime'):
        #     if (random.randint(0, 1) == 0):
        #         await message.channel.send('https://www.youtube.com/watch?v=2XDfp4_eZf4')
        #     else:
        #         await message.channel.send('https://www.youtube.com/watch?v=N06fZxoUQx0')
        await client.process_commands(message)

# User Commands -----------------------------------------------
    # Queue join command
    @client.command(aliases=['Q', 'queue', 'Queue'])
    async def q(ctx):
        qcheck = False

        if not ctx.channel in queues:
            queues.update({ctx.channel: []})

        for user in queues[ctx.channel]:
            if user == ctx.author:
                qcheck = True

        if not qcheck:
            queues[ctx.channel].append(ctx.author)
            await ctx.send(f'{ctx.author.mention} has been added to the queue.')

            if len(queues[ctx.channel]) >= queueMax:
                userList = queues.pop(ctx.channel)
                
                nonlocal currentId
                matches.update({f'{currentId}': userList})

                atMembers = f''
                for user in matches[f'{currentId}']:
                    atMembers += f'{user.mention} '
                atMembers += f'\nYour match is now ready!\nYour match id is: {currentId}.'
                await ctx.send(atMembers)
                
                currentId += 1
                
        else:
            await ctx.send(f'{ctx.author.mention} is already in this queue.')
    
    # Leave queue command
    @client.command(aliases=['L', 'leave', 'Leave'])
    async def l(ctx):
        qCheck = False
        if ctx.channel in queues:
            for user in queues[ctx.channel]:
                if user == ctx.author:
                    qcheck = True

            if qcheck:
                queues[ctx.channel].remove(ctx.author)
                await ctx.send(f'{ctx.author.name} has been removed from the queue.')
            else:
                await ctx.send(f'{ctx.author.name} is not currently in this queue.')
        else:
            await ctx.send('This channel does not currently have an active queue.')

    # Status of active queue command
    @client.command(aliases=['S', 'status', 'Status'])
    async def s(ctx):
        if ctx.channel in queues:
            current_q = 'Members in the active queue: '
            for user in queues[ctx.channel]:
                current_q += f'{user.name}'
            await ctx.send(current_q)
        else:
            await ctx.send('This channel does not currently have an active queue.')

    @client.command(aliases=['R', 'random', 'Random'])
    async def r(ctx):
        await ctx.send('place holder text')

    @client.command(aliases=['C', 'captains', 'Captains'])
    async def c(ctx):
        await ctx.send('place holder text')

    @client.command()
    async def b(ctx):
        await ctx.send('place holder text')

    @client.command()
    async def active(ctx):
        await ctx.send('place holder text')
    
    @client.command()
    async def report(ctx, id, result):
        await ctx.send('place holder text')

    @client.command()
    async def leaderboard(ctx):
        await ctx.send('place holder text')

# Admin Commands -----------------------------------------------
    # Clear active queue command
    @client.command()
    @commands.has_role(BotModRole)
    async def clear(ctx):
        if ctx.channel in queues:
            queues.pop(ctx.channel)
            await ctx.send(f'The {ctx.channel} queue has been cleared.')
        else:
            await ctx.send(f'This channel does not currently have an active queue.')

    @client.command()
    @commands.has_role(BotModRole)
    async def cancel(ctx):
        await ctx.send('place holder text')

    @client.command()
    @commands.has_role(BotModRole)
    async def change(ctx):
        await ctx.send('place holder text')

    @client.command()
    @commands.has_role(BotModRole)
    async def delete(ctx):
        await ctx.send('place holder text')

    client.run(token)
# _______________________________________________ End of main _______________________________________________

# Calls main (run with: "python3 main.py") __________________________________________________________________
if __name__ == '__main__':
    main()
