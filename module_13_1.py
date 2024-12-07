# Асинхронность на практике
# Асинхронные силачи

import asyncio
import time


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнование')
    ExecutionTime = 1 / power
    for i in range(5):
        await asyncio.sleep(ExecutionTime)
        print(f'Силач {name} поднял шар номер {i + 1}')
    print(f'Силач {name} закончил соревнование')


async def start_tournament():
    st_st1 = asyncio.create_task(start_strongman('Вася', 3))
    st_st2 = asyncio.create_task(start_strongman('Петя', 4))
    st_st3 = asyncio.create_task(start_strongman('Жорж', 5))
    await st_st1
    await st_st2
    await st_st3


asyncio.run(start_tournament())
