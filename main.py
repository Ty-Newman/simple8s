import os
import random
import nextcord
from dotenv.main import load_dotenv
from nextcord.ext import commands

client = nextcord.Client()

def main():
    load_dotenv()
    token = os.getenv("TOKEN")

    client = commands.Bot(command_prefix="?")

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord! UwU")

    @client.event
    async def on_message(message):
        mess = message.content

        if message.author == client.user:
            return

        if mess.startswith('$hello'):
            await message.channel.send('Hello!')
        elif mess.startswith('?bigmantime'):
            if (random.randint(0, 1) == 0):
                await message.channel.send('https://www.youtube.com/watch?v=2XDfp4_eZf4')
            else:
                await message.channel.send('https://www.youtube.com/watch?v=N06fZxoUQx0')

    @client.command()
    async def test(ctx):
        print("Inside test command...")
        await ctx.send("Test succ")

    client.run(token)

if __name__ == '__main__':
    main()
