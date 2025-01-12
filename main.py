import os
import discord
from discord.ext import commands

# Считаем токен из переменных среды (Railway позволяет хранить секреты там)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
if not DISCORD_TOKEN:
    raise ValueError("Не найден DISCORD_TOKEN в переменных окружения")

# Указываем нужные Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот залогинился как {bot.user} (ID: {bot.user.id})")

@bot.command()
async def ping(ctx):
    """Простейшая команда !ping"""
    await ctx.send("Pong!")

# Запуск
bot.run(DISCORD_TOKEN)
