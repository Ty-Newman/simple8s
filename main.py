import os
import match
import discord
import nextcord
from dotenv.main import load_dotenv
from nextcord.ext import commands
from datetime import datetime
from multiprocessing.connection import Listener
from nextcord.ext.commands import view

def main():
# Variable declarations
    # Bot variables
    load_dotenv()
    token = os.getenv("TOKEN")
    client = commands.Bot(command_prefix="!")
    bot_mod_role = '8s Bot Mod'

    # Logic Variables
    current_id = 0
    queue_max = 1
    queues = {}
    matches = {}
    match_players = {}

    @client.event
    async def on_ready():
        # TODO: after the database is implemented, there needs to be a way to set this to an id 1 higher than the highest in the DB.
        # NOTE: Get the latest current ID from the database.
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

# THE TEST ZONE
    @client.command(aliases=['T', 'test', 'Test'])
    async def t(ctx):
        print('call\n')
        for member in ctx.guild.fetch_members(limit=None):
            print(f'searching...\n {member}')
            if member.name == 'Anelius':
                await member.send('Poggers')
        print('finished\n\n\n\n')
                
# Queue Commands -----------------------------------------------
    # Queue join command
    @client.command(aliases=['Q', 'queue', 'Queue'])
    async def q(ctx):
        if not ctx.channel in queues:
            queues.update({ctx.channel: []})

        if not is_in_queue(ctx):
            queues[ctx.channel].append(ctx.author)
            await ctx.send(f'{ctx.author.mention} has been added to the queue.')

            # Queue pops, Generates a new match and @s members with their match id
            if len(queues[ctx.channel]) >= queue_max:
                nonlocal current_id
                this_id = f'{current_id}'
                players = queues.pop(ctx.channel)

                match_players.update({this_id: players})
                new_match = match.Match(this_id, players, ctx.guild)
                matches.update({this_id: new_match})

                msg = f''
                for player in players:
                    msg += f'{player.mention} '
                msg += f'\nYour match is now ready!\nYour match id is: {this_id}\nMatch host: {matches[this_id].host.mention}'
                await ctx.send(msg)
                
                current_id += 1
        else:
            channel = get_player_queue_channel(ctx)
            await ctx.send(f'{ctx.author.mention} is already in a queue.')
    
    # Leave queue command
    @client.command(aliases=['L', 'leave', 'Leave'])
    async def l(ctx):
        if is_in_queue(ctx):
            channel = get_player_queue_channel(ctx)
            queues[channel].remove(ctx.author)
            if len(queues[channel]) == 0:
                queues.pop(channel)
            await ctx.send(f'{ctx.author.name} has been removed from their queue.')
        else:
            await ctx.send(f'{ctx.author.name} is not currently in a queue.')
    
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
    
    # Assigns captains that then select their team members
    @client.command(aliases=['C', 'captains', 'Captains'])
    async def c(ctx):
        id = get_player_match_id(ctx.author)
        await create_vote(ctx, 'captains')

        # Send messages to the captains
        matches[id].messages.append(await matches[id].captain_1.send("Pick a player"))
        #matches[id].messages.append(await matches[id].captain_2.send("Pick a player"))

    # TODO: Balances the teams according to the players' MMR
    @client.command(aliases=['B', 'balance', 'Balance', 'balanced', 'Balanced'])
    async def b(ctx):
        await ctx.send('Coming Soon:tm:')
        return
        await create_vote(ctx, 'balance')
        
    # Assigns teams based on the order the players queued
    # @client.command(aliases=['O', 'ordered', 'Ordered'])
    # async def o(ctx):
    #     await create_vote(ctx, 'ordered')

# Post queue pop commands
    # Lists the id of all the unreported matches
    @client.command()
    async def active(ctx):
        if len(matches) > 0:
            msg = 'List of all the active matches:\n'
            for match in matches:
                msg += f'Id: {match} - '
                if matches[match].sorted:
                    msg += 'Waiting to be reported\n'
                else:
                    msg += 'Waiting for votes on team selection mode\n'
            await ctx.send(msg)
        else:
            await ctx.send('There are no active matches.')
    
    # Reports the match for scoring based on the given id and result and then stores the match in the database.
    @client.command()
    async def report(ctx, id, result):
        if id in matches:
            if ctx.author in match_players[id]:
                if matches[id].sorted:
                    # TODO: Store the result in a database
                    # NOTE: Make this happen inside of match.py so that the variables are easily accessible.

                    await match_clear(ctx, id)
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

    # Custom help command
    async def help(ctx, overload):
        print(f'{overload}')

# Admin Commands -----------------------------------------------
    # Adds the bot_mod_role to the server if it doesn't exist
    @client.command(aliases=['make_role'])
    @commands.has_permissions(manage_roles=True)
    async def create_role(ctx):
        if not role_exists(ctx, bot_mod_role):
            await ctx.guild.create_role(name=bot_mod_role, color=discord.Color(0xff0000))
            print(f'Role {bot_mod_role} has been added to {ctx.guild.name}')
    
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
            await match_clear(ctx, id)
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

# Support methods ---------------------------------------------------------------------
    # Returns the queue channel associated with the given player
    def get_player_queue_channel(ctx):
        for channel in queues:
            for user in queues[channel]:
                if user == ctx.author:
                    return channel

    # Returns true if the command author is in a queue
    def is_in_queue(ctx):
        for channel in queues:
            for user in queues[channel]:
                if user == ctx.author:
                    return True
        return False

    # Returns the match id for the given player
    def get_player_match_id(player):
        for match in match_players:
            if player in match_players[match] and not matches[match].sorted:
                return match
        return '?'

    # Sends the vote of given vote type to the match object of the player who typed the command
    async def create_vote(ctx, vote_type):
        id = get_player_match_id(ctx.author)

        if id == '?':
            await ctx.send(f'{ctx.author.name} has no matches to vote in.')
        else:
            match = matches[id]
            if match.add_vote(ctx.author, vote_type):
                await ctx.send(f"{ctx.author.name}'s vote has been updated.")
            else:
                await ctx.send(f'{ctx.author.name} has voted for: {vote_type} team selection.')

            # If the match vote is successful here, players have their match id, the host, and the 2 teams listed out with @s for the players
            if match.count_votes(queue_max):
                if match.selection_mode != 'captains':
                    await match_setup(ctx, id)

    # Sets up the voice channels and posts the teams after voting
    async def match_setup(ctx, id):
        nonlocal matches

        if len(matches[id].team_1) > 0:
            team_1 = ''
        else:
            team_1 = 'empty'

        for player in matches[id].team_1:
            team_1 += f' {player.name}\n'

        if len(matches[id].team_2) > 0:
            team_2 = ''
        else:
            team_2 = 'empty'

        for player in matches[id].team_2:
            team_2 += f' {player.name}\n'

        embed = nextcord.Embed(title=f'Match {id}', description=f'Match host: {matches[id].host.name}', color=0x9e10e6, timestamp=datetime.today())
        embed.set_thumbnail(url="https://cdnb.artstation.com/p/assets/images/images/039/864/575/original/glitch5970-ezgif-2-11094518d275.gif?1627169802")
        embed.add_field(name="Team 1", value=team_1, inline=True)
        embed.add_field(name="Team 2", value=team_2, inline=True)
        embed.set_image(url="https://marketresearchtelecast.com/wp-content/uploads/2021/12/1638971459_Halo-Infinite-graphics-and-FPS-comparison-on-Xbox-Series-vs-1280x720.jpg")
        embed.set_footer(text="Good Luck Spartans!", icon_url="https://halo.wiki.gallery/images/thumb/6/62/HINF_Fret.png/300px-HINF_Fret.png")
        await ctx.send(embed=embed)

        matches[id].vcs.append(await ctx.guild.create_category(f'Match {id}'))
        matches[id].vcs.append(await ctx.guild.create_voice_channel('Team 1 VC', category=matches[id].vcs[0], user_limit=queue_max/2))
        matches[id].vcs.append(await ctx.guild.create_voice_channel('Team 2 VC', category=matches[id].vcs[0], user_limit=queue_max/2))

    # Clears the vcs of the match that has been reported
    async def match_clear(ctx, id):
        if len(matches[id].vcs) > 0:
            await matches[id].vcs[2].delete()
            await matches[id].vcs[1].delete()
            await matches[id].vcs[0].delete()
            
        match_players.pop(id)
        matches.pop(id)

    # Checks to see if the role of given name exists aleady
    def role_exists(ctx, name):
        roles = ctx.guild.roles
        for role in roles:
            if (role.name == name):
                return True

        return False

    client.run(token)
# _______________________________________________ End of main _______________________________________________

# Calls main (run with: "python3 main.py") __________________________________________________________________
if __name__ == '__main__':
    main()
