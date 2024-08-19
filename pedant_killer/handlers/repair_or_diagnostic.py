from aiogram import Router, F
rt_2 = Router()

@rt_2.message(F.text == "Нужен ремонт/диагностика устройства")
async def 