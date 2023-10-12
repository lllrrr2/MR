'''
new Env('京东商品评价');
cron: 6 6 6 6 6 python3 jd_comment_run.py
export RabbitToken="token值"
'''

import asyncio

from utils.comment import JDComment
from utils.common import TaskClass

if __name__ == '__main__':
    task = TaskClass("task")
    task.name = "comment"
    task.init_config(JDComment)
    asyncio.run(task.main("京东商品评价"))
