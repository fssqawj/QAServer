# coding: utf-8
import sys
import re
import os
import copy
from tqdm import *
import nltk
import cPickle as pickle
from nltk.corpus import stopwords
import math
from nltk.stem.lancaster import LancasterStemmer
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

avglen = 0
K1 = 1.0
b = 0.75
N = 101712


def remove_punctuation(text):
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    line = re.sub(r, ' ', text)
    return line


def remove_punctuation_re(text):
    # return re.sub(ur"\p{P}+", "", text)
    return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), text)


def getFileList(dir):
    fileList = []
    # for i in range(100000):
    #     fileList.append("report" + str(i) + ".xml")
    # return fileList
    files = os.listdir(dir)
    for f in files:
        if os.path.isfile(dir + '/' + f):
            fileList.append(f)
    return fileList


def wash(fileList):
    # denyPos = ['CC', 'CD', 'DT', 'TO', '']
    st = LancasterStemmer()
    for f in tqdm(fileList):
        fr = open('./washFile/' + f, 'r')
        fw = open("./washFile_stem/" + f, 'w')
        for line in fr.read().splitlines():
            line = remove_punctuation(line).lower()
            # wordpos = pos(remove_punctuation(line).lower())
            # for turple in wordpos:
            #     if (turple[0] not in stopwords.words('english')):
            #         fw.write(turple[0] + ' ')
            # fw.write(x + ' ' for x in line.split() if x not in stopwords.words('english'))
            # stopw = stopwords.words('english')
            words = [x for x in line.split()]
            for x in words:
                try:
                    fw.write(st.stem(x) + ' ')
                except:
                    print x

        fr.close()
        fw.close()


def pos(text):
    tokens = nltk.word_tokenize(text)
    wordpos = nltk.pos_tag(tokens)
    return wordpos


def init(titles, flag):
    wordindoc = {}  # f_ij
    wordindata = {}  # ni
    doclen = {}  # doclen
    sumlen = 0
    if flag:
        wordindoc = pickle.load(open('wordindoc_stem.pkl', 'r'))
        wordindata = pickle.load(open('wordindata_stem.pkl', 'r'))
        doclen = pickle.load(open('doclen_stem.pkl', 'r'))
        sumlen = pickle.load(open('sumlen_stem.pkl', 'r'))
    else:
        for idx, line in enumerate(titles):
            words = line.split()
            d = {k: words.count(k) for k in set(words)}
            doclen[line] = len(words)
            sumlen += len(words)
            for k in set(words):
                wordindata[k] = wordindata.get(k, 0) + d[k]
            for word in set(words):
                if(wordindoc.get(word) == None):
                    wordindoc[word] = {}
                wordindoc.get(word)[line] = d[word]

        pickle.dump(wordindoc, open('wordindoc_stem.pkl', 'w'))
        pickle.dump(wordindata, open('wordindata_stem.pkl', 'w'))
        pickle.dump(doclen, open('doclen_stem.pkl', 'w'))
        pickle.dump(sumlen, open('sumlen_stem.pkl', 'w'))
    return wordindoc, wordindata, doclen, sumlen


def process(query):
    st = LancasterStemmer()
    query = remove_punctuation(query).lower()
    stopw = stopwords.words('english')
    return [st.stem(x) for x in query.split() if x not in stopw]


def process_zh(query):
    return query.split()


def score(query, doc, wordindoc, wordindata, doclen):
    res = 0
    for word in query:
        fij = wordindoc.get(word, {}).get(doc, 0)
        # print doc
        # print avglen
        # print fij
        # print doclen.get(doc)
        res += (K1 + 1) * fij / (K1 * ((1 - b) + b * doclen.get(doc) / avglen) + fij) * math.log((N + 0.5) / (wordindata.get(word, 0) + 0.5))
    return res


def search(query, fileList, wordindoc, wordindata, doclen):
    query = process_zh(query)
    print query
    res = {}
    # for word in query:
    res = {(original_title, answer, iscore): score(query, title, wordindoc, wordindata, doclen) for title, original_title, answer, iscore in fileList}
    res = sorted(res.iteritems(), key=lambda d: d[1], reverse=True)
    return res


def p10(myList, resList):
    hit = 0
    AP = 0
    # print myList[:10]
    # print resList[:10]
    for i in range(1000):
        if(resList.count(myList[i][0][:-4]) > 0):
            hit = hit + 1
            AP = AP + 1.0 * hit / (i + 1)
    return 1.0 * hit / 1000, AP / 1000


def getRes(resfile):
    fr = open(resfile, 'r')
    res = {}
    for line in fr.read().splitlines():
        line = line.split()
        if(line[3] != '0'):
            if(line[0] not in res.keys()):
                res[line[0]] = []
            res[line[0]].append(line[5])
    return res


def bm25(p, titles, answers, scores):
    original_titles = copy.deepcopy(titles)
    titles = [remove_punctuation_re(title) for title in titles]
    answers = [remove_punctuation_re(answer) for answer in answers]
    p = remove_punctuation_re(p)
    titles = [' '.join(jieba.cut(title)) for title in titles]
    p = ' '.join(jieba.cut(p))
    wordindoc, wordindata, doclen, sumlen = init(titles, False)
    global avglen
    avglen = 1.0 * sumlen / N
    res = search(p, zip(titles, original_titles, answers, scores), wordindoc, wordindata, doclen)
    titles, answers, scores = [], [], []
    for key, _ in res:
        titles.append(key[0])
        answers.append(key[1])
        scores.append(key[2])
    return titles, answers, scores


if __name__ == "__main__":
    # print remove_punctuation('sdfsdfsdfd..df.<>dfdf..')
    # print getFileList("./trec_data1_renameCheckSum")
    # wash(getFileList("./washFile"))
    # fr = open('./washFile/report9.xml', 'r')
    # fw = open("./out.txt", 'w')

    # for line in fr.read().splitlines():
    #     fw.write(pos(line) + '\n')
    wordindoc, wordindata, doclen, sumlen = init(getFileList("./washFile_stem"), True)
    # print doclen
    avglen = 1.0 * sumlen / N
    # print str(avglen) + "\n"
    res = getRes('11qrels_visit_checksum.txt')
    # print res
    p = 0
    ap = 0
    psum = 0
    apsum = 0
    fr = open('0601_2011.txt', 'r')
    for query in tqdm(fr.readlines()):
        query = query.split()
        print query[0] + " solving... ...\n"
        myres = search(' '.join(query[1:]), getFileList("./washFile_stem"), wordindoc, wordindata, doclen)
        p, ap = p10(myres, res.get(query[0], []))
        psum += p
        apsum += ap
        print query[0] + " done!\n"
    print "P@10 : " + str(psum / 35) + '\n'
    print "MAP : " + str(apsum / 35) + '\n'
    # fw = open('BM25.index', 'w')
    # print >>fw, wordindoc
    # fw.close()
