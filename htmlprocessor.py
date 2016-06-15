# coding: utf8
from bs4 import BeautifulSoup


def process(htmlstr):
    soup = BeautifulSoup(htmlstr)
    titles = soup.select('dt')
    answers = soup.select("dd.dd.answer")
    return [x.get_text() for x in titles], [x.get_text() for x in answers]


if __name__ == '__main__':
    htmlstr = open('tem.txt').read()
    print htmlstr
    print process(htmlstr)
