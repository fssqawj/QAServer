# QAServer
相似问句检索在自动问答系统中有着重要的作用，他首先用来生成候选答案集，然后通过重新排序的方法来返回答案。
因此数据源的质量直接决定问答系统的性能。在本地没有充分数据集的情况下，要构建通用/领域问答系统是非常困难的，本项目利用广泛的社区问答资源，
为问答系统构建的候选集生成提供可用的工具。

## 使用方法

`python QAserver.py`

`http://localhost:18887/proxy?p=any_question`


返回格式:
```
{
    "_best_answer": "不能，我不是智能机器，世界上没人能…",
    "_best_vote_down": 0,
    "_best_vote_up": 0,
    "_candidates": [ ],
    "_description": null,
    "_question": "你能回答任何问题吗？",
    "_source": "Sougou",
    "_update_time": null,
    "_url": "http://www.sogou.com/sogou?query=你的任何问题&insite=wenwen.sogou.com&page=0"
}
... ...
```
## 爬取的CQA网站
* Baidu `BaiduProcessor`
* 360 `SoProcessor`
* Zhihu `ZhihuProcessor`
* Sougou `SougouProcessor`

## Connect
fssqawj fssqawj[AT]gmail[DOT]com
