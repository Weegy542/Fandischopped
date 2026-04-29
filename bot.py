import discord
from discord.ext import commands, tasks
import os
import time

# -------------------------- CONFIG --------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
PING_EVERYONE = True
MESSAGE = "Fand is Mega Chopped"
IMAGE_LINKS = [
    "https://i.imgur.com/8sYxQ8L.jpg",
    "https://i.imgur.com/9kRzX2P.jpg"
]
# ------------------------------------------------------------

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("="*50)
    print(f"✅ SUCCESS! LOGGED IN AS: {bot.user}")
    print(f"✅ BOT ID: {bot.user.id}")
    print(f"✅ CONNECTED TO {len(bot.guilds)} SERVER(S)")
    print("✅ ANNOUNCEMENT LOOP STARTED (EVERY 10 MINS)")
    print("="*50)
    if not send_message.is_running():
        send_message.start()

@tasks.loop(minutes=10)
async def send_message():
    ping = "@everyone " if PING_EVERYONE else ""
    content = f"{ping}{MESSAGE}"

    for guild in bot.guilds:
        # Find first channel bot can send messages
        channel = next((ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages), None)
        if channel:
            try:
                embeds = [discord.Embed().set_image(url=url) for url in IMAGE_LINKS]
                await channel.send(content=content, embeds=embeds)
                print(f"📢 Sent to: {guild.name} -> #{channel.name}")
            except Exception as e:
                print(f"⚠️ Send Error: {str(e)}")

@send_message.before_loop
async def wait_start():
    await bot.wait_until_ready()

# RUN BOT
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN NOT FOUND IN RAILWAY VARIABLES!")
        exit()
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ ERROR: INVALID BOT TOKEN! Go to Discord Dev Portal -> Bot -> Reset Token")
    except Exception as e:
        print(f"❌ CRASH: {str(e)}")
