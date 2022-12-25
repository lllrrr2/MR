'''
new Env('炸年兽-2022');
变量: RabbitToken
export RabbitToken="token值"
export ZNS_THREADS_NUMS=1
export ZNS_PINS="pin1,pin2,pin3"
export ZNS_NUM="0"
export ZNS_RAISE="1"


ZNS_THREADS_NUMS: 并发数
ZNS_PIN: 需要跑的ck的pin值
ZNS_NUM: 需要的前多少个号为车头
ZNS_RAISE: 是否自动升级，1：为自动升级，0为不自动升级

log剩余次数大于5000方可使用
'''

import os

if not os.environ.get("LogHost"):
    print("请先填写LogHost变量\nexport LogHost='xxxxx'")
    # exit()

try:
    ZNS_THREADS_NUM = int(os.environ.get("ZNS_THREADS_NUMS", 1))
except:
    ZNS_THREADS_NUM = 1
if ZNS_THREADS_NUM > 1:
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
        print("缺少依赖，无法并发")
try:
    import requests
    import Crypto
except ImportError:
    import shutil
    import os

    print("缺依赖，尝试进行修复，也可手动修复： pip3 install requests pycryptodome")
    os.system('pip3 install pycryptodome requests')

from MR_util.zns_task_2022 import main

if __name__ == '__main__':
    main()
