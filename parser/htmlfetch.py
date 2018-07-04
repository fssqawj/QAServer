# coding: utf8
import aiohttp
import asyncio
import async_timeout
from threading import Thread
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}


async def downloader(loop, url, time_out=10):
    with async_timeout.timeout(time_out):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url, headers=header) as response:
                content = await response.content.read()
                return content


def fetch_pages_in_loop(loop, urls):
    feature_works = [fetch_page(loop, url) for url in urls]
    return [res_run.result() for res_run in feature_works]


def fetch_page(loop, url):
    return asyncio.run_coroutine_threadsafe(downloader(loop, url), loop)


def start_crawler_worker(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def fetch_pages(urls):
    return [requests.get(url, headers=header).text for url in urls]


if __name__ == '__main__':
    urls = ['http://zhidao.baidu.com/search?word={}',
            'http://wenwen.sogou.com/s/?w={}',
            'http://iask.sina.com.cn/search?searchWord={}',
            'http://wenda.so.com/search/?q={}',
            'https://www.zhihu.com/search?q={}']
    # encodings = ['gbk', 'utf-8', 'utf-8', 'utf-8', 'utf-8']
    # print(fetch_pages(urls))
    crawler_worker_loop = asyncio.new_event_loop()
    Thread(target=start_crawler_worker, args=(crawler_worker_loop,)).start()
    res = fetch_pages_in_loop(crawler_worker_loop, urls)
    print(len(res), res)
