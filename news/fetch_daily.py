# coding: utf-8
import asyncio
from threading import Thread
from news import CaixinProcessor
from parser import start_crawler_worker
import json
import time
import codecs


def run(data_file):
    crawler_worker_loop = asyncio.new_event_loop()
    running = Thread(target=start_crawler_worker, args=(crawler_worker_loop,))
    running.setDaemon(True)
    running.start()
    summary_saved_file = data_file + '/summary_data_{}.txt'
    detail_saved_file = data_file + '/detail_data_{}.txt'
    today = time.strftime("%Y-%m-%d", time.localtime())
    processor = CaixinProcessor(crawler_worker_loop)
    with codecs.open(summary_saved_file.format(today), 'w', encoding='utf-8') as f:
        for item in processor.submit_summary_job().extract_summary():
            if today in item['time']:
                processor.detail_urls.append(item['link'])
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    with codecs.open(detail_saved_file.format(today), 'w', encoding='utf-8') as f:
        for item in processor.submit_detail_jobs().extract_details():
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
