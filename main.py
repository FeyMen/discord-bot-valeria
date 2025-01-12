import os
import discord
from discord.ext import commands
from flask import Flask, jsonify

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", None)
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not found!")

# Храним последнее сообщение
last_message = ""

app = Flask(__name__)

@app.route("/")
def index():
    return "OK, bot is running"

@app.route("/latest")
def get_latest():
    return f'{{message="{last_message}"}}'


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def v(ctx, *, text: str = None):
    global last_message
    if not text:
        await ctx.send("Пожалуйста, введите текст после !v")
        return
    last_message = text
    await ctx.send(f"Сохранил для Minecraft: {text}")

if __name__ == "__main__":
    import threading

    def run_discord():
        bot.run(DISCORD_TOKEN)

    # Запускаем бота в отдельном потоке
    t = threading.Thread(target=run_discord)
    t.start()

    # Запускаем Flask на порту Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
