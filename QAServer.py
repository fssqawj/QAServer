# coding: utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from htmlprocessor import *
from tornado.options import define, options
from score import *
from htmlfetch import *


define("port", default=18887, help="run on the given port", type=int)

urls = ['http://zhidao.baidu.com/search?word={}',
        'http://www.sogou.com/sogou?query={}&insite=wenwen.sogou.com',
        'http://iask.sina.com.cn/search?searchWord={}&record=1',
        'http://wenda.so.com/search/?q={}',
        'https://www.zhihu.com/search?q={}']

encodings = ['gbk', 'utf-8', 'utf-8', 'utf-8', 'utf-8']


class SolverHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(100)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        p = self.get_argument('p')
        html = yield self.get_html(p)
        self.write(html)
        self.finish()

    @run_on_executor
    def get_html(self, p):
        resources = fetch_pages([x.format(p) for x in urls])
        titles, answers, scores = [], [], []
        process_baidu(resources[0], titles, answers, scores)
        # process_sina(resources[0], titles, answers, scores)
        process_360(resources[3], titles, answers, scores)
        process_sougou(resources[1], titles, answers, scores)
        process_zhihu(resources[4], titles, answers, scores)
        print(titles, answers, scores)
        res = candidate_sort(p, titles, answers, scores)
        self.set_header("Access-Control-Allow-Origin", "*")
        resp = ""
        for item in res:
            title, answer, score = item
            resp += title + "</br>" + answer + "</br>" + score + "</br>"
        return resp


def server_init():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/proxy", SolverHandler),
        ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    server_init()
