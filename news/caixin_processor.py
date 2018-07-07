# coding: utf-8
from parser import BaseProcessor
import json
from bs4 import BeautifulSoup
from wrapper import timer


class CaixinProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, start=0, max_fetch_cnt=50):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self._start = start
        self.crawler_worker_loop = crawler_worker_loop
        self.channels = {"economy": 129, "finance": 125, "companies": 130, "china": 131, "science": 179,
                         "international": 132, "culture": 134}
        self.base_url = 'http://tag.caixin.com/news/homeInterface.jsp?' \
                        'channel={}&start={}&count={}&picdim=_145_97' \
                        '&callback=jQuery17209677058548357216_1530938601322&_=1530938933631'
        self.comment_url = 'http://file.c.caixin.com/comment-sync/js/100/{}/{}.js'
        self.summary_urls = [self.base_url.format(str(channel), self._start, self._max_fetch_cnt)
                             for _, channel in self.channels.items()]
        self._source = 'Caixin'

    @timer
    def extract_summary(self, fetch_detail=False):
        for item in self.get_summary_workers():
            res = item.worker.result().decode('utf-8')
            res = res[res.index("datas") - 2:res.rindex("}") + 1]
            json_res = json.loads(res)
            for obj in json_res['datas']:
                self.summary_candidates.append(obj)
        return self.summary_candidates

    @timer
    def extract_details(self):
        for item in self.get_detail_workers():
            passage_id = item.url[-14:-5]
            soup = BeautifulSoup(item.worker.result(), 'lxml')
            comments = self.submit_job(self.comment_url.format(passage_id[-3:], passage_id))\
                .worker.result().decode('utf-8')
            comments = json.loads(comments[comments.index('{'):comments.rindex('}') + 1])
            user_comments = []
            for comment in comments['list']:
                user_comments.append(comment['content'])
            self.detail_candidates.append({'title': soup.select_one('h1').text,
                                           'content': soup.select_one('div.textbox').text,
                                           'comments': user_comments})
        return self.detail_candidates
