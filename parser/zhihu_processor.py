# coding: utf-8
from parser.base_processor import BaseProcessor
import asyncio
from threading import Thread
import json
from cqa import CqaMeta
from parser.htmlfetch import start_crawler_worker
from wrapper import timer


class ZhihuProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, max_fetch_cnt=3):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'https://www.zhihu.com/api/v4/search_v3?' \
                        't=general&q={}&correction=1&offset=0&search_hash_id=87899&limit='
        self.summary_urls = [self.base_url + str(max_fetch_cnt)]
        self._source = 'Zhihu'

    @timer
    def extract_summary(self, fetch_detail=False):
        for item in self.get_summary_workers():
            json_res = json.loads(item.worker.result())

            for tag in json_res['data']:
                if tag['type'] == 'search_result':
                    self.summary_candidates.append(CqaMeta(item.url).set_question(tag['highlight']['title'])
                                                   .set_best_answer(tag['highlight']['description'])
                                                   .set_source(self.base_url))
        return self.summary_candidates

    def extract_details(self):
        raise NotImplementedError


if __name__ == '__main__':
    crawler_worker_loop = asyncio.new_event_loop()
    Thread(target=start_crawler_worker, args=(crawler_worker_loop,)).start()
    pro = ZhihuProcessor(crawler_worker_loop)
    pro.submit_summary_job('华东师范大学在什么地方')
    pro.extract_summary()
