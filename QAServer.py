# coding: utf8

import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.gen
import requests
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from htmlprocessor import process
from tornado.options import define, options
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Referer': 'http://www.bing.com/',
}


define("port", default=18888, help="run on the given port", type=int)


class SolverHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(100)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        p = self.get_argument('p')
        html = yield self.gethtml(p)
        self.write(html)
        self.finish()

    @run_on_executor
    def gethtml(self, p):
        # url = 'http://baike.baidu.com/search/none?word={}&enc=utf8'.format(p)
        url = 'http://zhidao.baidu.com/search?word={}'.format(p)
        r = requests.get(url, headers=header, timeout=12999)
        r.encoding = "gbk"
        open('tem.txt', 'w').write(r.text)
        titles, answers = process(r.text)
        resp = ""
        for i in range(0, len(titles)):
            if i >= len(answers):
                break
            title, answer = titles[i], answers[i]
            resp += title + "</br>" + answer + "</br>"
        return resp
        # return answers[0]


def serverinit():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/proxy", SolverHandler),
        ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    serverinit()
