import discord
from google import genai
import os
import requests

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
DIFY_SEARCH_URL = os.environ["DIFY_SEARCH_URL"]
DIFY_API_KEY = os.environ["DIFY_API_KEY"]

client_ai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def search_memory(keyword):
    try:
        r = requests.post(
            DIFY_SEARCH_URL,
            headers={"Authorization": f"Bearer {DIFY_API_KEY}", "Content-Type": "application/json"},
            json={"inputs": {"keyword": keyword}, "response_mode": "blocking", "user": "bot"}
        )
        data = r.json()
        return data.get("data", {}).get("outputs", {}).get("result", "")
    except:
        return ""

@client.event
async def on_ready():
    print(f"Bot已上线: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    memory = search_memory(message.content[:20])
    prompt = f"相关记忆: {memory}\n\n用户说: {message.content}" if memory else message.content
    response = client_ai.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    await message.channel.send(response.text[:2000])

client.run(DISCORD_TOKEN)
