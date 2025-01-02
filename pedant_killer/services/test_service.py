from device_service import DeviceServiceService
import asyncio


async def ggvp():
    m = DeviceServiceService()
    g = await m.get_relationship_order(7)
    # m = await s.save_user(27, 'i_am_gg', 'sdfsdf', 'dima', 'cherepovets', '9000000000')
    print(g)

asyncio.run(ggvp())
