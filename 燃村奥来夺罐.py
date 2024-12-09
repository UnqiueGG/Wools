"""
燃村奥来夺罐小程序
变量名： rqack
抓 https://jdbapi.socialark.net/api/user/getUserInfo 请求头中 FrontAuthorization
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
def random_delay():
    # 生成一个1到5秒之间的随机浮点数
    delay = random.uniform(1, 10)
    time.sleep(delay)  # 暂停执行指定的秒数
enable_notification = 1  # 0不发送通知   1发送通知

# 只有在需要发送通知时才尝试导入notify模块
if enable_notification == 1:
    try:
        from notify import send
    except ModuleNotFoundError:
        print("警告：未找到notify.py模块。它不是一个依赖项，请勿错误安装。程序将退出。")
        sys.exit(1)

# ---------简化的框架 0.7 带通知--------

jbxmmz = "燃村奥来夺罐小程序"
jbxmbb = "1.0"


# 获取北京日期的函数
def get_beijing_date():
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time.date()


def dq_time():
    # 获取当前时间戳
    dqsj = int(time.time())

    # 将时间戳转换为可读的时间格式
    dysj = datetime.fromtimestamp(dqsj).strftime('%Y-%m-%d %H:%M:%S')
    # print("当前时间戳:", dqsj)
    # print("转换后的时间:", dysj)
    return dqsj


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
        'Host': 'jdbapi.socialark.net',
        'Connection': 'keep-alive',
        'Content-Length': '8',  # 这里应该是请求体的长度，您需要根据实际情况来设置
        'FrontAuthorization': token,
        'xweb_xhr': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11275',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wxf16145cad2c70171/12/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    return headers


# -------------------------------封装请求---完成----------


def game(token):
    url = "https://jdbapi.socialark.net/api/game/redRainOk"
    headers = create_headers(token)
    data = {
        "id": 3
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 确保请求成功
        #print(response.text)
        data = response.json()
        if data['code'] != 200:
            print(f"游戏：{data['msg']}")
        elif data['code'] == 200:
            print("游戏：+20 积分")
            random_delay()
            game(token)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def getInfo(token):
    url = "https://jdbapi.socialark.net/api/user/getUserInfo"
    headers = create_headers(token)
    data = {}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 确保请求成功

        data = response.json()
        if data['code'] != 200:
            print(f"查询失败：{data['msg']}")
        elif data['code'] == 200:
            print(f"可用积分：{data['data']['leftScore']}")
            random_delay()
            return data['data']['leftScore']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def choujiang(token):
    url = "https://jdbapi.socialark.net/api/game/startNineScore"
    headers = create_headers(token)
    data = {}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 确保请求成功

        data = response.json()
        if data['code'] != 200:
            print(f"抽奖：{data['msg']}")
        elif data['code'] == 200:
            print(f"抽奖：{data['data']['prizeName']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def getJiangPaiInfo(token):
    url = "https://jdbapi.socialark.net/api/user/getUserInfo"
    headers = create_headers(token)
    data = {}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 确保请求成功

        data = response.json()
        if data['code'] != 200:
            print(f"查询失败：{data['msg']}")
        elif data['code'] == 200:
            numMedal1 = data['data']['numMedal1']
            numMedal2 = data['data']['numMedal2']
            numMedal3 = data['data']['numMedal3']
            numMedal4 = data['data']['numMedal4']
            numMedal5 = data['data']['numMedal5']
            numMedal6 = data['data']['numMedal6']
            print(f"奖牌数量：numMedal1 {numMedal1}枚")
            print(f"奖牌数量：numMedal2 {numMedal2}枚")
            print(f"奖牌数量：numMedal3 {numMedal3}枚")
            print(f"奖牌数量：numMedal4 {numMedal4}枚")
            print(f"奖牌数量：numMedal5 {numMedal5}枚")
            print(f"奖牌数量：numMedal6 {numMedal6}枚")
            if numMedal1!=0 and numMedal2!=0 and numMedal3!=0 and numMedal4!=0 and numMedal5!=0 and numMedal6!=0:
                random_delay()
                hecheng(token)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP错误：{http_err}")
    except Exception as err:
        print(f"请求异常：{err}")

def hecheng(token):
    pass



# 本地测试用
os.environ['rqack'] = '''
eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl9mcm9udF91c2VyX2tleSI6IjM1ODQ0NTdmLTRmNTEtNGZiZC1hZjkyLTNmZGEwNTdiMGMwZCJ9.aoaDj5f20f30HXvTUA61lpynI62t3WHCNYeRFDvN42Y8Z4lCjtrt2H0QXPfnb7_htrSta9Gu0BfwlCToy33NJQ#Unique
eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl9mcm9udF91c2VyX2tleSI6ImUwYmI3NGQzLWIzYTQtNDFkOC05NGUzLWQxMzY2ODg4ZjdkOSJ9.DKYo51RzZ5CIEFFy6j5483_-1whSxyeGynOqA34c2VeytuA132mCUEvotfQYE25GQvAd-tnAIzsuezdrsz50uw#高高
eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl9mcm9udF91c2VyX2tleSI6IjhiYTQxMzdjLTRkN2MtNGVkNS04NGE2LTBkMWJkZWFmNDdkNyJ9.XPrtT5rrsofudRRUhgJRJigKYJ_3pqTA6j4NqnvAGWb0ffiHVF4Tz1p35RRiAvKXjTrAhp3y18CJSVtYn1miaA#小手机
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
    var_name = 'rqack'  #
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
        game(token)  # 为每个用户执行签到操作，确保sign_in函数接受cookie参数
        jifen = getInfo(token)
        if jifen > 50:
            count = jifen//50
            for i in range(count):
                random_delay()
                choujiang(token)
        else:
            print("抽奖：积分不足")
        getJiangPaiInfo(token)




    sys.stdout = original_stdout
    output_content = captured_output.getvalue()
    captured_output.close()

    # 封装后的发送通知逻辑
    #send_notification(enable_notification, output_content)   #注释掉了  不让发送了


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f'代码执行完毕，共执行了{round(end - start, 5)}s')