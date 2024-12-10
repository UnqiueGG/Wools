'''
https://t.me/unique_gg
'''

import datetime
import json
import asyncio
import aiohttp
from aiohttp import ClientSession
from concurrent.futures import ThreadPoolExecutor
import time

# 活动id
activityId = 43

# InventoryId
consumptionInventoryId = 402888070

# 活动口令
keyWordAnswer = "冷链牛乳"

execution_times = 100  # 执行次数
max_workers = 5  # 最大线程数
request_interval = 300  # 请求间隔（单位：毫秒）
url = "https://h5api.gumingnc.com/newton-buyer/newton/buyer/ump/autumn/milk/activity/fcfs"
tokens = [
    {
        "token": {
            "token": "Bearer开头的",
            "ttoken": "xxxxxxxxx"
        },
        "remark": "备注1"
    },
    {
        "token": {
            "token": "xxxxx",
            "ttoken": "xxxxx"
        },
        "remark": "备注2"
    }
]


# 计算到11:59:59的倒计时
def get_time_until_115959():
    now = datetime.datetime.now()
    target_time = now.replace(hour=11, minute=59, second=59, microsecond=0)
    if now >= target_time:
        target_time += datetime.timedelta(days=1)
    time_diff = target_time - now
    return time_diff.total_seconds()


# 异步请求
async def rewardH5(session: ClientSession, token: dict, remark: str, times: int = 1, interval: int = 1):
    for i in range(times):
        curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        try:
            payload = {
                "channelCode": 20,
                "brandId": 1,
                "activityId": activityId,
                "keyWordAnswer": keyWordAnswer,
                "consumptionInventoryId": consumptionInventoryId
            }
            headers = {
                'User-Agent': "Mozilla/5.0 (Linux; Android 12; Redmi K30 Pro Zoom Edition Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.102 Mobile Safari/537.36 XWEB/1300073 MMWEBSDK/20240404 MMWEBID/9496 MicroMessenger/8.0.49.2600(0x28003133) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64 miniProgram/wx1736dcbd36f4c055",
                'Accept-Encoding': "gzip, deflate, br, zstd",
                'Content-Type': "application/json",
                'sec-ch-ua-platform': "Android",
                'Authorization': token["token"],
                'Cache-Control': "max-age=0",
                'sec-ch-ua': "Chromium;v=130, Android WebView;v=130, Not?A_Brand;v=99",
                'sec-ch-ua-mobile': "?1",
                't-token': token["ttoken"],
                'Origin': "https://h5.gumingnc.com",
                'X-Requested-With': "com.tencent.mm",
                'Sec-Fetch-Site': "same-site",
                'Sec-Fetch-Mode': "cors",
                'Sec-Fetch-Dest': "empty",
                'Referer': "https://h5.gumingnc.com/",
                'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }

            async with session.post(url, json=payload, headers=headers) as response:
                result = await response.json()
                print(f"账号{remark}，时间:{curTime}，结果:{result}")
        except Exception as e:
            print(f"账号{remark}，时间:{curTime}，错误:{e}")

        await asyncio.sleep(interval / 1000)


# 执行每个任务
async def task(session: ClientSession, token: dict, remark: str):
    await rewardH5(session, token, remark, execution_times, request_interval)


# 主函数
async def main():
    print(f"当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"共找到{len(tokens)}个账号")

    # 等待倒计时到达11:59:59
    time_to_wait = get_time_until_115959()
    print(f"距离11:59:59还有 {time_to_wait:.2f} 秒")

    await asyncio.sleep(time_to_wait)  # 等待直到11:59:59

    print("开始执行任务...")

    # 使用异步的HTTP会话
    async with aiohttp.ClientSession() as session:
        tasks = []
        for token in tokens:
            tasks.append(task(session, token['token'], token['remark']))

        # 限制最大并发数
        semaphore = asyncio.Semaphore(max_workers)

        # 执行所有任务
        async def limited_task(task_func):
            async with semaphore:
                await task_func

        await asyncio.gather(*(limited_task(t) for t in tasks))
    print("执行结束")


# 启动异步任务
if __name__ == '__main__':
    asyncio.run(main())
