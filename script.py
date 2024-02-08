import asyncio
import datetime

import aiohttp

from models import Session, SwapiPeople, engine, init_db

CHUNK = 10


async def get_person(client, person_id):
    http_response = await client.get(f"https://swapi.py4e.com/api/people/{person_id}/")
    json_result = await http_response.json()
    return json_result


async def insert_to_db(data_list):
    models = [
        SwapiPeople(
            name=json_item["name"],
            height=json_item["height"],
            mass=json_item["mass"],
            hair_color=json_item["hair_color"],
            skin_color=json_item["skin_color"],
            eye_color=json_item["eye_color"],
            birth_year=json_item["birth_year"],
            gender=json_item["gender"],
            homeworld=json_item["homeworld"],
            films=json_item["films"],
            species=json_item["species"],
            vehicles=json_item["vehicles"],
            starships=json_item["starships"],
        )
        for json_item in data_list
    ]
    async with Session() as session:
        session.add_all(models)
        await session.commit()


async def main():
    await init_db()
    client = aiohttp.ClientSession()
    last_person = 1
    strike = 0
    while True:
        coros = []
        for person in range(last_person, last_person + CHUNK):
            content = get_person(client, person)
            coros.append(content)
        result = await asyncio.gather(*coros)
        strike += 1 if not all("detail" not in item for item in result) else 0
        result_after_check = [item for item in result if "detail" not in item]
        # print(result_after_check)
        insert_task = asyncio.create_task(insert_to_db(result_after_check))
        last_person += CHUNK
        if strike > 1:
            break

    task_set = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*task_set)

    await client.close()
    await engine.dispose()


if __name__ == "__main__":
    # start = datetime.datetime.now()
    asyncio.run(main())
    # print(datetime.datetime.now() - start)
