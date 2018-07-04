# coding: utf-8
from parser.base_processor import BaseProcessor
from bs4 import BeautifulSoup
from cqa.cqa_meta import CqaMeta


class SougouProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, max_fetch_cnt=3):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'http://www.sogou.com/sogou?query={}&insite=wenwen.sogou.com'
        self._source = 'Sougou'

    def extract_summary(self):
        soup = BeautifulSoup(self.get_summary_result(), 'lxml')
        cards = soup.select('div.vrwrap')
        for idx, card in enumerate(cards):
            if idx >= self._max_fetch_cnt:
                break
            cqa = CqaMeta().set_question(card.select_one('h3.vrTitle').get_text().replace('- 搜狗问问', '').replace('_搜狗问问', '').strip())\
                .set_best_answer(card.select('div.str-text-info')[-1].get_text().replace('最佳答案', '').strip())\
                .set_source(self._source)
            self.summary_candidates.append(cqa)

            self.detail_urls.append(card.select_one('h3.vrTitle').a['href'])
        return self.summary_candidates

    def extract_details(self):
        raise NotImplementedError
