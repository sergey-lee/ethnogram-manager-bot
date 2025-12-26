import asyncio
from fastapi import FastAPI, Request
from bot import bot, dp

# WEBHOOK_URL = "https://your-railway-url/webhook"
WEBHOOK_URL = "https://ethnogram-manager-bot-production.up.railway.app/webhook"
app = FastAPI()

@app.on_event("startup")
async def on_start():
    await bot.set_webhook(WEBHOOK_URL)

@app.post("/webhook")
async def webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot, update)
    return {"ok": True}
