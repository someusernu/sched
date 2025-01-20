import base
import asyncio


async def main():
    # await base.drop_base()
    await base.create_base()
    await base.create_tables()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
