# coding: utf-8
import json
import time
import codecs


def run(processor):
    today = time.strftime("%Y-%m-%d", time.localtime())
    with codecs.open(processor.summary_saved_file.format(today), 'w',
                     encoding='utf-8') as f:
        for item in processor.submit_summary_job().extract_summary():
            if processor.judge_in_this_day(today, item):
                processor.add_detail_url(item)
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    with codecs.open(processor.detail_saved_file.format(today), 'w',
                     encoding='utf-8') as f:
        for item in processor.submit_detail_jobs().extract_details():
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
