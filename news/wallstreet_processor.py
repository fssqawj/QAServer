# coding: utf-8
from parser import BaseProcessor
import json
import time
from bs4 import BeautifulSoup
from wrapper import timer
from utils import create_path


class WallStreetProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, path, start=0, max_fetch_cnt=50):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self._start = start
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'https://api-prod.wallstreetcn.com/apiv1/content/articles?category=global&limit=100'
        self.summary_urls = [self.base_url]
        self._path = path
        self.summary_saved_file = self._path + '/summary_{}.txt'
        self.detail_saved_file = self._path + '/detail_{}.txt'
        self._source = 'WallStreet'

        create_path(self._path)

    @timer
    def extract_summary(self, fetch_detail=False):
        for item in self.get_summary_workers():
            res = item.worker.result().decode('utf-8')
            json_res = json.loads(res)
            for obj in json_res['data']['items']:
                self.summary_candidates.append(obj)
        return self.summary_candidates

    @timer
    def extract_details(self):
        for item in self.get_detail_workers():
            soup = BeautifulSoup(item.worker.result(), 'lxml')
            if soup.select_one('div.article__heading__title') is None:
                continue
            self.detail_candidates.append({'title': soup.select_one('div.article__heading__title').text,
                                           'content': soup.select_one('div.node-article-content').text})
        return self.detail_candidates

    def add_detail_url(self, item):
        self.detail_urls.append(item['uri'])

    @staticmethod
    def judge_in_this_day(day, item):
        return time.strftime('%Y-%m-%d', time.localtime(item['display_time'])) == day
