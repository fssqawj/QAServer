# coding: utf-8
import copy
import json
from warnings import warn
from bs4.element import Tag


class CqaMeta:
    def __init__(self, url):
        self._question = None
        self._description = None
        self._best_answer = None
        self._best_vote_up = 0
        self._best_vote_down = 0
        self._candidates = []
        self._update_time = None
        self._source = None
        self._url = url

    def set_question(self, question):
        if question is None:
            warn(self._url + ' has no question!')
        elif isinstance(question, str):
            self._question = question
        elif isinstance(question, Tag):
            self._question = question.text
        else:
            raise NotImplementedError
        return self

    def set_description(self, description):
        if description is None:
            warn(self._url + ' has no description!')
        elif isinstance(description, str):
            self._description = description
        elif isinstance(description, Tag):
            self._description = description.text
        else:
            raise NotImplementedError
        return self

    def set_best_answer(self, best_answer):
        if best_answer is None:
            warn(self._url + ' has no best answer!')
        elif isinstance(best_answer, str):
            self._best_answer = best_answer
        elif isinstance(best_answer, Tag):
            self._best_answer = best_answer.text
        else:
            raise NotImplementedError
        return self

    def set_best_vote_up(self, best_vote_up):
        if best_vote_up is None:
            warn(self._url + ' has no best vote up!')
        elif isinstance(best_vote_up, int):
            self._best_vote_up = best_vote_up
        elif isinstance(best_vote_up, Tag):
            self._best_vote_up = int(best_vote_up.text)
        else:
            raise NotImplementedError
        return self

    def set_best_vote_down(self, best_vote_down):
        if best_vote_down is None:
            warn(self._url + ' has no best vote down!')
        elif isinstance(best_vote_down, int):
            self._best_vote_down = best_vote_down
        elif isinstance(best_vote_down, Tag):
            self._best_vote_down = int(best_vote_down.text)
        else:
            raise NotImplementedError
        return self

    def set_candidates(self, candidates):
        self._candidates = copy.deepcopy(candidates)
        return self

    def set_update_time(self, update_time):
        if update_time is None:
            warn(self._url + ' has no update time!')
        elif isinstance(update_time, str):
            self._update_time = update_time
        elif isinstance(update_time, Tag):
            self._update_time = update_time.text
        else:
            raise NotImplementedError
        return self

    def set_source(self, source):
        self._source = source
        return self

    def set_url(self, url):
        self._url = url
        return self

    @property
    def question(self):
        return self._question

    @property
    def description(self):
        return self._description

    @property
    def best_answer(self):
        return self._best_answer

    @property
    def best_vote_up(self):
        return self._best_vote_up

    @property
    def best_vote_down(self):
        return self._best_vote_down

    @property
    def candidates(self):
        return self._candidates

    @property
    def update_time(self):
        return self._update_time

    @property
    def source(self):
        return self._source

    @property
    def url(self):
        return self._url

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)

