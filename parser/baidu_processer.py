# coding: utf-8
from parser.base_processor import BaseProcessor
from bs4 import BeautifulSoup
from cqa.cqa_meta import CqaMeta


class BaiduProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, max_fetch_cnt=3):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'http://zhidao.baidu.com/search?word={}'
        self._source = 'Baidu'

    def extract_summary(self):
        soup = BeautifulSoup(self.get_summary_result(), 'lxml')
        titles_bd = soup.select('dt')
        answers_bd = soup.select("dd.dd.answer")
        for idx, title in enumerate(titles_bd):
            if idx >= len(answers_bd) or idx >= self._max_fetch_cnt:
                break
            cqa = CqaMeta().set_question(title.get_text())\
                .set_best_answer(answers_bd[idx].get_text())\
                .set_source(self._source)
            self.summary_candidates.append(cqa)

            self.detail_urls.append(title.a['href'])
        return self.summary_candidates

    def extract_details(self):
        print(self.detail_urls)
        for item in self.get_detail_results():
            soup = BeautifulSoup(item, 'lxml')
            try:
                print(soup.select_one('span.ask-title').text)
                cqa = CqaMeta().set_question(soup.select_one('span.ask-title'))\
                    .set_description(soup.select_one('span.con'))\
                    .set_best_answer(soup.select_one('pre.best-text.mb-10'))\
                    .set_update_time(soup.select_one('span.grid-r.f-aid.pos-time.answer-time.f-pening'))\
                    .set_source(self._source)
                self.detail_candidates.append(cqa)
            except AttributeError as e:
                print(e)
        return self.detail_candidates
