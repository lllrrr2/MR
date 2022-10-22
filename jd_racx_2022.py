'''
new Env('热爱穿行-2022');
变量: RabbitToken
export RabbitToken="token值"

log剩余次数大于6500方可使用
'''


import os
BING_FA_STATUS = False
if os.environ.get("CXJ_THREADS_NUM"):
    BING_FA_STATUS = True
    try:
        from gevent import monkey
        monkey.patch_all()
    except:
        import os
        os.system("apk add g++ python3-dev libc-dev gcc libev-dev")
        os.system("pip3 install --upgrade pip")
        os.system("pip3 install --upgrade pip")
        os.system("pip3 install gevent")
    try:
        from gevent import monkey
        monkey.patch_all()
    except:
        BING_FA_STATUS = False
try:
    import requests
    import Crypto
except ImportError:
    import shutil
    import os

    print("缺依赖，尝试进行修复，也可手动修复： pip3 install requests pycryptodome")
    os.system('pip3 install pycryptodome requests')

from MR_util.racx_task_2022 import main


if __name__ == '__main__':
    main(BING_FA_STATUS)
