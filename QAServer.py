# coding: utf8
import tornado.ioloop
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.gen
import asyncio
from threading import Thread
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from htmlprocessor import process_community_site
from tornado.options import define, options
from parser.htmlfetch import start_crawler_worker


define("port", default=18887, help="run on the given port", type=int)

crawler_worker_loop = asyncio.new_event_loop()
Thread(target=start_crawler_worker, args=(crawler_worker_loop,)).start()


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
        search_results = process_community_site(crawler_worker_loop, p)
        self.set_header("Access-Control-Allow-Origin", "*")
        resp = ""
        for item in search_results:
            resp += item.question + "</br>" + item.best_answer + "</br>" + item.source + "</br>"
        return resp


def server_init():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/proxy", SolverHandler),
        ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


def start_crawler_worker(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == '__main__':
    server_init()
