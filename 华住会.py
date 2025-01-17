"""
华住会小程序
变量： Cookie
变量名： hzhck
抓 任意 Cookie

多账号   换行/回车
版本 1.0
------更新记录----
1.0 测试版


"""
import os
import requests
from datetime import datetime, timezone, timedelta
import json
import time
import io
import sys
import requests
import base64

import random  # 导入random模块以生成随机暂停时间

enable_notification = 1  # 0不发送通知   1发送通知

# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

# ---------简化的框架 0.7 带通知--------

jbxmmz = "华住会小程序"
jbxmbb = "1.0"


# 获取北京日期的函数
def get_beijing_date():
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()


def dq_time():
    # 获取当前时间戳
    dqsj = int(time.time())
    return dqsj
    # 将时间戳转换为可读的时间格式
    # dysj = datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
    # print("当前时间戳:", dqsj)
    # print("转换后的时间:", dysj)
    # if int(dysj[8])==int('0'):
    #     return dysj[9]
    # else:
    #     return dysj[8:10]
    # return dqsj, dysj


def log(message):
    print(message)


def print_disclaimer():
    log("📢 请认真阅读以下声明")
    log("      【免责声明】         ")
    log("✨ 脚本及其中涉及的任何解密分析程序，仅用于测试和学习研究")
    log("✨ 禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断")
    log("✨ 禁止任何公众号、自媒体进行任何形式的转载、发布")
    log("✨ 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害")
    log("✨ 脚本文件请在下载试用后24小时内自行删除")
    log("✨ 脚本文件如有不慎被破解或修改由破解或修改者承担")
    log("✨ 如不接受此条款请立即删除脚本文件")
    log("" * 10)
    log("" * 10)
    log("" * 10)
    log(f'-----------{jbxmmz} {jbxmbb}-----------')


# 获取环境变量
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f'环境变量{var_name}未设置，请检查。')
        return None
    accounts = value.strip().split('\n')
    num_accounts = len(accounts)
    print(f'-----------本次账号运行数量：{num_accounts}-----------')

    print_disclaimer()
    return accounts


# -------------------------------封装请求-------------


def create_headers(token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11581',
        'Accept': 'application/json, text/plain, */*',
        'Client-Platform': 'WX-MP',
        'Origin': 'https://cdn.huazhu.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cdn.huazhu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': token
    }
    return headers


# -------------------------------封装请求---完成----------


def sign_in1(token):
    url = f"https://appgw.huazhu.com/game/sign_in?date={dq_time()}"
    headers = create_headers(token)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 确保请求成功

        data = response.json()
        if data['code'] != 200:
            print(f"签到错误---> {data['message']}")
        elif data['code'] == 200:
            print(f"签到成功--->获得积分【{data['content']['point']}】")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")


# 本地测试用
os.environ['hzhck'] = '''
userToken=da267669c432427e8a877fc41792461f076684440; __tea_cache_tokens_10000004={%22web_id%22:%227452912016940884238%22%2C%22user_unique_id%22:%22076684440%22%2C%22timestamp%22:1735266302293%2C%22_type_%22:%22default%22}; ec=GB5MDifp-1735266303393-20f8d2bfb48581847382632; _efmdata=luJ8yfep%2BoAwiYHBkqXP5JU%2BoxdA6cKf8K3nHSyT4WU2zGRQtEYfWfGZcRGXm%2FyHaX4ei8M%2BJsZM3lnoT%2F%2Bjdg%2FFj7vgu8tk3bneeGNq7wM%3D; _exid=qpn%2FbQe3oRMn8rcx2IEApu0g6CPveECGSeAd5qdDAxLE29xwzO%2BbFoSlNXGzZlA8d8a%2BqNW1XYdEDUXj64%2B%2Bjw%3D%3D
'''


class Tee:
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for file in self.files:
            file.write(obj)
            file.flush()

    def flush(self):
        for file in self.files:
            file.flush()


def send_notification(enable, content):
    if enable:
        try:
            print("\n")
            print("通知已发送。输出内容为：")
            send(f"{jbxmmz}  {jbxmbb}版", content)  # 尝试发送通知
            # print(content)
        except NameError:
            print("通知发送失败，send函数未定义。")


def main():
    var_name = 'hzhck'  #
    tokens = get_env_variable(var_name)
    if not tokens:
        print(f'环境变量{var_name}未设置，请检查。')
        return

    captured_output = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = Tee(sys.stdout, captured_output)

    total_accounts = len(tokens)

    for i, token in enumerate(tokens):
        parts = token.split('#')
        if len(parts) < 1:
            print("令牌格式不正确。跳过处理。")
            continue

        token = parts[0]
        # unionid = parts[1]
        account_no = parts[1] if len(parts) > 1 else ""  # 备注信息
        account_info = f" {account_no}" if account_no else ""  # 如果有备注信息，则附加到账号信息中
        print(f'------账号 {i + 1}/{total_accounts} {account_info} -------')

        sign_in1(token)  # 为每个用户执行签到操作，确保sign_in函数接受cookie参数

    sys.stdout = original_stdout
    output_content = captured_output.getvalue()
    captured_output.close()

    # 封装后的发送通知逻辑
    send_notification(enable_notification, output_content)   #注释掉了  不让发送了


if __name__ == "__main__":
    main()