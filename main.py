import os
import discord
from discord.ext import commands
from flask import Flask, jsonify

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("Не найден DISCORD_TOKEN в переменных окружения")

# Храним последнее сообщение в переменной
last_message = ""

# Создаём Flask-приложение
app = Flask(__name__)

@app.route("/")
def index():
    return "OK, bot is running!"

@app.route("/latest")
def get_latest():
    # Возвращаем JSON с последним сообщением
    return jsonify({"message": last_message})

# Discord-бот
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def val(ctx, *, text: str = None):
    global last_message
    if not text:
        await ctx.send("Вы не написали текст после !val")
        return
    last_message = text
    await ctx.send(f"Сохранил для Minecraft: {text}")

# Запуск бота и Flask вместе
if __name__ == "__main__":
    import threading

    # 1) Поток для Discord-бота
    def run_discord():
        bot.run(DISCORD_TOKEN)

    t = threading.Thread(target=run_discord)
    t.start()

    # 2) Запускаем Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
