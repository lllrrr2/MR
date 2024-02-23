'''
new Env('取关商品'); 
cron: 6 6 6 6 6 python3 jd_unfollow.py
export RabbitToken="token值"
'''
import asyncio
import json

from utils.common import UserClass, TaskClass, get_error_msg, wait, print_trace


class UnFollowClass(UserClass):

    def __init__(self, cookie):
        super(UnFollowClass, self).__init__(cookie)
        self.H5ST_VERSION = "4_2"
        self.ua = self.ep_UA

    def searchParams(self, searchParams):
        _searchParams = {
            "client": "apple",
            "clientVersion": "11.4.0",
            "appid": "jd-cphdeveloper-m",
        }
        _searchParams.update(searchParams)
        return _searchParams

    def opt(self, opt):
        _opt = {
            "method": "get",
            "api": "api",
        }
        _opt.update(opt)
        return _opt

    async def favoriteList(self):
        body = {
            "origin": "2",
            "coordinate": "",
            "pagesize": "100",
            "page": "1",
            "sortType": "time_desc",
        }
        opt = {
            "method": "post",
            "functionId": "favoriteList",
            "body": body,
            "sign": True
        }
        status_code, result = await self.jd_api(opt)
        code = result.get('code', status_code)
        if code == "0":
            sku_list = [x['wareId'] for x in result.get('favoriteList', [])]
            if sku_list:
                if await self.batchCancelFavorite(sku_list):
                    await self.favoriteList()
            else:
                self.printf('商品收藏列表空的')
        else:
            msg = get_error_msg(result)
            self.printf(f'查询商品收藏列表失败[{code}]: {msg}')
            # if not opt.get('retry'):
            #     await wait(1)
            #     opt['retry'] = True
            #     await self.favoriteList(opt)

    async def queryFollowProduct(self):
        body = {
            "cp":1,
            "pageSize":30,
            "category":"",
            "promote":0,
            "cutPrice":0,
            "coupon":0,
            "stock":0,
            "area":"1_72_2819_0",
            "tenantCode":"jgm",
            "bizModelCode":"6",
            "bizModeClientType":"M",
            "externalLoginType":"1"
        }
        opt = {
            "functionId": "queryFollowProduct",
            "body": body,
            "appId": "c420a",
            "searchParams": self.searchParams({
                "functionId": "queryFollowProduct",
                "body": json.dumps(body, separators=(",", ":"))
            }),
            "h5st": True
        }
        self.temporary_referer = "https://wqs.jd.com/"
        status_code, result = await self.jd_api(self.opt(opt))
        code = result.get('code', status_code)
        if code == "0":
            sku_list = [x['commId'] for x in result.get('followProductList', [])]
            if sku_list:
                if await self.batchCancelFavorite(sku_list):
                    await self.queryFollowProduct()
            else:
                self.printf('商品收藏列表空的')
        else:
            msg = get_error_msg(result)
            self.printf(f'查询商品收藏列表失败[{code}]: {msg}')

    async def batchCancelFavorite(self, sku_list):
        ret = False
        try:
            body = {
                "skus": ",".join(sku_list),
            }
            opt = {
                "method": "post",
                "functionId": "batchCancelFavorite",
                "body": body,
                "sign": True
            }
            status_code, result = await self.jd_api(opt)
            code = result.get('code', status_code)
            if code == '0':
                ret = True
                self.printf(f'成功取消关注{len(sku_list)}件商品')
            else:
                msg = get_error_msg(result)
                self.printf(f'取消关注商品失败[{code}]: {msg}')
        except:
            print_trace()
        return ret

    async def main(self):
        await self.queryFollowProduct()


if __name__ == '__main__':
    task = TaskClass("task")
    task.name = 'UnFollow'
    task.init_config(UnFollowClass)
    asyncio.run(task.main("取关商品"))
