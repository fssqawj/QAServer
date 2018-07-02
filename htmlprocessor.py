# coding: utf-8
import requests
from bs4 import BeautifulSoup


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}

max_fetch_cnt = 3


def process_baidu(content, titles, answers, scores):
    soup = BeautifulSoup(content, 'lxml')
    titles_bd = soup.select('dt')
    answers_bd = soup.select("dd.dd.answer")
    for idx, title in enumerate(titles_bd):
        if idx >= len(answers_bd) or idx >= max_fetch_cnt:
            break
        titles.append(title.get_text())
        answers.append(answers_bd[idx].get_text())
        scores.append('Baidu')


def process_sina(content, titles, answers, scores):
    soup = BeautifulSoup(content)
    search_list = soup.select('div.search_item')
    for item in search_list[1:min(max_fetch_cnt, len(search_list))]:
        titles.append(item.h2.text)
        answ = item.div.text
        answers.append(answ[answ.find('答：'):answ.find('详细>')])
        scores.append('Sina')


def process_360(content, titles, answers, scores):
    soup = BeautifulSoup(content.decode('utf-8'))
    titles_360 = soup.select('div.qa-i-hd')
    answers_360 = soup.select('div.qa-i-bd')
    titles += [x.get_text() for x in titles_360][:min(max_fetch_cnt, len(titles_360))]
    answers += [x.get_text() for x in answers_360][:min(max_fetch_cnt, len(titles_360))]
    scores += ['360' for _ in titles_360][:min(max_fetch_cnt, len(titles_360))]


def process_sougou(content, titles, answers, scores):
    soup = BeautifulSoup(content)
    titles_sougou = soup.select('h3.vrTitle')
    answers_sougou = soup.select('div.str-text-info')
    titles += [x.get_text().replace('- 搜狗问问', '').replace('_搜狗问问', '').strip() for x in titles_sougou][:min(max_fetch_cnt, len(titles_sougou))]
    answers += [x.get_text().replace('最佳答案', '').strip() for x in answers_sougou][:min(max_fetch_cnt, len(titles_sougou))]
    scores += ['Sougou' for _ in titles_sougou][:min(max_fetch_cnt, len(titles_sougou))]


def process_zhihu(content, titles, answers, scores):
    soup = BeautifulSoup(content)
    titles_zhihu = soup.select('h2.ContentItem-title')
    answers_zhihu = soup.select('div.RichContent.Highlight.is-collapsed')
    titles += [x.get_text() for x in titles_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]
    answers += [x.get_text() for x in answers_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]
    scores += ['Zhihu' for _ in titles_zhihu][:min(max_fetch_cnt, len(titles_zhihu))]


def process_test():
    url = 'http://zhidao.baidu.com/question/1446465410952140860.html'
    r = requests.get(url, headers=header, timeout=12999, verify=False)
    r.encoding = "gbk"

    soup = BeautifulSoup(r.text)
    print(soup.pre)


if __name__ == '__main__':
    process_test()
