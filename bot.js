import discord
from discord.ext import commands, tasks
import os

# -------------------------- CONFIGURATION --------------------------
# Loads from Railway Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
PING = True  # Set to False to stop @everyone spam
MESSAGE = "Fand is Mega Chopped"

# YOUR IMAGES
IMAGE_LINKS = [
    "https://i.imgur.com/8sYxQ8L.jpg",
    "https://i.imgur.com/9kRzX2P.jpg"
]
# -------------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ FAND IS CHOPPED BOT ONLINE | Logged in as: {bot.user}")
    send_announcement.start()

# RUNS EVERY 10 MINUTES
@tasks.loop(minutes=10)
async def send_announcement():
    ping_text = "@everyone " if PING else ""
    full_msg = f"{ping_text}{MESSAGE}"

    # Send to first available channel per server
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    embeds = [discord.Embed().set_image(url=url) for url in IMAGE_LINKS]
                    await channel.send(content=full_msg, embeds=embeds)
                    print(f"✅ Sent to {guild.name}")
                    break
                except:
                    continue

@send_announcement.before_loop
async def wait_ready():
    await bot.wait_until_ready()

bot.run(BOT_TOKEN)
