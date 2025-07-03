import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import urllib.parse
import hashlib
import json
import requests
import base64,uvicorn
import urllib.parse
from fastapi import FastAPI


app = FastAPI()

print('听梦用少羽爹妈双亡换的10U超级无敌二要素缓慢解密老奶奶口 💥\n')
def eys(name,card:str):
    start_time = int(time.time() * 1000)
    def encode(name, card):
        global temp_key, temp_iv
        e = {"apiCode": "CustomerEIDPhoto", "head": '{"AppCode":"WjrcbWdXcx","WaterMark":' + str(start_time) + '}'}
        data = {
            "idNo": f"{card}",
            "custName": f"{name}",
            "address": "江苏省苏州市吴江区中山南路1777号",
            "latitude": "31.14277052670606",
            "longitude": "120.64269731792356"
        }
        # 生成 MD5 哈希
        md5_hash = hashlib.md5((e["apiCode"] + e["head"]).encode()).hexdigest()
        print('MD5 Hash:', md5_hash)
        temp_iv = md5_hash[:16].encode()
        temp_key = md5_hash[16:].encode()

        json_data = json.dumps(data)

        def encrypt_data(t):
            if t and t != "{}":
                cipher = AES.new(temp_key, AES.MODE_CBC, temp_iv)
                encrypted_data = cipher.encrypt(pad(t.encode(), AES.block_size))
                return base64.b64encode(encrypted_data).decode()  # 返回 base64 编码的密文
            return ""

        encrypted_data = encrypt_data(json_data)
        return encrypted_data
    def decode(str):
        def decrypt_data(encrypted_data):
            global temp_key, temp_iv
            encrypted_data_bytes = base64.b64decode(encrypted_data)  # 使用 base64 解码
            cipher = AES.new(temp_key, AES.MODE_CBC, temp_iv)
            decrypted_data = unpad(cipher.decrypt(encrypted_data_bytes), AES.block_size)
            return decrypted_data.decode()

        decrypted_data = decrypt_data(str)
        return decrypted_data
    key = encode(name,card)
    headers = {
        'content-length': '349',
        'accept': '*/*',
        'xweb_xhr': '1',
        'dsn': '1751507951714',
        'authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJXSlJDQl9VXzE3NTE1MDc5ODI3NTAxNjMiLCJpc3MiOiJXVUpJQU5HIFJVUkFMIENPTU1FUkNJQUwgQkFOSyIsImV4cCI6MTc1MTU0MDM4MywiaWF0IjoxNzUxNTA3OTgzLCJqdGkiOiIyMDc0ODAifQ.ZSZ6q233AD2YDhGO904VArAPkqTYhTPqlzd5qygtPiOpWRX3b-VZRz7EotTh61IIVKA6xlRiMxLN2OrkuqW7B14wzVYOcl9q72UJOGYlvMCGPI8ZsAMdBmpCYweupS6I17ccFkXuTJqIEik2ggKK18mw3tmJRd8Rw62lO56sw3c',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309092b) XWEB/8555',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8;',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://servicewechat.com/wx45f18ba09a9f9169/209/page-frame.html',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'JSESSIONID=B556FDEF332873CD28FB16ADAE86D40D;Path=/web'}
    # 构建 head 字符串
    head = '{"AppCode":"WjrcbWdXcx","WaterMark":' + str(start_time) + '}'
    encoded_head = urllib.parse.quote(head)
    encoded_body = urllib.parse.quote(key)
    payload = 'head=' + encoded_head + '&body=' + encoded_body
    try:
        response0 = requests.post("https://jzr.szrcb.com/applet/CustomerEIDPhoto.do",headers=headers, data=payload)
        if response0.text != None:
            js = json.loads(decode(response0.text))
            print(js)
            if js['_RejCode']=='000000':
                return True
            else:
                return False
        else:
            print('二要素接口|返回为空')
            return False
    except Exception as e:
        print(f'二要素错误|{e}')


# name = '冯德兵'
# card = '513021199001175853'
# if eys(name,card):
#     print(f"{name}-{card} 二要素验证成功✅")
# else:
#     print(f"{name}-{card} 二要素验证失败❌")

@app.get('/eys')
def main(name:str,card:str):
    if eys(name, card):
        return {'data':f"{name}-{card} 二要素验证成功✅"}
    else:
        return {'data':f"{name}-{card} 二要素验证失败❌"}

if __name__ == '__main__':
    uvicorn.run(app='苏州银行二要素:app', host='0.0.0.0', port=38841)
