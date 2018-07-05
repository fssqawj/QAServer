# coding: utf-8
from score import candidate_sort
from parser import BaiduProcessor, SougouProcessor, SoProcessor, ZhihuProcessor, Processor


def process_community_site(crawler_worker_loop, query):
    processor = Processor().register(ZhihuProcessor(crawler_worker_loop, max_fetch_cnt=35))\
        .register(BaiduProcessor(crawler_worker_loop, max_fetch_cnt=35))\
        .register(SougouProcessor(crawler_worker_loop, max_fetch_cnt=35))\
        .register(SoProcessor(crawler_worker_loop, max_fetch_cnt=35))
    return candidate_sort(query, processor.fetch_results(query, fetch_detail=False))


if __name__ == '__main__':
    pass
