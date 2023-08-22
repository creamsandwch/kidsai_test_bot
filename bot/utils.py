import aiohttp


async def create_media_id(data, url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, data=data) as response:
            return response.status


async def update_media_id(data, url, id):
    url += f'{id}/'
    async with aiohttp.ClientSession() as session:
        async with session.patch(url=url, data=data) as response:
            return response.status


async def search_for_file_by_name(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url, params={'filename': filename}
        ) as response:
            resp_json = await response.json()
            return resp_json
