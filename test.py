import asyncio, aiohttp, ujson


async def test_tasker_connect(method='get'):
    header = {
        'Authorization': 'kzBE8Q1KmeBkx_uD'
    }

    data = {
        'name': 'wezzyofficial'
    }

    session = aiohttp.ClientSession(
        headers=header,
        json_serialize=ujson.dumps,
        trust_env=True,
        connector=aiohttp.TCPConnector(verify_ssl=True)
    )

    if method == 'get':
        handler = session.get
    else:
        handler = session.post

    async with handler('http://localhost:8080/test', json=data) as response:
        try:
            answer = await response.text()
        except:
            answer = None

    await session.close()

    print(answer)

    return answer


if __name__ == "__main__":
    asyncio.run(test_tasker_connect(method='get'))