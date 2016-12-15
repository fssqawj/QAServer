# coding: utf8
import requests
from bs4 import BeautifulSoup


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}

max_fetch_cnt = 3

def process_baidu(p, titles, answers, scores):
    url = 'http://zhidao.baidu.com/search?word={}'.format(p)
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "gbk"

    soup = BeautifulSoup(r.text)
    titles_bd = soup.select('dt')
    answers_bd = soup.select("dd.dd.answer")
    # titles += [x.get_text() for x in titles_bd]
    # answers += [x.get_text() for x in answers_bd]
    for idx, title in enumerate(titles_bd):
        if idx >= len(answers_bd) or idx >= max_fetch_cnt:
            break
        titles.append(title.get_text())
        answers.append(answers_bd[idx].get_text())
        scores.append('Baidu')


def process_sina(p, titles, answers, scores):
    url = 'http://iask.sina.com.cn/search?searchWord={}'.format(p)
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text)
    # titles_sina = soup.select('dt')
    # answers_sina = soup.select("dd.dd.answer")
    searchList = soup.select('div.search_item')
    for item in searchList[1:min(max_fetch_cnt, len(searchList))]:
        titles.append(item.h2.text)
        answ = item.div.text
        answers.append(answ[answ.find('答：'):answ.find('详细>')])
        scores.append('Sina')


def process_360(p, titles, answers, scores):
    url = 'http://wenda.so.com/search/?q={}'.format(p)
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text)
    titles_360 = soup.select('div.qa-i-hd')
    answers_360 = soup.select('div.qa-i-bd')
    titles += [x.get_text() for x in titles_360][:min(max_fetch_cnt, len(titles_360))]
    answers += [x.get_text() for x in answers_360][:min(max_fetch_cnt, len(titles_360))]
    scores += ['360' for _ in titles_360][:min(max_fetch_cnt, len(titles_360))]


def process_sougou(p, titles, answers, scores):
    url = 'http://wenwen.sogou.com/s/?w={}'.format(p)
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text)
    titles_sougou = soup.select('h3.result-title.sIt_title')
    answers_sougou = soup.select('div.result-summary')
    titles += [x.get_text() for x in titles_sougou][:min(max_fetch_cnt, len(titles_sougou))]
    answers += [x.get_text() for x in answers_sougou][:min(max_fetch_cnt, len(titles_sougou))]
    scores += ['Sougou' for _ in titles_sougou][:min(max_fetch_cnt, len(titles_sougou))]


def process_zhihu(p, titles, answers, scores):
    url = 'https://www.zhihu.com/search?q={}'.format(p)
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "utf-8"
    open('zhihu.txt', 'w').write(r.text)
    soup = BeautifulSoup(r.text)
    titles_zhihu = soup.select('div.title')
    answers_zhihu = soup.select('div.summary.hidden-expanded')
    titles += [x.get_text() for x in titles_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]
    answers += [x.get_text() for x in answers_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]
    scores += ['Zhihu' for _ in titles_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]


def process_test():
    url = 'http://zhidao.baidu.com/question/1446465410952140860.html'
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "gbk"

    soup = BeautifulSoup(r.text)
    print soup.pre


if __name__ == '__main__':
    # htmlstr = open('tem.txt').read()
    # print htmlstr
    # print process_baidu(htmlstr)
    process_test()
