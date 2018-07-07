# coding: utf-8
from parser.htmlfetch import fetch_page


class JobWorker:
    def __init__(self, worker, url):
        self.worker = worker
        self.url = url


class BaseProcessor:
    def __init__(self):
        self.base_url = None
        self.summary_urls = []
        self.detail_urls = []
        self.crawler_worker_loop = None
        self.summary_workers = None
        self.detail_workers = []
        self.summary_candidates = []
        self.detail_candidates = []

    def submit_summary_job(self, query=None):
        if query is not None:
            self.summary_workers = [JobWorker(fetch_page(self.crawler_worker_loop, summary_url.format(query)),
                                              summary_url.format(query)) for summary_url in self.summary_urls]
        else:
            self.summary_workers = [JobWorker(fetch_page(self.crawler_worker_loop, url), url)
                                    for url in self.summary_urls]
        return self

    def submit_detail_jobs(self):
        self.detail_workers = [JobWorker(fetch_page(self.crawler_worker_loop, detail_url), detail_url)
                               for detail_url in self.detail_urls]
        return self

    def submit_job(self, url):
        return JobWorker(fetch_page(self.crawler_worker_loop, url), url)

    def get_summary_workers(self):
        return self.summary_workers

    def get_detail_workers(self):
        return self.detail_workers

    def extract_summary(self):
        pass

    def extract_details(self):
        pass
