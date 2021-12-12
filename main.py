import os
import match
import nextcord
from dotenv.main import load_dotenv
from nextcord.ext import commands
from multiprocessing.connection import Listener
from nextcord.ext.commands import view

def main():
# Variable declarations
    # Bot variables
    load_dotenv()
    token = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="!")
    bot_mod_role = 'Codi Boi'

    # Logic Variables
    matches = {}
    match_players = {}
    queues = {}
    queue_max = 1
    current_id = 0 # TODO: after the database is implemented, there needs to be a way to set this to an id 1 higher than the highest in the DB.

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

# Queue Commands -----------------------------------------------
    # Queue join command
    @client.command(aliases=['Q', 'queue', 'Queue'])
    async def q(ctx):
        q_check = False

        if not ctx.channel in queues:
            queues.update({ctx.channel: []})

        for user in queues[ctx.channel]:
            if user == ctx.author:
                q_check = True

        if not q_check:
            queues[ctx.channel].append(ctx.author)
            await ctx.send(f'{ctx.author.mention} has been added to the queue.')

            # Queue pops, Generates a new match and @s members with their match id
            if len(queues[ctx.channel]) >= queue_max:
                nonlocal current_id
                players = queues.pop(ctx.channel)

                match_players.update({f'{current_id}': players})
                new_match = match.Match(f'{current_id}', players)
                matches.update({f'{current_id}': new_match})

                atMembers = f''
                for player in players:
                    atMembers += f'{player.mention} '
                atMembers += f'\nYour match is now ready!\nYour match id is: {current_id}.'
                await ctx.send(atMembers)
                
                current_id += 1
                
        else:
            await ctx.send(f'{ctx.author.mention} is already in this queue.')
    
    # Leave queue command
    @client.command(aliases=['L', 'leave', 'Leave'])
    async def l(ctx):
        q_check = False
        if ctx.channel in queues:
            for user in queues[ctx.channel]:
                if user == ctx.author:
                    q_check = True

            if q_check:
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

# Selection mode commands
    # Randomly selects teams
    @client.command(aliases=['R', 'random', 'Random'])
    async def r(ctx):
        await create_vote(ctx, 'random')
        
    @client.command(aliases=['C', 'captains', 'Captains'])
    async def c(ctx):
        await ctx.send('Coming Soon:tm:')

    @client.command(aliases=['B', 'balanced', 'Balanced'])
    async def b(ctx):
        await ctx.send('Coming Soon:tm:')

    @client.command(aliases=['O', 'ordered', 'Ordered'])
    async def o(ctx):
        await create_vote(ctx, 'ordered')

# Post queue pop commands
    # Lists the id of all the unreported matches
    @client.command()
    async def active(ctx):
        if len(matches) > 0:
            msg = 'Here are the id numbers of all of the current, unreported matches:\n'
            for match in matches:
                msg += f'{match}\n'
            await ctx.send(msg)
        else:
            await ctx.send('There are no unreported matches.')
    
    # Reports the match for scoring based on the given id and result and then stores the match in the database.
    @client.command()
    async def report(ctx, id, result):
        if id in matches:
            if ctx.author in match_players[id]:
                if matches[id].sorted:
                    # TODO: Store the result in a database
                    # NOTE: Make this happen inside of match.py so that the variables are easily accessible.

                    match_players.pop(f'{id}')
                    matches.pop(f'{id}')
                    await ctx.send(f'No database to store the match, but match {id} has been completed anyway.')
                else:
                    await ctx.send(f'Match {id} has not even started yet, get to voting.')
            else:
                await ctx.send(f'Bruh, match {id} is not even your match.')
        else:
            await ctx.send(f'Match {id} is not an active match to report on.')

# Misc. commands
    # Check the mmr of the player who ran the command followed by the top x of their rank?
    @client.command()
    async def leaderboard(ctx):
        await ctx.send('No database currently implemented')

# Admin Commands -----------------------------------------------
    # Clear active queue command
    @client.command()
    @commands.has_role(bot_mod_role)
    async def clear(ctx):
        if ctx.channel in queues:
            queues.pop(ctx.channel)
            await ctx.send(f'The {ctx.channel} queue has been cleared.')
        else:
            await ctx.send(f'This channel does not currently have an active queue.')

    # Cancel active match based on the given id
    @client.command()
    @commands.has_role(bot_mod_role)
    async def cancel(ctx, id):
        if id in matches:
            match_players.pop(f'{id}')
            matches.pop(f'{id}')
            await ctx.send(f'Match of match id: {id} has been cancelled.')
        else:
            await ctx.send(f'Match of match id {id} is not an active match.')

    @client.command()
    @commands.has_role(bot_mod_role)
    async def change(ctx, id, result):
        await ctx.send('place holder text')

    @client.command()
    @commands.has_role(bot_mod_role)
    async def delete(ctx, id):
        await ctx.send('place holder text')

# Support methods
    # Returns the match id for the given player
    def get_player_match_id(player):
        for match in match_players:
            if player in match_players[match]:
                return match
        return '?'

    # Sends the vote of given vote type to the match object of the player who typed the command
    async def create_vote(ctx, vote_type):
        found_id = get_player_match_id(ctx.author)

        if found_id == '?':
            await ctx.send(f'{ctx.author.name} has no matches to vote in.')
        else:
            match_in = matches[found_id]
            if match_in.add_vote(ctx.author, vote_type):
                await ctx.send(f"{ctx.author.name}'s vote has been updated.")
            else:
                await ctx.send(f'{ctx.author.name} has voted for: {vote_type} team selection.')

            if match_in.count_votes(queue_max):
                await ctx.send(f'Teams have been assigned for match of match id: {found_id}')

    client.run(token)
# _______________________________________________ End of main _______________________________________________

# Calls main (run with: "python3 main.py") __________________________________________________________________
if __name__ == '__main__':
    main()
