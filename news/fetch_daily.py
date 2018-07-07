# coding: utf-8
import asyncio
from threading import Thread
from parser.htmlfetch import start_crawler_worker
from news import CaixinProcessor
import json
import time
import codecs

if __name__ == '__main__':
    crawler_worker_loop = asyncio.new_event_loop()
    running = Thread(target=start_crawler_worker, args=(crawler_worker_loop,))
    running.setDaemon(True)
    running.start()
    saved_file = '../newsdata/data_{}.txt'
    today = time.strftime("%Y-%m-%d", time.localtime())
    with codecs.open(saved_file.format(today), 'w', encoding='utf-8') as f:
        for item in CaixinProcessor(crawler_worker_loop).submit_summary_job().extract_summary():
            if today in item['time']:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
