import requests
import json
import urllib.parse

headers = {
           'Content-Type': 'application/json; charset=UTF-8',
           # 'Host':'192.168.1.1',
           # 'Connection':'keep-alive',
           # 'Content-Length':'54',
           # 'Accept':'application/json, text/javascript, */*; q=0.01',
           # 'Origin':'http://192.168.1.1',
           # 'X-Requested-With':'XMLHttpRequest',
           # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
           # 'Referer':'http://192.168.1.1/',
           # 'Accept-Encoding':'gzip, deflate',
           # 'Accept-Language':'zh-CN,zh;q=0.8',
           }
url = 'http://192.168.1.1/'

def check_pwd(type_in):
    """
    因为无线路由器要求设置的密码至少6位，少于6位直接判定密码错误
    """
    while len(type_in) < 6:
        type_in = input('密码错误！请重新输入：')
    return type_in

def encrypt_pwd(password):
    input1 = "RDpbLfCPsJZ7fiv"
    input3 = "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW"
    len1 = len(input1)
    len2 = len(password)
    dictionary = input3
    lenDict = len(dictionary)
    output = ''
    if len1 > len2:
        length = len1
    else:
        length = len2
    index = 0
    while index < length:
        # 十六进制数 0xBB 的十进制为 187
        cl = 187
        cr = 187
        if index >= len1:
            # ord() 函数返回字符的整数表示
            cr = ord(password[index])
        elif index >= len2:
            cl = ord(input1[index])
        else:
            cl = ord(input1[index])
            cr = ord(password[index])
        index += 1
        # chr() 函数返回整数对应的字符
        output = output + chr(ord(dictionary[cl ^ cr]) % lenDict)
    return output

def stok(url, encryptPwd):
    payload = '{"method":"do","login":{"password":"%s"}}' % encryptPwd
    response = requests.post(url, data=payload, headers=headers)
    while json.loads(response.text)['error_code'] != 0:
        password = check_pwd(input('密码错误！请重新输入：'))
        pwd = encrypt_pwd(password)
        payload2 = '{"method":"do","login":{"password":"%s"}}' % pwd
        response = requests.post(url, data=payload2, headers=headers)
    stok = json.loads(response.text)['stok']
    return stok

def user_list(url, stok):
    url = '%sstok=%s/ds' % (url,stok)
    payload = '{"hosts_info":{"table":"host_info"},"method":"get"}'
    response = requests.post(url, data=payload, headers=headers)
    # 返回的response为json结构，内部字符串采用URL编码
    for l in json.loads(response.text)['hosts_info']['host_info']:
        for k,v in l.items():
            for k2,v2 in v.items():
                if k2 == 'hostname':
                    username = urllib.parse.unquote(v2)
                elif k2 == 'ip':
                    ip = v2
                elif k2 == 'up_speed':
                    upspeed = v2
                elif k2 == 'down_speed':
                    downspeed = v2
            print('用户名：' + username, 'IP地址：' + ip, '上传速度：' + upspeed + 'B/s', '下载速度：' + downspeed + 'B/s')

if __name__ == '__main__':
    type_in = input('请输入密码：')
    password = check_pwd(type_in)
    encryptPwd = encrypt_pwd(password)
    stok = stok(url, encryptPwd)
    user_list(url, stok)
