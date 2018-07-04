# coding: utf-8
from score import candidate_sort
from parser import BaiduProcessor, SougouProcessor, SoProcessor, ZhihuProcessor


def process_community_site(crawler_worker_loop, query):
    processors = [BaiduProcessor(crawler_worker_loop),
                  SougouProcessor(crawler_worker_loop),
                  SoProcessor(crawler_worker_loop),
                  ZhihuProcessor(crawler_worker_loop)]
    for item in processors:
        item.submit_summary_job(query)

    summary_candidates = []
    for item in processors:
        summary_candidates += item.extract_summary()
        item.submit_detail_jobs()

    return candidate_sort(query, summary_candidates)


if __name__ == '__main__':
    pass
