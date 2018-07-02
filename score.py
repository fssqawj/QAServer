# coding: utf-8
from similarity import *


def candidate_sort(p, titles, answers, scores):
    return sorted(zip(titles, answers, scores), key=lambda x: similarity(p, x[0]), reverse=True)


if __name__ == '__main__':
    pass
