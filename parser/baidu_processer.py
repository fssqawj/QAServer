# coding: utf-8
from parser.base_processor import BaseProcessor
from bs4 import BeautifulSoup
from cqa.cqa_meta import CqaMeta


class BaiduProcessor(BaseProcessor):
    def __init__(self, crawler_worker_loop, max_fetch_cnt=3):
        super().__init__()
        self._max_fetch_cnt = max_fetch_cnt
        self.crawler_worker_loop = crawler_worker_loop
        self.base_url = 'http://zhidao.baidu.com/search?word={}&pn='
        self.page_num = [x * 10 for x in range(max_fetch_cnt // 10 + 1)]
        self.summary_urls = [self.base_url + str(x) for x in self.page_num]
        self._source = 'Baidu'

    def extract_summary(self, fetch_detail=True):
        total_idx = 0
        for item in self.get_summary_workers():
            soup = BeautifulSoup(item.worker.result(), 'lxml')
            titles_bd = soup.select('dt')
            answers_bd = soup.select("dd.dd.answer")
            for idx, title in enumerate(titles_bd):
                if idx >= len(answers_bd) or total_idx >= self._max_fetch_cnt:
                    break
                total_idx += 1
                cqa = CqaMeta(item.url).set_question(title.get_text())\
                    .set_best_answer(answers_bd[idx].get_text())\
                    .set_source(self._source)
                self.summary_candidates.append(cqa)
                if fetch_detail:
                    self.detail_urls.append(title.a['href'])
                    self.detail_workers.append(self.submit_job(title.a['href']))
        return self.summary_candidates

    def extract_details(self):
        print(self.detail_urls)
        for item in self.get_detail_workers():
            soup = BeautifulSoup(item.worker.result(), 'lxml')
            try:
                if soup.select_one('span.ask-title') is None:
                    cqa = self.extract_baike_page(soup, item.url)
                else:
                    candidate_answers = []
                    for candidate in soup.select('div.answer-text.line'):
                        candidate_answers.append(candidate.text)
                    best_answer_tag = soup.select_one('pre.best-text.mb-10')
                    if best_answer_tag is None:
                        best_answer_tag = soup.select_one('div.best-text.mb-10')
                    cqa = CqaMeta(item.url).set_question(soup.select_one('span.ask-title'))\
                        .set_description(soup.select_one('span.con'))\
                        .set_best_answer(best_answer_tag)\
                        .set_update_time(soup.select_one('span.grid-r.f-aid.pos-time.answer-time.f-pening'))\
                        .set_source(self._source)\
                        .set_candidates(candidate_answers)
                self.detail_candidates.append(cqa)
            except AttributeError as e:
                print(e)
        return self.detail_candidates

    @staticmethod
    def extract_baike_page(soup, url):
        return CqaMeta(url).set_question(soup.select_one('dd.lemmaWgt-lemmaTitle-title'))\
            .set_best_answer(soup.select_one('div.lemma-summary'))
