
import time


async def fake_reading_file():
    print("Reading file content")
    # time.sleep(5)
    await asyncio.sleep(5)
    print("file content read")


async def main():
    print("start time", time.time())
    print("Start reading file")

    tasks = []
    # for _ in range(3):
    #     task = asyncio.create_task(fake_reading_file())
    #     tasks.append(task)

    while True:
        user_input = input("Do you want to read the file? (y/n)")
        if user_input == 'y':
            tasks.append(asyncio.create_task(fake_reading_file()))
            # await fake_reading_file()
        else:
            break

    await asyncio.gather(*tasks)
    print("End reading file")
    print("end time", time.time())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
