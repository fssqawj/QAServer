# coding: utf-8
import asyncio
from threading import Thread
from news import CaiXinProcessor, WallStreetProcessor
from parser import start_crawler_worker
from news import run

if __name__ == '__main__':
    crawler_worker_loop = asyncio.new_event_loop()
    running = Thread(target=start_crawler_worker, args=(crawler_worker_loop,))
    running.setDaemon(True)
    running.start()

    cai_xin_data_path = './newsdata/caixin'
    wall_street_data_path = './newsdata/wallstreet'
    run(CaiXinProcessor(crawler_worker_loop, cai_xin_data_path))
    run(WallStreetProcessor(crawler_worker_loop, wall_street_data_path))
