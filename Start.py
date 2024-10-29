import asyncio
from Instruments.Config import bot, dp, fapi
import uvicorn

from Information.Start import rs
from Information.Date import rd
from Information.FullName import rfn
from Information.Phone import rp
from Information.Cities import rc
from Information.Confirmation import rco
from Information.Categories import rca

from Operator.Conversation import roc
from Operator.MissText import rot

from Categories.Categories import rcc
from Categories.Rate import rcr

from Omnidesk.Reminder import rr

from Omnidesk.Receiving import router

dp.include_routers(rs, rd, rfn, rp, rc, rco, rca, roc, rot, rcc, rcr, rr)


async def start_fastapi():
    fapi.include_router(router)
    config = uvicorn.Config(fapi, host="0.0.0.0", port=8080)
    server = uvicorn.Server(config)
    await server.serve()


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def start():
    await asyncio.gather(start_fastapi(), start_bot())


if __name__ == "__main__":
    asyncio.run(start())
