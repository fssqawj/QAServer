# coding: utf-8


class Processor:
    def __init__(self):
        self._processors = []

    def register(self, processor):
        self._processors.append(processor)
        return self

    def start_summary_jobs(self, query):
        for processor in self._processors:
            processor.submit_summary_job(query)
        return self

    def fetch_summary_results(self, query):
        self.start_summary_jobs(query)
        summary_candidates = []
        for item in self._processors:
            summary_candidates += item.extract_summary(fetch_detail=False)
        return summary_candidates

    def fetch_detail_results(self, query):
        self.start_summary_jobs(query)
        detail_candidates = []
        for processor in self._processors:
            processor.extract_summary()
            detail_candidates += processor.extract_details()
        return detail_candidates

    def fetch_results(self, query, fetch_detail=True):
        if fetch_detail:
            return self.fetch_detail_results(query)
        return self.fetch_summary_results(query)
