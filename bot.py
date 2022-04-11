import os
import discord
import asyncio
import tweepy
from server import keep_alive
from dotenv import load_dotenv

consumer_key = os.getenv("CK")
consumer_secret = os.getenv("CS")
key = os.getenv("KEY")
secret = os.getenv("TOKEN")
channel_ID = os.getenv("CHANNEL")
discord_token = os.getenv("TOKEN")
user_ID = os.getenv("USER")
twitter_ID = os.getenv("TWITTER") 


checker = []
key_words = ["closed", "two hours", "canceled", "virtual", "weather", "release"]

game = discord.Game("At your service")
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        await client.change_presence(status=discord.Status.online, activity=game)
        discord.Game("At your service")

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(channel_ID)

        while not self.is_closed():
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(key,secret)
            api = tweepy.API(auth)
            tweet = api.user_timeline(screen_name = twitter_ID, count = 100, include_rts = True)[0]
            link = api.get_oembed("https://twitter.com/{}/status/{}".format(twitter_ID,tweet.id))

            for word in key_words:
                if(word in tweet.text and link["url"] not in checker):
                    await channel.send(user_ID)
                    await channel.send(link["url"])
                    checker.append(link["url"])
            await asyncio.sleep(20)


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
keep_alive()

client.run(discord_token)