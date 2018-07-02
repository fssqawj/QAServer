# coding: utf8
import aiohttp
import asyncio
import async_timeout

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}


async def downloader(session, url, time_out=10):
    with async_timeout.timeout(time_out):
        async with session.get(url, headers=header) as response:
            content = await response.content.read()
            return content


async def runner(loop, urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [downloader(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def fetch_pages(urls):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(runner(loop, urls))


if __name__ == '__main__':
    urls = ['http://zhidao.baidu.com/search?word={}',
            'http://wenwen.sogou.com/s/?w={}',
            'http://iask.sina.com.cn/search?searchWord={}',
            'http://wenda.so.com/search/?q={}',
            'https://www.zhihu.com/search?q={}',
            ]
    encodings = ['gbk', 'utf-8', 'utf-8', 'utf-8', 'utf-8']
    print(fetch_pages(urls))
