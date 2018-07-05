# coding: utf-8
import jieba
from utils import *


def remove_punctuation(text):
    return ''.join([' ' if is_punctuation_or_unreadable(x) else x for x in text]).strip().lower()


def similarity(text_x, text_y):
    if text_y is None:
        return 0
    word_token_x = list(jieba.cut(remove_punctuation(text_x)))
    word_token_y = list(jieba.cut(remove_punctuation(text_y)))
    return len([x for x in word_token_x if x in word_token_y]) / len(word_token_y + word_token_x)


def qq_similarity(question_x, question_y):
    return similarity(question_x, question_y)


def qa_similarity(question, answer):
    return similarity(question, answer)


if __name__ == "__main__":
    print(similarity('怎么办理个人所得税～', '个人所得税如何办理？'))
