# coding: utf-8
from parser.htmlfetch import fetch_page


class BaseProcessor:
    def __init__(self):
        self.base_url = None
        self.detail_urls = []
        self.crawler_worker_loop = None
        self.summary_worker = None
        self.detail_workers = []
        self.summary_candidates = []
        self.detail_candidates = []

    def submit_summary_job(self, query):
        self.summary_worker = fetch_page(self.crawler_worker_loop, self.base_url.format(query))

    def submit_detail_jobs(self):
        self.detail_workers = [fetch_page(self.crawler_worker_loop, detail_url) for detail_url in self.detail_urls]

    def get_summary_result(self):
        return self.summary_worker.result()

    def get_detail_results(self):
        return [detail_worker.result() for detail_worker in self.detail_workers]

    def extract_summary(self):
        pass

    def extract_details(self):
        pass

