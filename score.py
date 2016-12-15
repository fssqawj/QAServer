# coding: utf-8
from BM25 import bm25


def candidate_sort(p, titles, answers, scores):
    return bm25(p, titles, answers, scores)


if __name__ == '__main__':
    pass
