# coding: utf-8
from bs4 import BeautifulSoup
from htmlfetch import fetch_pages_in_loop
from score import candidate_sort


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}

max_fetch_cnt = 3

urls = ['http://zhidao.baidu.com/search?word={}',
        'http://www.sogou.com/sogou?query={}&insite=wenwen.sogou.com',
        'http://iask.sina.com.cn/search?searchWord={}&record=1',
        'http://wenda.so.com/search/?q={}',
        'https://www.zhihu.com/search?q={}']

encodings = ['gbk', 'utf-8', 'utf-8', 'utf-8', 'utf-8']


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
    soup = BeautifulSoup(content)
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


def process_community_site(crawler_worker_loop, query):
    resources = fetch_pages_in_loop(crawler_worker_loop, [x.format(query) for x in urls])
    # resources = fetch_pages(urls)
    titles, answers, scores = [], [], []
    process_baidu(resources[0], titles, answers, scores)
    # process_sina(resources[0], titles, answers, scores)
    process_360(resources[3], titles, answers, scores)
    process_sougou(resources[1], titles, answers, scores)
    process_zhihu(resources[4], titles, answers, scores)
    print(titles, answers, scores)
    return candidate_sort(query, titles, answers, scores)


if __name__ == '__main__':
    pass
