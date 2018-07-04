# coding: utf-8
from parser.base_processor import BaseProcessor
from bs4 import BeautifulSoup
from cqa.cqa_meta import CqaMeta


class SoProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, max_fetch_cnt=3):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'http://wenda.so.com/search/?q={}'
        self._source = '360'

    def extract_summary(self):
        soup = BeautifulSoup(self.get_summary_result(), 'lxml')
        titles = soup.select('div.qa-i-hd')
        answers = soup.select('div.qa-i-bd')
        for idx, title in enumerate(titles):
            if idx >= len(answers) or idx >= self._max_fetch_cnt:
                break
            cqa = CqaMeta().set_question(title.get_text())\
                .set_best_answer(answers[idx].get_text())\
                .set_source(self._source)
            self.summary_candidates.append(cqa)

            self.detail_urls.append(title.h3.a['href'])
        return self.summary_candidates

    def extract_details(self):
        raise NotImplementedError
